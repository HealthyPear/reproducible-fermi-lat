import matplotlib.pyplot as plt
import numpy as np

from fermipy.gtanalysis import GTAnalysis
from fermipy.plotting import ROIPlotter

import paths

tsmap_output = np.load(
    paths.data / "Fermi_LAT/fermipy_analysis/null_hypothesis_tsmap_output.npy",
    allow_pickle=True,
).flat[0]


gta = GTAnalysis.create(
    str(paths.data / "Fermi_LAT/fermipy_analysis/null_hypothesis.npy")
)

fig = plt.figure(figsize=(14, 6))

print(tsmap_output)


ROIPlotter(tsmap_output["sqrt_ts"], roi=gta.roi).plot(
    levels=[0, 3, 5, 7],
    # vmin=3,
    # vmax=5,
    # subplot=111,
    cmap="magma",
)
plt.gca().set_title("Sqrt(TS)")

plt.savefig(
    paths.figures / "null_hypothesis_pointsource_powerlaw_2.00_tsmap_sqrt_ts.png"
)
