import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


def to_inspection_daynum(date_ser):
    SECONDS = 60 * 60 * 24
    dates = date_ser.apply(lambda d: datetime.fromtimestamp(d * SECONDS))
    daynums = (dates - dates.min()).apply(lambda dt: dt.days + 1).values
    return daynums


def get_days_by_score(days, y_scores):
    res = pd.DataFrame()
    res["Score"] = y_scores
    ranked = res.sort_values(by="Score", ascending=False).reset_index()
    ranked["Day"] = np.sort(days)
    ranked_days = ranked.sort_values(by="index")["Day"].values
    return ranked_days


def get_cumulative(y_true, days):
    res = pd.DataFrame()
    res["Result"] = y_true
    res["Day"] = days
    cumsum = res.groupby("Day")["Result"].sum().cumsum()
    # Assumes that groupby.sum.cumsum is sorted by index
    total = int(cumsum.iloc[-1])
    return cumsum, total


def compare_cumulative(y_true, days, rankings, ax=None):
    if not ax:
        ax = plt.gca()
    pal = sns.hls_palette(len(rankings), h=0.5)
    true_total = int(y_true.sum())
    note = "Total number of critical violations found in {} ({}) does not match true total ({})."
    for i, (name, scores) in enumerate(rankings):
        sorted_days = get_days_by_score(days, scores)
        cumsum, total = get_cumulative(y_true, sorted_days)
        assert total == true_total, note.format(name, total, true_total)
        sns.lineplot(x=cumsum.index, y=cumsum.values, label=name, color=pal[i], ax=ax)
    ax.set_xlabel("Inspection Day")
    ax.set_ylabel("Critical Violations Found")
    ax.set_title("Critical Violations Found Over Time")
    ax.legend()


def get_days_earlier(y_true, days, y_scores):
    sorted_days = get_days_by_score(days, y_scores)
    diff = days - sorted_days
    res = pd.DataFrame()
    res["Result"] = y_true
    res["NewDay"] = sorted_days
    res["Diff"] = diff
    crit_diff = res.query("Result > 0")["Diff"].values
    return crit_diff


def get_first_half_proportion(y_true, y_scores):
    res = pd.DataFrame()
    res["Result"] = y_true
    res["Score"] = y_scores
    halftime = len(y_true) / 2
    ranked = res.sort_values(by="Score", ascending=False).reset_index()
    ranked["FirstHalf"] = np.array(range(len(y_true))) < halftime
    prop = ranked.query("FirstHalf")["Result"].sum() / y_true.sum()
    return prop


def bin_range(vals, size):
    max_val = max(max(vals), 0)
    min_val = min(min(vals), 0)
    range_max = int(size * np.ceil(max_val / size))
    range_min = int(size * np.floor(min_val / size))
    rg = range(range_min, range_max, size)
    return rg


def compare_days_earlier(y_true, days, rankings, ax=None, verbose=False):
    if not ax:
        ax = plt.gca()
    bins = bin_range([-1 * days.max(), days.max()], 5)
    pal = sns.hls_palette(len(rankings), h=0.5)
    no_changes = []
    for i, (name, scores) in enumerate(rankings):
        crit_diff = get_days_earlier(y_true, days, scores)
        abs_sum = np.abs(crit_diff).sum()
        if abs_sum > 0:
            sns.distplot(
                crit_diff, kde=False, label=name, color=pal[i], bins=bins, ax=ax
            )
            ax.axvline(crit_diff.mean(), color=pal[i], linestyle="--")
        else:
            no_changes.append(name)
    ax.set_xlabel("Days Earlier")
    ax.set_ylabel("Frequency")
    ax.set_title("Change in Days to Find Critical Violations")
    ax.legend()
    if verbose:
        note = "Note: {} led to no changes in detection of critical violations."
        for name in no_changes:
            print(note.format(name))


def compare_stats(y_true, days, rankings):
    rows = []
    for i, (name, scores) in enumerate(rankings):
        crit_diff = get_days_earlier(y_true, days, scores)
        row = {}
        row["Model"] = name
        row["Mean Change"] = crit_diff.mean()
        row["Std. Change"] = crit_diff.std()
        row["First Half"] = get_first_half_proportion(y_true, scores)
        rows.append(row)
    cols = ["Model", "First Half", "Mean Change", "Std. Change"]
    df = pd.DataFrame(rows)
    return df[cols]


def compare_metrics(y_true, days, models):
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 5))
    fig.set_figwidth(15)
    compare_cumulative(y_true, days, models, ax0)
    compare_days_earlier(y_true, days, models, ax1)
    plt.show()
    df = compare_stats(y_true, days, models)
    order = ["First Half", "Mean Change", "Std. Change"]
    asc = [False, False, True]
    return df.sort_values(by=order, ascending=asc).round(3)


def show_metrics(y_true, days, y_scores, name="Model"):
    return compare_metrics(y_true, days, [(name, y_scores)])
