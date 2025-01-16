"""Produce a fermipy ltcube from a config file."""

import argparse
import os

from pathlib import Path

from fermipy.gtanalysis import GTAnalysis

import paths

parser = argparse.ArgumentParser(
    prog="fermi_ltcube",
    description="Produce a fermipy ltcube from a config file.",
)
parser.add_argument("--config", type=str, required=True)
args = parser.parse_args()

data_path = paths.data

config_path = Path(args.config)

os.environ["LATEXTDIR"] = str((data_path / "Fermi_LAT/Extended_14years").resolve())

gta = GTAnalysis(str(config_path), logging={"verbosity": 3})
# data preparation and response calculations needed for the analysis
# (selecting the data, creating counts and exposure maps, etc.)
gta.setup()
# output of setup() is cached in the analysis working directory
# so subsequent calls to setup() will run much faster.
