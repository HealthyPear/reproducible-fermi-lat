"""Query for Fermi data from the server and save list of files to download.

The script also load from fermi_data.yml the list of auxiliary data files.
"""

from pathlib import Path

from astropy.coordinates import SkyCoord
from astroquery import fermi
from yaml import load, Loader

import paths

data_path = paths.data
fermi_data = data_path / "Fermi_LAT"
fermi_data.mkdir(parents=False, exist_ok=True)

# Load the template configuration file
with open(paths.scripts / "fermipy_data.yml", mode="r", encoding="utf-8") as file:
    config = load(file, Loader=Loader)

query_config = config["query"]

coordinates = SkyCoord(
    ra=query_config["name_or_coordinates"][0],
    dec=query_config["name_or_coordinates"][1],
    unit="deg",
    frame="icrs",
)

query = fermi.FermiLAT.query_object(
    coordinates,
    energyrange_MeV=query_config["energy_range_MeV"],
    searchradius=query_config["search_radius_degrees"],
    obsdates=query_config["observation_dates"],
    LATdatatype=query_config["LAT_data_type"],
    spacecraftdata=query_config["spacecraft_data"],
)

spacecraft_and_photons_urls_filenames = [
    (url, str(fermi_data / Path(url).name)) for url in query
]
aux_data_filenames = [
    (url, str(fermi_data / Path(url).name)) for url in config["aux_data"]
]

urls_filenames = spacecraft_and_photons_urls_filenames + aux_data_filenames

with open(fermi_data / "url_filenames.txt", mode="w", encoding="utf-8") as file:
    for url in urls_filenames:
        file.write(f"{url}\n")
