import pandas as pd
import sys
from lib.strings import TARGET, DATE, PREDICTORS

trainfile = sys.argv[1]
testfile = sys.argv[2]
infile = sys.argv[3]
if not trainfile:
    raise ValueError("No trainfile specified.")
if not testfile:
    raise ValueError("No testfile specified.")
if not infile:
    raise ValueError("No infile specified.")


colnames = [TARGET, DATE] + PREDICTORS
# This integer value represents the split date: 2014-07-01
SPLIT_DATE = 16252


mm = pd.read_csv(infile)
# Date range for entries before split date: "2011-09-02" to "2014-04-16"
# Date range for entries after split date: "2014-09-02" to "2014-10-31"
iiTrain = mm["Inspection_Date"] < SPLIT_DATE
iiTest = mm["Inspection_Date"] > SPLIT_DATE
# Check to see if any rows didn't make it through the model.matrix formula
# len(dat), len(xmat), len(mm)
data_train = mm[iiTrain][colnames]
data_test = mm[iiTest][colnames]
data_train.to_csv(trainfile, index=False)
data_test.to_csv(testfile, index=False)
