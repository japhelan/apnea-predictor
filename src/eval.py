"""
Evaluation utilities for binary and multiclass classification model performance.
"""

import re

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


# ── notebook-style comparison helpers ────────────────────────────────────────

_MC_NAMES_DEFAULT = ["none", "mild", "moderate", "severe"]


def evaluate_binary(
    name: str,
    y_true,
    y_pred,
    y_proba,
    threshold: float = 0.5,
) -> dict:
    """Compute binary metrics, print a tidy summary, and return a result row.

    Parameters
    ----------
    name : str
        Model label used in the printed header and returned dict.
    y_true, y_pred : array-like
        Ground-truth and predicted labels (0/1).
    y_proba : array-like of shape (n,) or (n, 2)
        Predicted probabilities. If 2-D, column 1 is used.
    threshold : float, default 0.5
        Decision threshold stored in the returned dict (not used for prediction).

    Returns
    -------
    dict
        Keys: model, roc_auc, accuracy, f1_macro, threshold.
    """
    proba_pos = np.asarray(y_proba)
    if proba_pos.ndim == 2:
        proba_pos = proba_pos[:, 1]
    auc = roc_auc_score(y_true, proba_pos)
    acc = accuracy_score(y_true, y_pred)
    f1m = f1_score(y_true, y_pred, average="macro", zero_division=0)
    print(f"\n{'─' * 58}")
    print(f"  {name}")
    print(f"{'─' * 58}")
    print(
        f"  ROC-AUC : {auc:.4f}  |  Accuracy : {acc:.4f}"
        f"  |  F1-macro : {f1m:.4f}  (thresh={threshold:.2f})"
    )
    print(
        classification_report(
            y_true, y_pred, target_names=["no_apnea", "apnea"], zero_division=0
        )
    )
    return {
        "model": name,
        "roc_auc": round(float(auc), 4),
        "accuracy": round(float(acc), 4),
        "f1_macro": round(float(f1m), 4),
        "threshold": threshold,
    }


def evaluate_multiclass(
    name: str,
    y_true,
    y_pred,
    y_proba,
    class_names: list | None = None,
) -> dict:
    """Compute multiclass metrics, print a summary, and return a result row.

    Parameters
    ----------
    name : str
        Model label.
    y_true, y_pred : array-like
        Ground-truth and predicted labels.
    y_proba : array-like of shape (n, n_classes)
        Per-class predicted probabilities.
    class_names : list[str], optional
        Display names for the classification report.
        Defaults to ["none", "mild", "moderate", "severe"].

    Returns
    -------
    dict
        Keys: model, roc_auc_ovr, accuracy, f1_macro.
    """
    if class_names is None:
        class_names = _MC_NAMES_DEFAULT
    auc = roc_auc_score(y_true, y_proba, multi_class="ovr", average="macro")
    acc = accuracy_score(y_true, y_pred)
    f1m = f1_score(y_true, y_pred, average="macro", zero_division=0)
    print(f"\n{'─' * 58}")
    print(f"  {name}")
    print(f"{'─' * 58}")
    print(f"  ROC-AUC(OvR/macro): {auc:.4f}  |  Acc: {acc:.4f}  |  F1-macro: {f1m:.4f}")
    print(
        classification_report(y_true, y_pred, target_names=class_names, zero_division=0)
    )
    return {
        "model": name,
        "roc_auc_ovr": round(float(auc), 4),
        "accuracy": round(float(acc), 4),
        "f1_macro": round(float(f1m), 4),
    }


def safe_mlflow_key(name: str) -> str:
    """Sanitize a string for use as an MLflow metric or param key.

    Strips characters disallowed by MLflow and replaces spaces with underscores.
    """
    return re.sub(r"[^a-zA-Z0-9_\-\. /]", "", name).replace(" ", "_")


def tag_comparison_df(
    df: pd.DataFrame,
    approach: str,
    auc_col: str = "roc_auc",
) -> pd.DataFrame:
    """Normalize a results DataFrame for the cross-approach summary.

    Parameters
    ----------
    df : pd.DataFrame
        Per-model results with at least columns: model, <auc_col>, accuracy, f1_macro.
    approach : str
        Approach label inserted as the first column.
    auc_col : str, default "roc_auc"
        Column to rename to "roc_auc" in the output.

    Returns
    -------
    pd.DataFrame
        Columns: approach, model, roc_auc, accuracy, f1_macro.
    """
    out = df[["model", auc_col, "accuracy", "f1_macro"]].copy()
    out = out.rename(columns={auc_col: "roc_auc"})
    out.insert(0, "approach", approach)
    return out


