import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from sklearn.metrics import confusion_matrix
from sklearn.base import clone as sklearn_clone
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_array
from sklearn.metrics import (
    roc_curve,
    roc_auc_score,
    precision_recall_curve,
    average_precision_score,
)
from sklearn import tree as sklearn_tree
from sklearn.externals.six import StringIO
from IPython.display import Image
import pydotplus


def visualize_tree(model, feature_names, class_names, fill_colors):
    dot_data = StringIO()
    sklearn_tree.export_graphviz(
        model, out_file=dot_data, feature_names=feature_names, class_names=class_names
    )
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    leaves = set()
    non_leaves = set()
    for edge in graph.get_edges():
        leaves.add(int(edge.get_destination()))
        non_leaves.add(int(edge.get_source()))
    leaves.difference_update(non_leaves)
    leaves_idx = list(filter(lambda l: type(l) is int, leaves))
    nodes = graph.get_nodes()
    terminal_nodes = [nodes[i + 1] for i in leaves_idx]
    for node in terminal_nodes:
        text = node.get_label()
        if text:
            cls = text[1:-1].split("nclass = ")[1]
            node.set("style", "filled")
            if cls == class_names[0]:
                node.set("fillcolor", fill_colors[0])
            elif cls == class_names[1]:
                node.set("fillcolor", fill_colors[1])
    return Image(graph.create_png())


def show_roc(clf, X_test, y_test):
    y_score = clf.predict_proba(X_test)[:, 1]
    fpr, tpr, roc_t = roc_curve(y_test, y_score)
    print("AUROC = {0:.3f}".format(roc_auc_score(y_test, y_score)))
    sns.lineplot(x=fpr, y=tpr)
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.show()


def show_prc(clf, X_test, y_test):
    y_score = clf.predict_proba(X_test)[:, 1]
    precs, recs, prc_t = precision_recall_curve(y_test, y_score)
    print("AUPRC = {0:.3f}".format(average_precision_score(y_test, y_score)))
    best_f1 = -1
    best_t = 2
    for p, r, t in zip(precs, recs, prc_t):
        f1 = (2 * p * r) / (p + r + 1e-10)
        if f1 > best_f1:
            best_f1 = f1
            best_t = t
    print("Best F1 = {0:.3f} at threshold = {1:.3f}".format(best_f1, best_t))
    sns.lineplot(x=recs, y=precs)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.show()


def evaluate_model(y_true, y_pred, verbose=True, show_proportion=False):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    matrix = [[tp, fn], [fp, tn]]
    zero = 1e-10
    if show_proportion:
        n = tn + fp + fn + tp + zero
        matrix = [[tp / n, fn / n], [fp / n, tn / n]]
    prec = tp / (tp + fp + zero)
    rec = tp / (tp + fn + zero)
    f1 = (2 * prec * rec) / (prec + rec + zero)
    out = ""
    out += "F1 Score = {0:.5f}".format(f1)
    out += "\nPrecision = {0:.5f}".format(prec)
    out += "\nRecall = {0:.5f}".format(rec)
    table = pd.DataFrame(
        matrix, columns=["Predicted +", "Predicted -"], index=["Actual +", "Actual -"]
    )
    if verbose:
        print(out)
        return table
    else:
        return f1, prec, rec, table, (tn, fp, fn, tp)


def rank_models(models, Xt, yt, Xv, yv, predictors, demographics):
    results = []
    clfs = []
    for base_clf in tqdm(models):
        clf = sklearn_clone(base_clf)
        name = type(clf).__name__
        params = str(clf)
        clf.fit(Xt[predictors], yt)
        y_pred = clf.predict(Xv[predictors])
        f1, prec, rec, _, mat = evaluate_model(yv, y_pred, verbose=False)
        tn, fp, fn, tp = mat
        zero = 1e-10
        res = {
            "Model": name,
            "Params": params,
            "F1": f1,
            "Prc": prec,
            "Rec": rec,
            "TN": tn,
            "FP": fp,
            "FN": fn,
            "TP": tp,
        }
        for demo in demographics:
            chosen = (Xv[demo] * y_pred).sum()
            opportunity = "P(I|{})".format(demo)
            res[opportunity] = chosen / (Xv[demo].sum() + zero)
            probability = "P({}|I)".format(demo)
            res[probability] = chosen / (y_pred.sum() + zero)
        clfs.append(clf)
        results.append(res)
    cols = ["Model", "F1", "Prc", "Rec", "TP", "FN", "FP", "TN"]
    for demo in demographics:
        opportunity = "P(I|{})".format(demo)
        probability = "P({}|I)".format(demo)
        cols.append(opportunity)
        cols.append(probability)
    rdf = pd.DataFrame(results)
    return rdf, cols, clfs
