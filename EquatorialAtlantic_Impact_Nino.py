import numpy as np
from spy4cast import Dataset, Region, Month
from spy4cast.spy4cast import Preprocess, MCA, Crossvalidation, Validation

## CONFIGURATION
# We will use sea surface temperature both for dataset and predictor, but
# with differnt regions
predictor = Dataset("HadISST_sst-1960_2020.nc", "./datasets").open("sst").slice(
    Region(lat0=-30, latf=10,
           lon0=-60, lonf=15,
           month0=Month.JUN, monthf=Month.AUG,
           year0=1970, yearf=2019),
    skip=1
)
predictand = Dataset("HadISST_sst-1960_2020.nc", "./datasets").open("sst").slice(
    Region(lat0=-30, latf=30,
           lon0=-200, lonf=-60,
           month0=Month.DEC, monthf=Month.FEB,  
           # year0 and yearf refer to monthf so the slice will span from DEC 1970 to FEB 2020 
           year0=1971, yearf=2020),
    skip=1
)
#  There is a lag of 6 months (from June to December)

## METHODOLOGY

# First step. Preprocess variables: anomaly and reshaping
predictor_preprocessed = Preprocess(predictor, period=8, order=4)
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
# mca = MCA.load("mca_", "./data-EquatorialAtalantic_Impact_Nino/", dsy=predictor_preprocessed, dsz=predictand_preprocessed)

# Third step. Crossvalidation: skill and hidcast evaluation and products
cross = Crossvalidation(predictor_preprocessed, predictand_preprocessed, nm, alpha)
cross.save("cross_", "./data-EquatorialAtalantic_Impact_Nino/")
# cross = Crossvalidation.load("cross_", "./data-EquatorialAtalantic_Impact_Nino/", dsy=predictor_preprocessed, dsz=predictand_preprocessed)

mca.plot(save_fig=True, name="mca.png", folder="./plots-EquatorialAtalantic_Impact_Nino/", ruy_ticks=[-1, -0.5, 0, 0.5, 1], ruz_ticks=[-1, -0.5, 0, 0.5, 1])
cross.plot(save_fig=True, name="cross.png", folder="./plots-EquatorialAtalantic_Impact_Nino/")
cross.plot_zhat(1998, figsize=(12, 10), save_fig=True, name="zhat_1998.png", folder="./plots-EquatorialAtalantic_Impact_Nino/", z_levels=np.linspace(-2, 2, 10), z_ticks=np.linspace(-2, 2, 5))

# VALIDATION
# It is important to say that this is **not** a good example of validation becuase it uses two periods 
# where the relation is **non stationary**, so the results are not good. 
# However, it shows how to apply *Validation* to any dataset with any configuration.

# To apply validation we first preprocess the training data
training_y = Preprocess(Dataset("HadISST_sst-1960_2020.nc", "./datasets").open("sst").slice(
    Region(lat0=-30, latf=10,
           lon0=-60, lonf=15,
           month0=Month.JUN, monthf=Month.AUG,
           year0=1970, yearf=2000),
    skip=1
), period=8, order=4)
training_z = Preprocess(Dataset("HadISST_sst-1960_2020.nc", "./datasets").open("sst").slice(
    Region(lat0=-30, latf=30,
           lon0=-200, lonf=-60,
           month0=Month.DEC, monthf=Month.FEB,
           year0=1971, yearf=2001),
    skip=1
))
# Optionally save so that we save computing time for next runs
training_y.save("training_y_", "./data-EquatorialAtalantic_Impact_Nino/")
# training_y = Preprocess.load("training_y_", "./data/-EquatorialAtalantic_Impact_Nino")
training_z.save("training_z_", "./data-EquatorialAtalantic_Impact_Nino/")
# training_z = Preprocess.load("training_z_", "./data/-EquatorialAtalantic_Impact_Nino")

# Train the prediction model
training_mca = MCA(training_y, training_z, nm=6, alpha=0.05)
training_mca.save("training_mca_", "./data-EquatorialAtalantic_Impact_Nino/")
# training_mca = MCA.load("training_mca_", "./data-EquatorialAtalantic_Impact_Nino/", dsy=training_y, dsz=training_z)

# We now validate agains the period from 2001 - 2020
validating_y = Preprocess(Dataset("HadISST_sst-1960_2020.nc", "./datasets").open("sst").slice(
    Region(lat0=-30, latf=10,
           lon0=-60, lonf=15,
           month0=Month.JUN, monthf=Month.AUG,
           year0=2010, yearf=2019),
    skip=1
), period=8, order=4)
validating_z = Preprocess(Dataset("HadISST_sst-1960_2020.nc", "./datasets").open("sst").slice(
    Region(lat0=-30, latf=30,
           lon0=-200, lonf=-60,
           month0=Month.DEC, monthf=Month.FEB,
           year0=2011, yearf=2020),
    skip=1
))
# Optionally save so that we save computing time for next runs
validating_y.save("validating_y_", "./data-EquatorialAtalantic_Impact_Nino/")
# validating_y = Preprocess.load("training_y_", "./data/-EquatorialAtalantic_Impact_Nino")
validating_z.save("validating_z_", "./data-EquatorialAtalantic_Impact_Nino/")
# validating_z = Preprocess.load("validating_z_", "./data/-EquatorialAtalantic_Impact_Nino")

validation = Validation(training_mca, validating_y, validating_z)
validation.save("validation_z_", "./data-EquatorialAtalantic_Impact_Nino/")

validation.plot(save_fig=True, folder="./plots-EquatorialAtalantic_Impact_Nino/", 
                name="validation.png", version='default')
validation.plot_zhat(2016, save_fig=True, folder="./plots-EquatorialAtalantic_Impact_Nino/", 
                     name="zhat_2016_validation.png", z_levels=np.linspace(-4.1, 4.1, 10))

