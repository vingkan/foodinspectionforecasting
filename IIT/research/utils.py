import pandas as pd


from sklearn.preprocessing import MultiLabelBinarizer


def get_violation_codes(report):
    if pd.isnull(report):
        return []
    else:
        codes = [int(comment.split(".")[0]) for comment in report.split(" | ")]
        return codes


def get_violation_level(code):
    if code <= 14:
        return "critical"
    elif code <= 29:
        return "serious"
    elif code <= 44 or code == 70:
        return "minor"
    else:
        return "unknown"


def get_crit_mat(df):
    code_array = [get_violation_codes(report) for report in df["violations"].values]
    crit_array = [
        list(filter(lambda code: get_violation_level(code) == "critical", arr))
        for arr in code_array
    ]
    crit_array = [["V" + str(i) for i in arr] for arr in crit_array]
    crit_viols = ["V" + str(i) for i in range(1, 15)]
    mlb_crit = MultiLabelBinarizer(classes=crit_viols)
    mlb_crit.fit(crit_array)
    crit_mat = pd.DataFrame(mlb_crit.transform(crit_array), columns=mlb_crit.classes_)
    return crit_mat
