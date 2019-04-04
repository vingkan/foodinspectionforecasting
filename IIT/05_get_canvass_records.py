import pandas as pd
import numpy as np
import requests
import sys
from research.utils import get_crit_mat


outfile = sys.argv[1]
if not outfile:
    raise ValueError("No outfile specified.")


INSPECTIONS_DATA_URL = "https://data.cityofchicago.org/resource/cwig-ma7x.json"
query = """
    SELECT
        address,
        aka_name,
        city,
        dba_name,
        facility_type,
        inspection_id,
        inspection_date,
        inspection_type,
        latitude,
        license_ AS license_id,
        longitude,
        results,
        risk,
        state,
        violations,
        zip
    WHERE
        facility_type == "Restaurant"
        AND inspection_type IN ("CANVAS", "Canvass", "CANVASS")
        AND results IN ("Pass", "Fail", "Pass w/ Conditions")
        AND inspection_date <= "2018-06-30"
        AND inspection_date IS NOT NULL
        AND address IS NOT NULL
        AND license_ IS NOT NULL
        AND risk IS NOT NULL
    LIMIT 60000
"""


# Fetch records from data portal
r = requests.get(INSPECTIONS_DATA_URL, params={"$query": query})
rows = r.json()
# Expect 50462 rows
print("Returned {} rows from query.".format(len(rows)))
data = pd.DataFrame(rows)

# Extract date information
data["month"] = pd.DatetimeIndex(data["inspection_date"]).month.values
data["year"] = pd.DatetimeIndex(data["inspection_date"]).year.values
data["week"] = pd.DatetimeIndex(data["inspection_date"]).week.values
data["date_str"] = (
    data["inspection_date"]
    .astype(np.datetime64)
    .apply(lambda dt: dt.strftime("%Y-%m-%d"))
)

# Extract critical violation codes
crit_mat = get_crit_mat(data)
print("Found {} critical violation labels.".format(len(crit_mat.columns)))

# Merge on inspection ID
inspection_id = "inspection_id"
crit_mat[inspection_id] = data[inspection_id]
merged = data.set_index(inspection_id).join(crit_mat.set_index(inspection_id))
merged = merged.reset_index()
print("Merged: {} records.".format(len(merged)))

# Write to file
merged.to_csv(outfile, index=False)
