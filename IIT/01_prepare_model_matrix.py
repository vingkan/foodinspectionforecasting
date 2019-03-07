import pandas as pd
import numpy as np
import sys
from research.strings import TARGET, META, PREDICTORS


outfile = sys.argv[1]
infile = sys.argv[2]
if not outfile:
    raise ValueError("No outfile specified.")
if not infile:
    raise ValueError("No infile specified.")


colnames = [TARGET] + META + PREDICTORS


dat = pd.read_csv(infile)
xmat = pd.DataFrame()
xmat["Inspector"] = dat["Inspector_Assigned"]
xmat["pastSerious"] = np.minimum(dat["pastSerious"], 1)
xmat["pastCritical"] = np.minimum(dat["pastCritical"], 1)
xmat["timeSinceLast"] = dat["timeSinceLast"]
xmat["ageAtInspection"] = (dat["ageAtInspection"] > 4).astype(int)
xmat["consumption_on_premises_incidental_activity"] = dat[
    "consumption_on_premises_incidental_activity"
]
xmat["tobacco_retail_over_counter"] = dat["tobacco_retail_over_counter"]
xmat["temperatureMax"] = dat["temperatureMax"]
xmat["heat_burglary"] = np.minimum(dat["heat_burglary"], 70)
xmat["heat_sanitation"] = np.minimum(dat["heat_sanitation"], 70)
xmat["heat_garbage"] = np.minimum(dat["heat_garbage"], 50)
xmat["criticalFound"] = dat["criticalFound"]
# Create model matrix
mm = pd.get_dummies(xmat)
# Add meta data columns
for meta in META:
    mm[meta] = dat[meta]
# Set column order
mm = mm[colnames]
print("{} records.".format(len(mm)))
mm.to_csv(outfile, index=False)
