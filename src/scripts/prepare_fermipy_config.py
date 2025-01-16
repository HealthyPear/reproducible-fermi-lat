"""This script loads the fermipy config as a template ans fills it with information from previous steps."""

from datetime import datetime
from pathlib import Path

from astropy.coordinates import SkyCoord
from astropy.time import Time
from yaml import load, dump, Loader

import paths

# Load the template configuration file
with open(paths.scripts / "fermipy_config.yml", mode="r", encoding="utf-8") as file:
    input_configuration = load(file, Loader=Loader)

# Load the template configuration file
with open(paths.scripts / "fermipy_data.yml", mode="r", encoding="utf-8") as file:
    fermi_data_config = load(file, Loader=Loader)

coordinates = SkyCoord(
    ra=fermi_data_config["query"]["name_or_coordinates"][0],
    dec=fermi_data_config["query"]["name_or_coordinates"][1],
    unit="deg",
    frame="icrs",
)

input_configuration["selection"]["ra"] = float(coordinates.ra.to_value("deg"))
input_configuration["selection"]["dec"] = float(coordinates.dec.to_value("deg"))

input_configuration["selection"]["emin"] = float(
    fermi_data_config["query"]["energy_range_MeV"].split(",")[0].strip()
)

input_configuration["selection"]["emin"] = 10000

input_configuration["selection"]["emax"] = float(
    fermi_data_config["query"]["energy_range_MeV"].split(",")[1].strip()
)

observation_dates = fermi_data_config["query"]["observation_dates"].split(",")

mission_start = Time("2001-01-01 00:00:00", format="iso", scale="utc")

tmin = (
    mission_start
    if "START" in observation_dates[0]
    else Time(observation_dates[0].strip(), format="iso", scale="utc")
)
tmax = (
    Time(datetime.utcnow())
    if "END" in observation_dates[1]
    else Time(observation_dates[1].strip(), format="iso", scale="utc")
)
input_configuration["selection"]["tmin"] = float((tmin - mission_start).sec)
input_configuration["selection"]["tmax"] = float((tmax - mission_start).sec)


fermipy_output_path = paths.data / "Fermi_LAT"

input_configuration["data"]["evfile"] = str(fermipy_output_path / "evt.list")
input_configuration["data"]["scfile"] = [
    str(path) for path in fermipy_output_path.glob("*SC*.fits")
][0]

input_configuration["fileio"]["outdir"] = str(fermipy_output_path / "fermipy_analysis")
input_configuration["fileio"]["logfile"] = str(
    Path(input_configuration["fileio"]["outdir"]) / "fermipy_analysis.log"
)

input_configuration["model"]["galdiff"] = [
    str(path) for path in fermipy_output_path.glob("gll*.fits")
]
input_configuration["model"]["isodiff"] = [
    str(path) for path in fermipy_output_path.glob("iso*.txt")
]
input_configuration["model"]["catalogs"] = [
    str(path) for path in fermipy_output_path.glob("gll*.xml")
]

# Write the final configuration file
with open(
    fermipy_output_path / "fermipy_config.yml", mode="w", encoding="utf-8"
) as file:
    dump(input_configuration, file)
