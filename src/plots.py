"""
Plotting utilities for binary classification model evaluation.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    PrecisionRecallDisplay,
)
from sklearn.calibration import calibration_curve
from factor_analyzer import FactorAnalyzer


def plot_confusion_matrix(
    y_true, y_pred, labels=None, ax=None, title="Confusion Matrix"
):
    """Display a confusion matrix heatmap.

    Parameters
    ----------
    y_true : array-like
        Ground-truth labels.
    y_pred : array-like
        Predicted labels.
    labels : list[str], optional
        Class display names. Defaults to ["No Apnea", "Apnea"].
    ax : matplotlib.axes.Axes, optional
        Axes to plot on. Created if not provided.
    title : str, default "Confusion Matrix"

    Returns
    -------
    matplotlib.figure.Figure
    """
    if labels is None:
        labels = ["No Apnea", "Apnea"]
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 5))
    else:
        fig = ax.figure

    ConfusionMatrixDisplay.from_predictions(
        y_true, y_pred, display_labels=labels, cmap="Blues", ax=ax
    )
    ax.set_title(title)
    plt.tight_layout()
    return fig


def plot_roc_curve(y_true, y_proba, ax=None, title="ROC Curve", **kwargs):
    """Plot receiver operating characteristic curve.

    Parameters
    ----------
    y_true : array-like
        Ground-truth labels.
    y_proba : array-like
        Predicted probabilities for the positive class.
    ax : matplotlib.axes.Axes, optional
    title : str, default "ROC Curve"

    Returns
    -------
    matplotlib.figure.Figure
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 6))
    else:
        fig = ax.figure

    RocCurveDisplay.from_predictions(y_true, y_proba, ax=ax, **kwargs)
    ax.plot([0, 1], [0, 1], "k--", alpha=0.4, label="Random")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    return fig


def plot_precision_recall_curve(
    y_true, y_proba, ax=None, title="Precision-Recall Curve", **kwargs
):
    """Plot precision-recall curve.

    Parameters
    ----------
    y_true : array-like
        Ground-truth labels.
    y_proba : array-like
        Predicted probabilities for the positive class.
    ax : matplotlib.axes.Axes, optional
        Axes to plot on. Created if not provided.
    title : str, default "Precision-Recall Curve"

    Returns
    -------
    matplotlib.figure.Figure
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 6))
    else:
        fig = ax.figure

    PrecisionRecallDisplay.from_predictions(y_true, y_proba, ax=ax, **kwargs)
    ax.set_title(title)
    plt.tight_layout()
    return fig


def plot_roc_and_pr(y_true, y_proba, title_prefix=""):
    """Plot ROC and Precision-Recall curves side by side.

    Parameters
    ----------
    y_true : array-like
        Ground-truth labels.
    y_proba : array-like
        Predicted probabilities for the positive class.
    title_prefix : str, optional
        Prefix for subplot titles.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    prefix = f"{title_prefix} " if title_prefix else ""
    plot_roc_curve(y_true, y_proba, ax=axes[0], title=f"{prefix}ROC Curve")
    plot_precision_recall_curve(
        y_true, y_proba, ax=axes[1], title=f"{prefix}Precision-Recall Curve"
    )
    plt.tight_layout()
    return fig


def plot_feature_importances(
    model, feature_names=None, top_n=20, ax=None, title="Feature Importances"
):
    """Bar chart of feature importances from a tree-based model.

    Parameters
    ----------
    model : estimator
        A fitted model with a ``feature_importances_`` attribute.
    feature_names : list[str], optional
        Names for each feature. Falls back to integer indices.
    top_n : int, default 20
        Number of top features to display.
    ax : matplotlib.axes.Axes, optional
    title : str, default "Feature Importances"

    Returns
    -------
    matplotlib.figure.Figure
    """
    importances = model.feature_importances_
    if feature_names is None:
        feature_names = [f"Feature {i}" for i in range(len(importances))]

    indices = np.argsort(importances)[::-1][:top_n]

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, max(6, top_n * 0.35)))
    else:
        fig = ax.figure

    ax.barh(
        [feature_names[i] for i in reversed(indices)],
        importances[sorted(indices)],
        color="steelblue",
    )
    ax.set_xlabel("Importance")
    ax.set_title(title)
    plt.tight_layout()
    return fig


