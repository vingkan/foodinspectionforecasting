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