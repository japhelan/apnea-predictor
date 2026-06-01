"""
MLflow helper utilities shared across experiment notebooks.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mlflow
import mlflow.data
import mlflow.sklearn
import shap
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    ConfusionMatrixDisplay,
    f1_score,
    roc_auc_score,
)


def setup_experiment(name, tags, base_tags=None):
    """Create or retrieve an MLflow experiment, set tags, and delete stale runs.

    Parameters
    ----------
    name : str
        Experiment name.
    tags : dict
        Per-experiment tags merged on top of ``base_tags``.
    base_tags : dict, optional
        Notebook-level base tags applied to every experiment.

    Returns
    -------
    mlflow.entities.Experiment
    """
    merged = {**(base_tags or {}), **tags}
    exp = mlflow.set_experiment(name)
    mlflow.set_experiment_tags(merged)
    _client = mlflow.MlflowClient()
    for _run in mlflow.search_runs(experiment_ids=[exp.experiment_id], output_format="list"):
        _client.delete_run(_run.info.run_id)
    mlflow.sklearn.autolog(log_models=False, silent=True)
    return exp


def run_mlflow_trials(trials, model_configs, extra_run_tags=None, log_shap=True):
    """Train each (dataset × model) pair and log results to the active MLflow experiment.

    Parameters
    ----------
    trials : list of tuples
        Each tuple: (name, mlflow_dataset, X_train, X_test, y_train, y_test).
    model_configs : dict
        Mapping of model_name -> (ModelClass, params_dict).
    extra_run_tags : dict, optional
        Additional tags to attach to every run.
    log_shap : bool
        Whether to compute and log SHAP values and bar plot.
    """
    print(f"{'dataset':<25}  {'model':<6}  {'acc':>6}  {'auc':>6}  {'f1':>6}  {'auprc':>6}  {'n_features':>10}")
    print("-" * 78)
    for name, mlflow_ds, X_train, X_test, y_train, y_test in trials:
        for model_name, (ModelClass, params) in model_configs.items():
            tags = {"dataset": name, "model_type": model_name}
            if extra_run_tags:
                tags.update(extra_run_tags)
            with mlflow.start_run(run_name=f"{name}_{model_name}"):
                mlflow.set_tags(tags)
                mlflow.log_input(mlflow_ds, context="training")
                mlflow.log_param("n_features", X_train.shape[1])

                model = ModelClass(**params)
                model.fit(X_train, y_train)

                y_pred = model.predict(X_test)
                y_prob = model.predict_proba(X_test)[:, 1]

                acc   = accuracy_score(y_test, y_pred)
                auc   = roc_auc_score(y_test, y_prob)
                f1    = f1_score(y_test, y_pred)
                auprc = average_precision_score(y_test, y_prob)
                mlflow.log_metrics({"test_accuracy": acc, "test_roc_auc": auc, "test_f1": f1, "test_auprc": auprc})

                if log_shap:
                    explainer = shap.TreeExplainer(model)
                    shap_vals = explainer(X_test)
                    sv = shap_vals[..., 1] if shap_vals.values.ndim == 3 else shap_vals
                    mean_shap = pd.Series(np.abs(sv.values).mean(axis=0), index=X_test.columns)
                    mlflow.log_metrics({f"shap_{col}": float(v) for col, v in mean_shap.items()})
                    shap.plots.bar(sv, max_display=15, show=False)
                    mlflow.log_figure(plt.gcf(), "shap_bar.png")
                    plt.close("all")

                cm_fig, cm_ax = plt.subplots()
                ConfusionMatrixDisplay.from_predictions(y_test, y_pred, ax=cm_ax, colorbar=False)
                cm_ax.set_title(f"{name} — {model_name}")
                mlflow.log_figure(cm_fig, "confusion_matrix.png")
                plt.close(cm_fig)

                print(f"{name:<25}  {model_name:<6}  {acc:>6.3f}  {auc:>6.3f}  {f1:>6.3f}  {auprc:>6.3f}  {X_train.shape[1]:>10}")
