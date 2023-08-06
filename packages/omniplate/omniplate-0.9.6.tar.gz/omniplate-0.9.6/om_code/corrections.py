# functions for correcting for non-linearities in the OD, for
# the fluorescence of the media, and for autofluorescence
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import gaussianprocessderivatives as gp
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.optimize import minimize_scalar
import pandas as pd
import re
import importlib.resources as import_files
import om_code.sunder as sunder
import om_code.omerrors as errors
import om_code.omgenutils as gu


def _read_dilution_data(fname):
    d = import_files.read_text("om_code", fname)
    res = np.array(re.split(r"\n|\t", d)[:-1]).astype(float)
    od, dilfac = res[::2], res[1::2]
    return od, dilfac


def findODcorrection(wdirpath, ODfname, figs, odmatch, bd, gp_results):
    """
    Determine a function to correct OD.

    Use a Gaussian process to fit serial dilution data to correct for
    non-linearities in the relationship between OD and cell density.

    The data are either loaded from file ODfname or the default
    data for haploid yeast growing in glucose are used.
    """
    print("Fitting dilution data for OD correction for non-linearities")
    if ODfname is not None:
        try:
            od_df = pd.read_csv(
                str(wdirpath / ODfname), sep=None, engine="python", header=None
            )
            print("Using", ODfname)
            od_data = od_df.to_numpy()
            od, dilfac = od_data[:, 0], od_data[:, 1]
        except (FileNotFoundError, OSError):
            raise errors.FileNotFound(str(wdirpath / ODfname))
    else:
        print("Using default data")
        fname = "dilution_data_xiao.tsv"
        od, dilfac = _read_dilution_data(fname)
    # process data
    dilfac = dilfac[np.argsort(od)]
    od = np.sort(od)
    if odmatch is not None:
        # rescale so that OD and dilfac match at a particular OD
        # compares better with Warringer & Blomberg, Yeast 2003,
        # and rescaled OD is larger
        dilfacmatch = interp1d(od, dilfac)(odmatch)
        y = dilfac / dilfacmatch * odmatch
    else:
        y = dilfac
    # set up Gaussian process
    bds = {0: (-4, 4), 1: (-4, 4), 2: (-3, 1)}
    # find bounds
    if bd is not None:
        bds = gu.mergedicts(original=bds, update=bd)
    gc = gp.maternGP(bds, od, y)
    # run Gaussian process
    gc.findhyperparameters(noruns=5, exitearly=True, quiet=True)
    if gp_results:
        gc.results()
    gc.predict(od)
    if figs:
        plt.figure()
        gc.sketch(".")
        plt.grid(True)
        plt.xlabel("OD")
        plt.ylabel("corrected OD (relative cell numbers)")
        if ODfname:
            plt.title("Fitting " + ODfname)
        else:
            plt.title("for haploid budding yeast in glucose")
        plt.show()
    return gc


###


def performmediacorrection(r_df, dtype, exp, condition, figs, commonmedia, frac):
    """
    Correct data of type dtype for any signal from the media.

    Use lowess to smooth over time the media data from the Null
    wells and subtract the smoothed values from the data.
    """
    # find data for correction with condition equal to commonmedia
    df = r_df.query(
        "experiment == @exp and condition == @commonmedia" " and strain == 'Null'"
    )
    if df.empty:
        # no data
        print(
            ' No well annotated "Null" was found for',
            commonmedia,
            "in experiment",
            exp,
        )
        print(" Correcting for media for", dtype, "in", commonmedia, "abandoned!")
        return False, None
    else:
        # there is data - change r dataframe
        rtest = (r_df.experiment == exp) & (r_df.condition == condition)
        t, data = df["time"].to_numpy(), df[dtype].to_numpy()
        # find correction
        res = lowess(data, t, frac=frac)
        correctionfn = interp1d(
            res[:, 0],
            res[:, 1],
            fill_value=(res[0, 1], res[-1, 1]),
            bounds_error=False,
        )
        if figs:
            plt.figure()
            plt.plot(t, data, "ro", res[:, 0], res[:, 1], "b-")
            plt.xlabel("time (hours)")
            plt.title(exp + ": media correction for " + dtype + " in " + condition)
            plt.show()
        # perform correction
        r_df.loc[rtest, dtype] = r_df[rtest][dtype] - correctionfn(r_df[rtest]["time"])
        # check for any negative values
        negvalues = ""
        for s in np.unique(r_df[rtest]["strain"][r_df[rtest][dtype] < 0]):
            if s != "Null":
                wstr = "\t" + dtype + ": " + s + " in " + condition + " for wells "
                for well in np.unique(
                    r_df[rtest][r_df[rtest].strain == s]["well"][r_df[rtest][dtype] < 0]
                ):
                    wstr += well + " "
                wstr += "\n"
                negvalues += wstr
        return True, negvalues


