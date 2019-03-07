import pandas as pd
import sys


outfile = sys.argv[1]
infile = sys.argv[2]
inspectionfile = sys.argv[3]
if not outfile:
    raise ValueError("No outfile specified.")
if not infile:
    raise ValueError("No infile specified.")
if not inspectionfile:
    raise ValueError("No inspectionfile specified.")


data = pd.read_csv(infile)
inspections = pd.read_csv(inspectionfile)
data["inspection_id"] = data["Inspection_ID"]
merged = data.set_index("inspection_id").join(inspections.set_index("inspection_id"))
print("{} records.".format(len(merged)))
merged.to_csv(outfile, index=False)
