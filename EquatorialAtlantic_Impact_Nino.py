from spy4cast import Dataset, Region, Month
from spy4cast.spy4cast import Preprocess, MCA, Crossvalidation

## CONFIGURATION
# We will use sea surface temperature both for dataset and predictor, but
# with differnt regions
predictor = Dataset("HadISST_sst-1970_2020.nc", "./datasets").open("sst").slice(
    Region(lat0=-30, latf=30,
           lon0=-60, lonf=15,
           month0=Month.MAY, monthf=Month.JUL,
           year0=1976, yearf=2000),
    skip=1
)
predictand = Dataset("HadISST_sst-1970_2020.nc", "./datasets").open("sst").slice(
    Region(lat0=-30, latf=30,
           lon0=-200, lonf=-60,
           month0=Month.DEC, monthf=Month.FEB,
           year0=1977, yearf=2001),
    skip=1
)
# There is a lag of 7 months (from May to December)

## METHODOLOGY

# First step. Preprocess variables: anomaly and reshaping
predictor_preprocessed = Preprocess(predictor)
predictor_preprocessed.save("y_", "./data-EquatorialAtalantic_Impact_Nino/")
# Save matrices as .npy for fast loading. To load use:
# predictor_preprocessed = Preprocess.load("y_", "./data-EquatorialAtalantic_Impact_Nino/")
predictand_preprocessed = Preprocess(predictand)
predictand_preprocessed.save("z_", "./data-EquatorialAtalantic_Impact_Nino/")
# predictand_preprocessed = Preprocess.load("z_", "./data/-EquatorialAtalantic_Impact_Nino")

# Second step. MCA: expansion coefficients and correlation and regression maps
nm = 3
alpha = 0.05
mca = MCA(predictor_preprocessed, predictand_preprocessed, nm, alpha)
mca.save("mca_", "./data-EquatorialAtalantic_Impact_Nino/")
# mca = MCA.load("mca_", "./data-EquatorialAtalantic_Impact_Nino/", dsy=predictor_preprocessed, dsz=predictand_preprocessed)

# Third step. Crossvalidation: skill and hidcast evaluation and products
cross = Crossvalidation(predictor_preprocessed, predictand_preprocessed, nm, alpha)
cross.save("cross_", "./data-EquatorialAtalantic_Impact_Nino/")
# cross = Crossvalidation.load("cross_", "./data-EquatorialAtalantic_Impact_Nino/", dsy=predictor_preprocessed, dsz=predictand_preprocessed)

mca.plot(save_fig=True, name="mca.png", folder="./plots-EquatorialAtalantic_Impact_Nino/", suy_ticks=[-0.25, -0.125, 0, 0.125, 0.250], suz_ticks=[-0.25, -0.125, 0, 0.125, 0.250])
cross.plot(save_fig=True, name="cross.png", folder="./plots-EquatorialAtalantic_Impact_Nino/")