###


def correctauto1(
    self,
    f,
    refstrain,
    figs,
    experiments,
    experimentincludes,
    experimentexcludes,
    conditions,
    conditionincludes,
    conditionexcludes,
    strains,
    strainincludes,
    strainexcludes,
):
    """
    Correct autofluorescence for measurements with emissions at one wavelength.

    Corrects for autofluorescence for data with emissions measured at one
    wavelength using the fluorescence of the reference strain
    interpolated to the OD of the tagged strain.

    This method in principle corrects too for the fluorescence of the medium,
    although running correctmedia is still recommended.
    """
    print("Correcting autofluorescence using", f[0])
    for e in sunder.getexps(self, experiments, experimentincludes, experimentexcludes):
        for c in sunder.getcons(
            self,
            conditions,
            conditionincludes,
            conditionexcludes,
            nomedia=True,
        ):
            # process reference strain
            refstrfn = processref1(self, f, refstrain, figs, e, c)
            # correct strains
            for s in sunder.getstrs(
                self, strains, strainincludes, strainexcludes, nonull=True
            ):
                if not self.sc[
                    (self.sc.experiment == e)
                    & (self.sc.condition == c)
                    & (self.sc.strain == s)
                ][f[0] + " corrected for autofluorescence"].any():
                    od, rawfl = sunder.extractwells(
                        self.r, self.s, e, c, s, ["OD", f[0]]
                    )
                    # no data
                    if od.size == 0 or rawfl.size == 0:
                        continue
                    # correct autofluorescence for each replicate
                    fl = np.transpose(
                        [rawfl[:, i] - refstrfn(od[:, i]) for i in range(od.shape[1])]
                    )
                    flperod = np.transpose(
                        [
                            (rawfl[:, i] - refstrfn(od[:, i])) / od[:, i]
                            for i in range(od.shape[1])
                        ]
                    )
                    # replace negative values with NaNs
                    fl[fl < 0] = np.nan
                    flperod[flperod < 0] = np.nan
                    nonans = np.count_nonzero(np.isnan(fl))
                    if np.any(nonans):
                        print(
                            "Warning -",
                            e + ":",
                            s,
                            "in",
                            c,
                            "\n",
                            nonans,
                            "corrected data points are"
                            " NaN because the corrected fluorescence"
                            " was negative",
                        )
                        if nonans == fl.size:
                            print(
                                "Warning -",
                                e + ":",
                                s,
                                "in",
                                c,
                                "\n",
                                "Corrected fluorescence is all NaN",
                            )
                    # store results
                    bname = "c-" + f[0]
                    autofdict = {
                        "experiment": e,
                        "condition": c,
                        "strain": s,
                        "time": self.s.query(
                            "experiment == @e and condition == @c " "and strain == @s"
                        )["time"].to_numpy(),
                        bname: np.nanmean(fl, 1),
                        bname + " err": nanstdzeros2nan(fl, 1),
                        bname + "perOD": np.nanmean(flperod, 1),
                        bname + "perOD err": nanstdzeros2nan(flperod, 1),
                    }
                    autofdf = pd.DataFrame(autofdict)
                    if bname not in self.s.columns:
                        # extend dataframe
                        self.s = pd.merge(self.s, autofdf, how="outer")
                    else:
                        # update dataframe
                        self.s = gu.absorbdf(
                            self.s,
                            autofdf,
                            ["experiment", "condition", "strain", "time"],
                        )
                    # record that correction has occurred
                    self.sc.loc[
                        (self.sc.experiment == e)
                        & (self.sc.condition == c)
                        & (self.sc.strain == s),
                        f[0] + " corrected for autofluorescence",
                    ] = True


###


