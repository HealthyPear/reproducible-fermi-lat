"""Helper functions used by multiple fermipy-based scripts."""


def lock_sources(gta, exclude=[]):
    """Lock sources out of binning area of the ROI.

    Parameters
    ----------
    gta : fermipy.gtanalysis.GTAnalysis
        Instance of a fermipy high-level analysis interface.
    exclude : list of str
        List of sources to exclude from the locking procedure.
    """
    for src in sorted(gta.roi.sources, key=lambda t: t["npred"], reverse=True):
        if src.diffuse:
            continue
        if src["npred"] > 1.0:
            continue
        if src.name in exclude:
            continue
        gta.logger.info("Locking %s with npred=%s" % (src.name, src["npred"]))
        gta.lock_source(src.name, lock=True)


def gta_preliminaries(gta):
    """"""

    # First we lock those the nasty pulsar parameters
    for src in sorted(gta.roi.sources, key=lambda t: t["ts"], reverse=True):
        if src["SpectrumType"] == "PLSuperExpCutoff4":
            gta.lock_parameter(src.name, "IndexS", lock=True)
            gta.lock_parameter(src.name, "Index2", lock=True)

    # Before running any other analysis methods it is recommended to first run optimize()
    # after this every source has a TS and a npred
    # This will loop over all model components in the ROI and fit their normalization and
    # spectral shape parameters.
    # This method also computes the TS of all sources which can be useful for identifying
    # weak sources that could be fixed or removed from the model.

    gta.optimize()

    exclude = ["galdiff", "isodiff"]

    # We also lock weak sources
    for src in sorted(gta.roi.sources, key=lambda t: t["npred"], reverse=True):
        if src.diffuse:
            continue

        if src["npred"] > 1.0:
            continue

        if src.name in exclude:
            continue

        gta.logger.info("Locking %s with npred=%s" % (src.name, src["npred"]))
        gta.lock_source(src.name, lock=True)

    # 2nd optimize
    gta.optimize()
    # all sources must be fixed now (not locked, fixed)
    gta.free_sources(free=False)

    return gta
