TARGET = "criticalFound"
DATE = "Inspection_Date"
LICENSE = "License"
INSPECTION_ID = "Inspection_ID"
BUSINESS_ID = "Business_ID"
INSPECTORS = [
    "Inspector_blue",
    "Inspector_brown",
    "Inspector_green",
    "Inspector_orange",
    "Inspector_purple",
    "Inspector_yellow",
]
OTHER_PREDICTORS = [
    "pastSerious",
    "pastCritical",
    "timeSinceLast",
    "ageAtInspection",
    "consumption_on_premises_incidental_activity",
    "tobacco_retail_over_counter",
    "temperatureMax",
    "heat_burglary",
    "heat_sanitation",
    "heat_garbage",
]
DETAILS = [
    "address",
    "aka_name",
    "city",
    "dba_name",
    "facility_type",
    "inspection_date",
    "inspection_type",
    "latitude",
    "license_id",
    "longitude",
    "results",
    "risk",
    "state",
    "violations",
    "zip",
]
VIOLATIONS = [
    "V1",
    "V2",
    "V3",
    "V4",
    "V5",
    "V6",
    "V7",
    "V8",
    "V9",
    "V10",
    "V11",
    "V12",
    "V13",
    "V14",
]
MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
META = [DATE, LICENSE, INSPECTION_ID, BUSINESS_ID]
PREDICTORS = INSPECTORS + OTHER_PREDICTORS
