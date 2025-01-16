from yaml import safe_load

from astropy.coordinates import SkyCoord

import paths

with open(paths.scripts / "fermipy_data.yml", mode="r", encoding="utf-8") as file:
    fermi_data_config = safe_load(file)

coordinates = SkyCoord(
    ra=fermi_data_config["query"]["name_or_coordinates"][0],
    dec=fermi_data_config["query"]["name_or_coordinates"][1],
    unit="deg",
    frame="icrs",
)

with open(
    paths.output / "download_coordinates.txt", mode="w", encoding="utf-8"
) as file:
    file.write(f"{coordinates.to_string('decimal')}")