def processref1(self, f, refstrain, figs, experiment, condition):
    """
    Process reference strain for data with one fluorescence measurement.

    Use lowess to smooth the fluorescence of the reference
    strain as a function of OD.

    Parameters
    ----------
    f: string
        The fluorescence to be corrected. For example, ['mCherry'].
    refstrain: string
        The reference strain. For example, 'WT'.
    figs: boolean
        If True, display fits of the reference strain's fluorescence.
    experiment: string
        The experiment to be corrected.
    condition: string
        The condition to be corrected.

    Returns
    -------
    refstrfn: function
        The reference strain's fluorescence as a function of OD.
    """
    e, c = experiment, condition
    print(
        e + ": Processing reference strain",
        refstrain,
        "for",
        f[0],
        "in",
        c,
    )
    od, fl = sunder.extractwells(self.r, self.s, e, c, refstrain, ["OD", f[0]])
    if od.size == 0 or fl.size == 0:
        raise errors.CorrectAuto(e + ": " + refstrain + " not found in " + c)
    else:
        odf = od.flatten("F")
        flf = fl.flatten("F")
        # smooth fluorescence as a function of OD using lowess to minimize
        # refstrain's autofluorescence

        def choosefrac(frac):
            res = lowess(flf, odf, frac=frac)
            refstrfn = interp1d(
                res[:, 0],
                res[:, 1],
                fill_value=(res[0, 1], res[-1, 1]),
                bounds_error=False,
            )
            # max gives smoother fits than mean
            return np.max(np.abs(flf - refstrfn(odf)))

        res = minimize_scalar(choosefrac, bounds=(0.1, 0.99), method="bounded")
        # choose the optimum frac
        frac = res.x if res.success else 0.33
        res = lowess(flf, odf, frac=frac)
        refstrfn = interp1d(
            res[:, 0],
            res[:, 1],
            fill_value=(res[0, 1], res[-1, 1]),
            bounds_error=False,
        )
        if figs:
            # plot fit
            plt.figure()
            plt.plot(odf, flf, ".", alpha=0.5)
            plt.plot(res[:, 0], res[:, 1])
            plt.xlabel("OD")
            plt.ylabel(f[0])
            plt.title(e + ": " + refstrain + " for " + c)
            plt.show()
        return refstrfn


###


def correctauto2(
    self,
    f,
    refstrain,
    figs,
    experiments,
    experimentincludes,
    experimentexcludes,
    conditions,
    conditionincludes,
    conditionexcludes,
    strains,
    strainincludes,
    strainexcludes,
):
    """
    Correct autofluorescence for measurements with two emission wavelengths.

    Corrects for autofluorescence using spectral unmixing for data with
    measured emissions at two wavelengths.

    References
    ----------
    CA Lichten, R White, IB Clark, PS Swain (2014). Unmixing of fluorescence
    spectra to resolve quantitative time-series measurements of gene
    expression in plate readers.
    BMC Biotech, 14, 1-11.
    """
    # correct for autofluorescence
    print("Correcting autofluorescence using", f[0], "and", f[1])
    for e in sunder.getexps(self, experiments, experimentincludes, experimentexcludes):
        for c in sunder.getcons(
            self,
            conditions,
            conditionincludes,
            conditionexcludes,
            nomedia=True,
        ):
            # process reference strain
            refqrfn = processref2(self, f, refstrain, figs, e, c)
            # process other strains
            for s in sunder.getstrs(
                self, strains, strainincludes, strainexcludes, nonull=True
            ):
                if s != refstrain and not (
                    self.sc[
                        (self.sc.experiment == e)
                        & (self.sc.condition == c)
                        & (self.sc.strain == s)
                    ][f[0] + " corrected for autofluorescence"].any()
                ):
                    f0, f1 = sunder.extractwells(self.r, self.s, e, c, s, f)
                    if f0.size == 0 or f1.size == 0:
                        continue
                    nodata, nr = f0.shape
                    # set negative values to NaNs
                    f0[f0 < 0] = np.nan
                    f1[f1 < 0] = np.nan
                    # use mean OD for correction
                    odmean = self.s.query(
                        "experiment == @e and condition == @c and strain == @s"
                    )["OD mean"].to_numpy()
                    # remove autofluorescence
                    ra = refqrfn(odmean)
                    fl = applyautoflcorrection(self, ra, f0, f1)
                    od = sunder.extractwells(self.r, self.s, e, c, s, "OD")
                    flperod = fl / od
                    # set negative values to NaNs
                    fl[fl < 0] = np.nan
                    flperod[flperod < 0] = np.nan
                    # store corrected fluorescence
                    bname = "c-" + f[0]
                    autofdict = {
                        "experiment": e,
                        "condition": c,
                        "strain": s,
                        "time": self.s.query(
                            "experiment == @e and condition == @c" " and strain == @s"
                        )["time"].to_numpy(),
                        bname: np.nanmean(fl, 1),
                        bname + " err": nanstdzeros2nan(fl, 1),
                        bname + "perOD": np.nanmean(flperod, 1),
                        bname + "perOD err": nanstdzeros2nan(flperod, 1),
                    }
                    # add to dataframe
                    self.s = gu.absorbdf(
                        self.s,
                        pd.DataFrame(autofdict),
                        ["experiment", "condition", "strain", "time"],
                    )
                    self.sc.loc[
                        (self.sc.experiment == e)
                        & (self.sc.condition == c)
                        & (self.sc.strain == s),
                        f[0] + " corrected for autofluorescence",
                    ] = True


