"""
Evaluation utilities for binary classification model performance.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import cross_validate, StratifiedKFold


def evaluate_model(y_true, y_pred, y_proba=None, target_names=None):
    """Compute standard binary classification metrics.

    Parameters
    ----------
    y_true : array-like
        Ground-truth labels (0/1).
    y_pred : array-like
        Predicted labels (0/1).
    y_proba : array-like, optional
        Predicted probabilities for the positive class. If provided,
        ROC-AUC is included in the results.
    target_names : list[str], optional
        Class names for the classification report.
        Defaults to ["No Apnea", "Apnea"].

    Returns
    -------
    dict
        Dictionary with keys: accuracy, precision, recall, f1,
        roc_auc (if y_proba given), classification_report (str),
        and confusion_matrix (ndarray).
    """
    if target_names is None:
        target_names = ["No Apnea", "Apnea"]

    results = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "confusion_matrix": confusion_matrix(y_true, y_pred),
        "classification_report": classification_report(
            y_true, y_pred, target_names=target_names, zero_division=0
        ),
    }

    if y_proba is not None:
        results["roc_auc"] = roc_auc_score(y_true, y_proba)

    return results


def print_evaluation(results):
    """Pretty-print the output of ``evaluate_model``.

    Parameters
    ----------
    results : dict
        Dictionary returned by ``evaluate_model``.
    """
    print("Classification Report:")
    print(results["classification_report"])
    print("Confusion Matrix:")
    print(results["confusion_matrix"])
    print(f"\nAccuracy:  {results['accuracy']:.4f}")
    print(f"Precision: {results['precision']:.4f}")
    print(f"Recall:    {results['recall']:.4f}")
    print(f"F1 Score:  {results['f1']:.4f}")
    if "roc_auc" in results:
        print(f"ROC AUC:   {results['roc_auc']:.4f}")


def cross_val_evaluate(model, X, y, cv=5, scoring=None, random_state=42):
    """Run stratified cross-validation and return a summary DataFrame.

    Parameters
    ----------
    model : estimator
        A scikit-learn compatible classifier.
    X : array-like
        Feature matrix.
    y : array-like
        Target vector.
    cv : int, default 5
        Number of cross-validation folds.
    scoring : list[str], optional
        Metrics to evaluate. Defaults to accuracy, precision, recall,
        f1, and roc_auc.
    random_state : int, default 42
        Random seed for reproducible folds.

    Returns
    -------
    pd.DataFrame
        One row per metric with mean and std columns.
    """
    if scoring is None:
        scoring = ["accuracy", "precision", "recall", "f1", "roc_auc"]

    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=random_state)
    cv_results = cross_validate(model, X, y, cv=skf, scoring=scoring)

    summary = {}
    for metric in scoring:
        key = f"test_{metric}"
        summary[metric] = {
            "mean": cv_results[key].mean(),
            "std": cv_results[key].std(),
        }

    return pd.DataFrame(summary).T


def compare_models(models, X_test, y_test, y_probas=None):
    """Compare multiple models on the same test set.

    Parameters
    ----------
    models : dict[str, estimator]
        Mapping of model name to fitted estimator.
    X_test : array-like
        Test feature matrix.
    y_test : array-like
        Test target vector.
    y_probas : dict[str, array-like], optional
        Mapping of model name to predicted probabilities.
        If not provided, ``predict_proba`` is called on each model.

    Returns
    -------
    pd.DataFrame
        Comparison table with one row per model and metric columns.
    """
    rows = []
    for name, model in models.items():
        y_pred = model.predict(X_test)
        if y_probas and name in y_probas:
            proba = y_probas[name]
        elif hasattr(model, "predict_proba"):
            proba = model.predict_proba(X_test)[:, 1]
        else:
            proba = None

        row = {
            "model": name,
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1": f1_score(y_test, y_pred, zero_division=0),
        }
        if proba is not None:
            row["roc_auc"] = roc_auc_score(y_test, proba)
        rows.append(row)

    return pd.DataFrame(rows).set_index("model")


def threshold_analysis(y_true, y_proba, thresholds=None):
    """Evaluate metrics across different decision thresholds.

    Parameters
    ----------
    y_true : array-like
        Ground-truth labels.
    y_proba : array-like
        Predicted probabilities for the positive class.
    thresholds : array-like, optional
        Thresholds to evaluate. Defaults to 0.1–0.9 in steps of 0.05.

    Returns
    -------
    pd.DataFrame
        Metrics (precision, recall, f1, accuracy) at each threshold.
    """
    if thresholds is None:
        thresholds = np.arange(0.1, 0.91, 0.05)

    rows = []
    for t in thresholds:
        y_pred = (np.asarray(y_proba) >= t).astype(int)
        rows.append(
            {
                "threshold": round(t, 3),
                "accuracy": accuracy_score(y_true, y_pred),
                "precision": precision_score(y_true, y_pred, zero_division=0),
                "recall": recall_score(y_true, y_pred, zero_division=0),
                "f1": f1_score(y_true, y_pred, zero_division=0),
            }
        )

    return pd.DataFrame(rows)
