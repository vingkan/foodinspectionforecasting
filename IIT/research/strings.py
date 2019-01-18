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
META = [DATE, LICENSE, INSPECTION_ID, BUSINESS_ID]
PREDICTORS = INSPECTORS + OTHER_PREDICTORS