def run_fa_shap_eval(
    pipeline,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train,
    y_test,
    run_name: str,
    extra_params: dict | None = None,
) -> dict:
    """Fit an FA + tree pipeline, compute SHAP values, and log results to MLflow.

    Assumes the pipeline has a ``Factor_Analyzer_Transformer`` as its first step
    and a tree-based classifier (e.g. XGBClassifier) as its last step.

    Parameters
    ----------
    pipeline : sklearn.pipeline.Pipeline
        Unfitted pipeline to fit on *X_train / y_train*.
    X_train, X_test : pd.DataFrame
        Feature matrices (no target column).
    y_train, y_test : array-like
        Binary (or multiclass) target vectors.
    run_name : str
        MLflow run name.
    extra_params : dict, optional
        Additional key-value pairs logged to MLflow with ``log_params``.

    Returns
    -------
    dict
        Keys: roc_auc, accuracy, classification_report (str), confusion_matrix (ndarray).
    """
    import os
    import tempfile

    import matplotlib.pyplot as plt
    import mlflow
    import shap

    fa_step = pipeline.steps[0][1]
    xgb_step = pipeline.steps[-1][1]

    pipeline.fit(X_train, y_train)

    X_bg = X_train.sample(min(200, len(X_train)), random_state=42)
    X_eval = X_test.sample(min(500, len(X_test)), random_state=42)

    X_bg_fa = fa_step.transform(X_bg)
    X_eval_fa = fa_step.transform(X_eval)

    fa_cols = [f"FA_{i + 1}" for i in range(X_eval_fa.shape[1])]

    explainer = shap.TreeExplainer(xgb_step)
    shap_values = explainer.shap_values(X_eval_fa)

    if isinstance(shap_values, list):
        shap_values_plot = shap_values[1] if len(shap_values) > 1 else shap_values[0]
    else:
        shap_values_plot = shap_values

    preds = pipeline.predict(X_test)
    proba = pipeline.predict_proba(X_test)

    if proba.shape[1] == 2:
        roc_auc = roc_auc_score(y_test, proba[:, 1])
    else:
        roc_auc = roc_auc_score(y_test, proba, multi_class="ovr", average="macro")

    acc = accuracy_score(y_test, preds)
    class_report = classification_report(y_test, preds)
    conf_matrix = confusion_matrix(y_test, preds)

    expected_value = explainer.expected_value
    if isinstance(expected_value, (list, np.ndarray)):
        expected_value = (
            expected_value[1]
            if np.ndim(expected_value) > 0 and len(expected_value) > 1
            else np.ravel(expected_value)[0]
        )

    with mlflow.start_run(run_name=run_name):
        if extra_params:
            mlflow.log_params(extra_params)
        mlflow.log_metric("roc_auc", float(roc_auc))
        mlflow.log_metric("accuracy", float(acc))

        # 1) SHAP summary (beeswarm)
        plt.figure()
        shap.summary_plot(
            shap_values_plot, X_eval_fa, feature_names=fa_cols, show=False
        )
        mlflow.log_figure(plt.gcf(), "shap/summary_beeswarm.png")
        plt.close()

        # 2) SHAP summary (bar importance)
        plt.figure()
        shap.summary_plot(
            shap_values_plot,
            X_eval_fa,
            feature_names=fa_cols,
            plot_type="bar",
            show=False,
        )
        mlflow.log_figure(plt.gcf(), "shap/summary_bar.png")
        plt.close()

        # 3) Force plot for one sample as HTML artifact
        force = shap.force_plot(
            expected_value,
            shap_values_plot[0],
            X_eval_fa.iloc[0],
            feature_names=fa_cols,
            matplotlib=False,
        )
        with tempfile.TemporaryDirectory() as td:
            force_path = os.path.join(td, "force_plot_sample0.html")
            shap.save_html(force_path, force)
            mlflow.log_artifact(force_path, artifact_path="shap")

        mlflow.log_text(class_report, "classification_report.txt")

    print(f"ROC-AUC: {roc_auc:.4f}")
    print(f"Accuracy: {acc:.4f}")
    print(class_report)
    print(conf_matrix)

    return {
        "roc_auc": roc_auc,
        "accuracy": acc,
        "classification_report": class_report,
        "confusion_matrix": conf_matrix,
    }
