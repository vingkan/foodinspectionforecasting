import pandas as pd
import numpy as np
import sys


outfile = sys.argv[1]
infile = sys.argv[2]
if not outfile:
    raise ValueError("No outfile specified.")
if not infile:
    raise ValueError("No infile specified.")


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
# Add inspection date for train/test split
mm["Inspection_Date"] = dat["Inspection_Date"]
mm.to_csv(outfile, index=False)