simport pandas as pd
import numpy as np
import pyreadr
import sys


outfile = sys.argv[1]
infile = sys.argv[2]
if not outfile:
    raise ValueError("No outfile specified.")
if not infile:
    raise ValueError("No infile specified.")


raw_dat = pyreadr.read_r(infile)[None]
# Only keep "Retail Food Establishment"
dat_retail = raw_dat.query("LICENSE_DESCRIPTION == 'Retail Food Establishment'")
# Remove License Description
dat_all = dat_retail.drop(columns=["LICENSE_DESCRIPTION"])
dat = pd.DataFrame(dat_all.dropna())
# Add criticalFound variable to dat:
# dat["criticalFound"] = (dat["criticalCount"] > 0).astype(int)
# To be faithful to the R source:
dat["criticalFound"] = np.minimum(1, dat["criticalCount"])
dat.to_csv(outfile, index=False)
