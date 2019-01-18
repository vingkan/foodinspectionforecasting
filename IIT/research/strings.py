TARGET = "criticalFound"
DATE = "Inspection_Date"
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
PREDICTORS = INSPECTORS + OTHER_PREDICTORS
