import numpy as np
from spy4cast import Dataset, Region, Month
from spy4cast.spy4cast import Preprocess, MCA, Crossvalidation

# Pacific impact on Sahelian rainfall

predictor = Dataset("HadISST_sst_chopped.nc", "./datasets").open("sst").slice(
    Region(lat0=-30, latf=30,
           lon0=-200, lonf=-60,
           month0=Month.APR, monthf=Month.JUN,
           year0=1970, yearf=2000),
)

predictand = Dataset("cru_ts4_pre_chopped.nc", "./datasets").open("pre").slice(
    Region(lat0=0, latf=25,
           lon0=-20, lonf=20,
           month0=Month.JUL, monthf=Month.SEP,
           year0=1970, yearf=2000),
)
#  There is a lag of 3 months (from April to July)

## METHODOLOGY

# First step. Preprocess variables: anomaly and reshaping
predictor_preprocessed = Preprocess(predictor, period=4, order=4, freq="high")
predictor_preprocessed.save("y_", "./data-Pacific_Impact_Sahelian_Rainfall/")
# Save matrices as .npy for fast loading. To load use:
# predictor_preprocessed = Preprocess.load("y_", "./data-Pacific_Impact_Sahelian_Rainfall/")
predictand_preprocessed = Preprocess(predictand)
# predictand_preprocessed.save("z_", "./data-Pacific_Impact_Sahelian_Rainfall/")
predictand_preprocessed = Preprocess.load("z_", "./data-Pacific_Impact_Sahelian_Rainfall")

# Second step. MCA: expansion coefficients and correlation and regression maps
nm = 3
alpha = 0.05
mca = MCA(predictor_preprocessed, predictand_preprocessed, nm, alpha)
mca.save("mca_", "./data-Pacific_Impact_Sahelian_Rainfall/")
mca = MCA.load("mca_", "./data-Pacific_Impact_Sahelian_Rainfall/", dsy=predictor_preprocessed, dsz=predictand_preprocessed)

# Third step. Crossvalidation: skill and hidcast evaluation and products
cross = Crossvalidation(predictor_preprocessed, predictand_preprocessed, nm, alpha)
cross.save("cross_", "./data-Pacific_Impact_Sahelian_Rainfall/")
# cross = Crossvalidation.load("cross_", "./data-Pacific_Impact_Sahelian_Rainfall/", dsy=predictor_preprocessed, dsz=predictand_preprocessed)

mca.plot(
    save_fig=True, cmap="BrBG", name="mca.png",
    folder="./plots-Pacific_Impact_Sahelian_Rainfall/",
    ruy_ticks=[-1, -0.5, 0, 0.5, 1],
    ruz_ticks=[-1, -0.5, 0, 0.5, 1],
)
cross.plot(
    save_fig=True, name="cross.png",
    folder="./plots-Pacific_Impact_Sahelian_Rainfall/",
    cmap="BrBG", 
    map_ticks=[-0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2],
    map_levels=[-0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2],
)
cross.plot_zhat(1999, figsize=(12, 10), save_fig=True, name="zhat_1999.png", 
                folder="./plots-Pacific_Impact_Sahelian_Rainfall/", cmap="BrBG", 
                z_levels=np.linspace(-100, 100, 15))

# Plot regression on a bigger map
map_y = Dataset("HadISST_sst_chopped.nc", "./datasets").open("sst").slice(
    Region(lat0=-32, latf=32,
           lon0=-309.5, lonf=39.5,
           month0=Month.APR, monthf=Month.JUN,
           year0=1976, yearf=2009),
)

map_y_pre = Preprocess(map_y)

mca.plot(
    save_fig=True, cmap="BrBG", name="mca2.png",
    folder="./plots-Pacific_Impact_Sahelian_Rainfall/",
    ruy_ticks=[-1, -0.5, 0, 0.5, 1],
    ruz_ticks=[-1, -0.5, 0, 0.5, 1],
    map_y=map_y_pre)

# To show the figures:
import matplotlib.pyplot as plt
plt.show()

