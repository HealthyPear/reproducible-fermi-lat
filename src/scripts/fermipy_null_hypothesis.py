"""Build the baseline model for the ROI using only the cataloged sources."""

import os

import numpy as np

from fermipy.gtanalysis import GTAnalysis

import paths

from fermipy_helpers import gta_preliminaries

data_path = paths.data

config_path = data_path / "Fermi_LAT/fermipy_config.yml"

os.environ["LATEXTDIR"] = str((data_path / "Fermi_LAT/Extended_14years").resolve())

gta = GTAnalysis(str(config_path), logging={"verbosity": 3})
gta.setup()

gta = gta_preliminaries(gta)

# free stuff

# Free normalization of all sources within 10 deg of ROI center
gta.free_sources(distance=10.0, pars="norm", minmax_ts=[9, np.inf])
# Free normalization and spectral indices of all sources within 10 deg of ROI center
gta.free_sources(distance=5.0, pars="shape", minmax_ts=[25, np.inf])

# Free all parameters of isotropic and galactic diffuse components
gta.free_source("galdiff")
gta.free_source("isodiff")

null_hypothesis_fit_result = gta.fit(min_fit_quality=3)

np.save(
    data_path / "Fermi_LAT/fermipy_analysis/null_hypothesis_fit_result.npy",
    null_hypothesis_fit_result,
)

gta.write_roi("null_hypothesis", make_plots=True, save_model_map=True)

tsmap_output = gta.tsmap(
    prefix="null_hypothesis",
    model=None,
    multithread=False,
    make_plots=False,
    write_fits=False,
    write_npy=True,
)

np.save(
    data_path / "Fermi_LAT/fermipy_analysis/null_hypothesis_tsmap_output.npy",
    tsmap_output,
)
