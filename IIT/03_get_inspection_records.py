import pandas as pd
import requests
import sys


outfile = sys.argv[1]
if not outfile:
    raise ValueError("No outfile specified.")


INSPECTIONS_DATA_URL = "https://data.cityofchicago.org/resource/cwig-ma7x.json"
query = """
    SELECT
        address AS address,
        aka_name AS aka_name,
        city AS city,
        dba_name AS dba_name,
        facility_type AS facility_type,
        inspection_date AS inspection_date,
        inspection_id AS inspection_id,
        inspection_type AS inspection_type,
        latitude AS latitude,
        license_ AS license_id,
        longitude AS longitude,
        results AS results,
        risk AS risk,
        state AS state,
        violations AS violations,
        zip AS zip
    WHERE
        inspection_type = "Canvass"
        AND inspection_date >= "2011-01-01"
        AND inspection_date <= "2014-11-01"
    LIMIT 100000
"""


r = requests.get(INSPECTIONS_DATA_URL, params={"$query": query})
rows = r.json()
# Expect 41366 rows
print("Returned {} rows from query.".format(len(rows)))
data = pd.DataFrame(rows)
data.to_csv(outfile, index=False)