def plot_threshold_analysis(threshold_df, ax=None, title="Threshold Analysis"):
    """Line plot of metrics vs. decision threshold.

    Parameters
    ----------
    threshold_df : pd.DataFrame
        Output of ``eval.threshold_analysis`` with a ``threshold`` column
        and metric columns.
    ax : matplotlib.axes.Axes, optional
    title : str, default "Threshold Analysis"

    Returns
    -------
    matplotlib.figure.Figure
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(9, 6))
    else:
        fig = ax.figure

    metrics = [c for c in threshold_df.columns if c != "threshold"]
    for metric in metrics:
        ax.plot(threshold_df["threshold"], threshold_df[metric], label=metric)

    ax.set_xlabel("Decision Threshold")
    ax.set_ylabel("Score")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def plot_calibration_curve(
    y_true, y_proba, n_bins=10, ax=None, title="Calibration Curve"
):
    """Plot a reliability / calibration diagram.

    Parameters
    ----------
    y_true : array-like
        Ground-truth labels.
    y_proba : array-like
        Predicted probabilities for the positive class.
    n_bins : int, default 10
    ax : matplotlib.axes.Axes, optional
    title : str, default "Calibration Curve"

    Returns
    -------
    matplotlib.figure.Figure
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 6))
    else:
        fig = ax.figure

    fraction_pos, mean_predicted = calibration_curve(y_true, y_proba, n_bins=n_bins)
    ax.plot(mean_predicted, fraction_pos, "s-", label="Model")
    ax.plot([0, 1], [0, 1], "k--", alpha=0.4, label="Perfectly calibrated")
    ax.set_xlabel("Mean Predicted Probability")
    ax.set_ylabel("Fraction of Positives")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def plot_model_comparison(comparison_df, ax=None, title="Model Comparison"):
    """Grouped bar chart comparing multiple models across metrics.

    Parameters
    ----------
    comparison_df : pd.DataFrame
        Output of ``eval.compare_models`` with model names as index
        and metric columns.
    ax : matplotlib.axes.Axes, optional
    title : str, default "Model Comparison"

    Returns
    -------
    matplotlib.figure.Figure
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    else:
        fig = ax.figure

    comparison_df.plot(kind="bar", ax=ax, rot=0)
    ax.set_ylabel("Score")
    ax.set_title(title)
    ax.legend(loc="lower right")
    ax.set_ylim(0, 1.05)
    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    return fig


def parallel_analysis(df, n_iterations=100):
    """
    Function to perform parallel analysis and plot the scree plot with observed vs. random eigenvalues.
    pulled from 2.1-jp-feature-engineering notebook, adapted to be a standalone function
    """
    n_obs, n_vars = df.shape

    # Observed eigenvalues from correlation matrix
    fa_all = FactorAnalyzer(rotation=None, n_factors=n_vars, method="principal")
    fa_all.fit(df)
    observed_ev, _ = fa_all.get_eigenvalues()

    # Generate random eigenvalues
    random_evs = np.zeros((n_iterations, n_vars))
    for i in range(n_iterations):
        random_data = np.random.normal(size=(n_obs, n_vars))
        random_corr = np.corrcoef(random_data, rowvar=False)
        random_evs[i, :] = np.sort(np.linalg.eigvalsh(random_corr))[::-1]

    mean_random_ev = random_evs.mean(axis=0)
    p95_random_ev = np.percentile(random_evs, 95, axis=0)

    # Find number of factors where observed > 95th percentile of random
    n_factors_parallel = np.sum(observed_ev > p95_random_ev)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    k = min(30, n_vars)  # plot up to 30 components for readability
    ax.plot(range(1, k + 1), observed_ev[:k], "b-o", label="Observed eigenvalues")
    ax.plot(
        range(1, k + 1), mean_random_ev[:k], "r--^", label="Mean random eigenvalues"
    )
    ax.plot(range(1, k + 1), p95_random_ev[:k], "g--s", label="95th percentile random")
    ax.axhline(
        y=1, color="gray", linestyle=":", alpha=0.5, label="Kaiser criterion (EV=1)"
    )
    ax.axvline(
        x=n_factors_parallel,
        color="purple",
        linestyle="--",
        alpha=0.7,
        label=f"Suggested factors: {n_factors_parallel}",
    )
    ax.set_xlabel("Factor Number")
    ax.set_ylabel("Eigenvalue")
    ax.set_title("Parallel Analysis Scree Plot")
    ax.legend()
    plt.tight_layout()
    plt.show()

    print(f"\nParallel analysis suggests {n_factors_parallel} factors")