###


def processref2(self, f, refstrain, figs, experiment, condition):
    """
    Process reference strain for spectral unmixing.

    Requires data with two fluorescence measurements.

    Use lowess to smooth the ratio of emitted fluorescence measurements
    so that the reference strain's data is corrected to zero as best
    as possible.

    Parameters
    ----------
    f: list of strings
        The fluorescence measurements. For example, ['GFP', 'AutoFL'].
    refstrain: string
        The reference strain. For example, 'WT'.
    figs: boolean
        If True, display fits of the fluorescence ratios.
    experiment: string
        The experiment to be corrected.
    condition: string
        The condition to be corrected.

    Returns
    -------
    qrfn: function
        The ratio of the two fluorescences for the reference strain as a
        function of OD.
    """
    e, c = experiment, condition
    print(
        e + ": Processing reference strain",
        refstrain,
        "for",
        f[0],
        "in",
        c,
    )
    # refstrain data
    f0, f1, od = sunder.extractwells(self.r, self.s, e, c, refstrain, f + ["OD"])
    if f0.size == 0 or f1.size == 0 or od.size == 0:
        raise errors.CorrectAuto(e + ": " + refstrain + " not found in " + c)
    else:
        f0[f0 < 0] = np.nan
        f1[f1 < 0] = np.nan
        odf = od.flatten("F")
        odrefmean = np.mean(od, 1)
        qrf = (f1 / f0).flatten("F")
        if np.all(np.isnan(qrf)):
            raise errors.CorrectAuto(
                e + ": " + refstrain + " in " + c + " has too many NaNs"
            )
        # smooth to minimize autofluorescence in refstrain

        def choosefrac(frac):
            res = lowess(qrf, odf, frac)
            qrfn = interp1d(
                res[:, 0],
                res[:, 1],
                fill_value=(res[0, 1], res[-1, 1]),
                bounds_error=False,
            )
            flref = applyautoflcorrection(self, qrfn(odrefmean), f0, f1)
            return np.max(np.abs(flref))

        res = minimize_scalar(choosefrac, bounds=(0.1, 0.99), method="bounded")
        # calculate the relationship between qr and OD
        frac = res.x if res.success else 0.95
        res = lowess(qrf, odf, frac)
        qrfn = interp1d(
            res[:, 0],
            res[:, 1],
            fill_value=(res[0, 1], res[-1, 1]),
            bounds_error=False,
        )
        if figs:
            plt.figure()
            plt.plot(odf, qrf, ".", alpha=0.5)
            plt.plot(res[:, 0], res[:, 1])
            plt.xlabel("OD")
            plt.ylabel(f[1] + "/" + f[0])
            plt.title(e + ": " + refstrain + " in " + c)
            plt.show()
        # check autofluorescence correction for reference strain
        flref = applyautoflcorrection(self, qrfn(odrefmean), f0, f1)
        flrefperod = flref / od
        # set negative values to NaNs
        flref[flref < 0] = np.nan
        flrefperod[flrefperod < 0] = np.nan
        # store results
        bname = "c-" + f[0]
        autofdict = {
            "experiment": e,
            "condition": c,
            "strain": refstrain,
            "time": self.s.query(
                "experiment == @e and condition == @c and strain == @refstrain"
            )["time"].to_numpy(),
            bname: np.nanmean(flref, 1),
            bname + "perOD": np.nanmean(flrefperod, 1),
            bname + " err": nanstdzeros2nan(flref, 1),
            bname + "perOD err": nanstdzeros2nan(flrefperod, 1),
        }
        if bname not in self.s.columns:
            self.s = pd.merge(self.s, pd.DataFrame(autofdict), how="outer")
        else:
            self.s = gu.absorbdf(
                self.s,
                pd.DataFrame(autofdict),
                ["experiment", "condition", "strain", "time"],
            )
        return qrfn


###


def applyautoflcorrection(self, ra, f0data, f1data):
    """Correct for autofluorescence returning an array of replicates."""
    nr = f0data.shape[1]
    raa = np.reshape(np.tile(ra, nr), (np.size(ra), nr), order="F")
    return (raa * f0data - f1data) / (raa - self._gamma * np.ones(np.shape(raa)))


###


def nanstdzeros2nan(a, axis=None):
    """Like nanstd but setting zeros to nan."""
    err = np.nanstd(a, axis)
    err[err == 0] = np.nan
    return err
