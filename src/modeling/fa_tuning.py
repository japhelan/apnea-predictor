"""Utilities for tuning factor-analysis rotations with Optuna."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import numpy as np
import optuna
import pandas as pd
from sklearn.metrics import get_scorer_names
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

from src.features.transformers import Factor_Analyzer_Transformer

DEFAULT_ROTATIONS = (
    "varimax",
    "promax",
    "oblimin",
    "oblimax",
    "quartimin",
    "quartimax",
    "equamax",
)

DEFAULT_METHODS = ("minres", "ml", "principal")

DEFAULT_XGB_PARAMS = {
    "n_estimators": 250,
    "max_depth": 4,
    "learning_rate": 0.05,
    "subsample": 0.9,
    "colsample_bytree": 0.9,
    "eval_metric": "logloss",
    "random_state": 42,
}

FA_PARAM_NAMES = {"rotation", "n_factors", "method"}


@dataclass
class FactorAnalysisTuningResult:
    study: optuna.Study
    best_rotation: str | None
    best_method: str | None
    best_score: float
    best_params: dict[str, object]
    trial_results: pd.DataFrame
    rotation_summary: pd.DataFrame


def _normalize_rotation(rotation: str | None) -> str | None:
    if rotation is None:
        return None
    if isinstance(rotation, str) and rotation.lower() == "none":
        return None
    return rotation


def _rotation_label(rotation: str | None) -> str:
    if rotation is None:
        return "none"
    return rotation


def _build_classifier_params(
    classifier_params: dict[str, object] | None,
    random_state: int,
) -> dict[str, object]:
    if classifier_params is None:
        params = DEFAULT_XGB_PARAMS.copy()
        params.update(classifier_params or {})
        params.setdefault("eval_metric", "logloss")
        params["random_state"] = random_state
    else:
        params = classifier_params.copy()
        params["random_state"] = random_state
    return params


def _validate_scoring(scoring: str) -> None:
    if scoring not in get_scorer_names():
        raise ValueError(f"Unsupported scoring metric: {scoring}")


def _build_study(
    rotation_labels: list[str],
    method_labels: list[str],
    n_factors_range: tuple[int, int] | None,
    xgb_search_space: dict[str, object] | None,
    random_state: int,
    direction: str,
) -> optuna.Study:
    if n_factors_range is None and not xgb_search_space:
        grid: dict[str, list[str]] = {
            "rotation": rotation_labels,
            "method": method_labels,
        }
        sampler = optuna.samplers.GridSampler(grid)
    else:
        sampler = optuna.samplers.TPESampler(seed=random_state)
    return optuna.create_study(direction=direction, sampler=sampler)


def _suggest_xgb_param(trial: optuna.Trial, name: str, spec: object) -> object:
    if isinstance(spec, list):
        return trial.suggest_categorical(name, spec)

    if isinstance(spec, tuple) and len(spec) == 2:
        low, high = spec
        if isinstance(low, int) and isinstance(high, int):
            return trial.suggest_int(name, low, high)
        if isinstance(low, (int, float)) and isinstance(high, (int, float)):
            return trial.suggest_float(name, float(low), float(high))

    if isinstance(spec, dict):
        spec_type = spec.get("type")
        if spec_type == "categorical":
            choices = spec.get("choices")
            if not isinstance(choices, list):
                raise ValueError(
                    f"Categorical XGBoost search space for {name} must provide a list of choices"
                )
            return trial.suggest_categorical(name, choices)

        if spec_type == "int":
            low = spec.get("low")
            high = spec.get("high")
            if not isinstance(low, int) or not isinstance(high, int):
                raise ValueError(
                    f"Integer XGBoost search space for {name} must provide integer low/high bounds"
                )
            step = spec.get("step", 1)
            log = bool(spec.get("log", False))
            return trial.suggest_int(name, low, high, step=int(step), log=log)

        if spec_type == "float":
            low = spec.get("low")
            high = spec.get("high")
            if not isinstance(low, (int, float)) or not isinstance(high, (int, float)):
                raise ValueError(
                    f"Float XGBoost search space for {name} must provide numeric low/high bounds"
                )
            step = spec.get("step")
            log = bool(spec.get("log", False))
            if step is None:
                return trial.suggest_float(name, float(low), float(high), log=log)
            return trial.suggest_float(
                name,
                float(low),
                float(high),
                step=float(step),
                log=log,
            )

    raise ValueError(
        f"Unsupported XGBoost search space specification for {name}: {spec!r}"
    )


def _suggest_xgb_params(
    trial: optuna.Trial,
    base_params: dict[str, object],
    xgb_search_space: dict[str, object] | None,
) -> dict[str, object]:
    if not xgb_search_space:
        return base_params

    params = base_params.copy()
    for name, spec in xgb_search_space.items():
        params[name] = _suggest_xgb_param(trial, name, spec)
    return params


def tune_factor_analysis_rotation(
    X: pd.DataFrame,
    y: pd.Series | np.ndarray,
    *,
    rotations: tuple[str | None, ...] | list[str | None] = DEFAULT_ROTATIONS,
    methods: tuple[str, ...] | list[str] = ("minres",),
    n_factors: int = 18,
    n_factors_range: tuple[int, int] | None = None,
    n_trials: int = 30,
    n_splits: int = 5,
    scoring: str = "roc_auc",
    classifier_params: dict[str, object] | None = None,
    xgb_search_space: dict[str, object] | None = None,
    random_state: int = 42,
    direction: str = "maximize",
    show_progress_bar: bool = False,
) -> FactorAnalysisTuningResult:
    """Tune factor-analysis rotations and rank them by cross-validated score.

    When only rotations are tuned, the search uses Optuna's grid sampler so each
    candidate rotation is evaluated exactly once. If ``n_factors_range`` is
    provided, or when ``xgb_search_space`` is supplied, Optuna switches to TPE
    and jointly tunes factor-analysis and XGBoost hyperparameters.
    """

    if n_splits < 2:
        raise ValueError("n_splits must be at least 2")

    if n_factors_range is not None and n_factors_range[0] > n_factors_range[1]:
        raise ValueError(
            "n_factors_range must be ordered as (min_factors, max_factors)"
        )

    _validate_scoring(scoring)

    y_series = pd.Series(y, index=X.index if hasattr(X, "index") else None)
    rotation_lookup = {
        _rotation_label(_normalize_rotation(rotation)): _normalize_rotation(rotation)
        for rotation in rotations
    }
    rotation_labels = list(rotation_lookup.keys())
    method_labels = list(methods)
    classifier_kwargs = _build_classifier_params(classifier_params, random_state)
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    study = _build_study(
        rotation_labels,
        method_labels,
        n_factors_range,
        xgb_search_space,
        random_state,
        direction,
    )

    def objective(trial: optuna.Trial) -> float:
        rotation_label = trial.suggest_categorical("rotation", rotation_labels)
        method = trial.suggest_categorical("method", method_labels)
        candidate_n_factors = n_factors
        if n_factors_range is not None:
            candidate_n_factors = trial.suggest_int(
                "n_factors", n_factors_range[0], n_factors_range[1]
            )
        candidate_classifier_kwargs = _suggest_xgb_params(
            trial,
            classifier_kwargs,
            xgb_search_space,
        )

        pipeline = Pipeline(
            [
                (
                    "factor_analysis",
                    Factor_Analyzer_Transformer(
                        n_factors=candidate_n_factors,
                        rotation=rotation_lookup[rotation_label],
                        method=str(method),
                    ),
                ),
                ("classifier", XGBClassifier(**candidate_classifier_kwargs)),
            ]
        )

        scores = cross_validate(
            pipeline,
            X,
            y_series,
            cv=cv,
            scoring=scoring,
            n_jobs=None,
            return_train_score=False,
        )["test_score"]

        mean_score = float(np.mean(scores))
        trial.set_user_attr("score_std", float(np.std(scores)))
        trial.set_user_attr("score_min", float(np.min(scores)))
        trial.set_user_attr("score_max", float(np.max(scores)))
        return mean_score

    if n_factors_range is None and not xgb_search_space:
        study.optimize(
            objective,
            n_trials=len(rotation_labels) * len(method_labels),
            show_progress_bar=show_progress_bar,
        )
    else:
        study.optimize(
            objective, n_trials=n_trials, show_progress_bar=show_progress_bar
        )

    rows = []
    for trial in study.trials:
        if trial.value is None:
            continue
        row = {
            "trial": trial.number,
            "rotation": trial.params["rotation"],
            "method": trial.params.get("method", method_labels[0]),
            "n_factors": trial.params.get("n_factors", n_factors),
            "mean_score": float(trial.value),
            "score_std": float(trial.user_attrs.get("score_std", np.nan)),
            "score_min": float(trial.user_attrs.get("score_min", np.nan)),
            "score_max": float(trial.user_attrs.get("score_max", np.nan)),
        }
        row.update(
            {
                key: value
                for key, value in trial.params.items()
                if key not in {"rotation", "method", "n_factors"}
            }
        )
        rows.append(row)

    trial_results = pd.DataFrame(rows).sort_values(
        by=["mean_score", "score_std"], ascending=[False, True]
    )
    rotation_summary = (
        trial_results.groupby("rotation", dropna=False)
        .agg(
            best_score=("mean_score", "max"),
            average_score=("mean_score", "mean"),
            average_std=("score_std", "mean"),
            trials=("trial", "count"),
            best_n_factors=("n_factors", "first"),
            best_method=("method", "first"),
        )
        .sort_values(by=["best_score", "average_score"], ascending=[False, False])
        .reset_index()
    )

    best_rotation = _normalize_rotation(study.best_params["rotation"])
    best_method = str(study.best_params.get("method", method_labels[0]))
    best_params = study.best_params.copy()
    best_params["rotation"] = best_rotation
    best_params["method"] = best_method

    return FactorAnalysisTuningResult(
        study=study,
        best_rotation=best_rotation,
        best_method=best_method,
        best_score=float(study.best_value),
        best_params=best_params,
        trial_results=trial_results.reset_index(drop=True),
        rotation_summary=rotation_summary,
    )


def build_best_factor_analysis_pipeline(
    tuning_result: FactorAnalysisTuningResult,
    *,
    classifier_params: dict[str, object] | None = None,
    random_state: int = 42,
) -> Pipeline:
    """Build a pipeline configured with the study's best FA parameters."""

    classifier_kwargs = _build_classifier_params(classifier_params, random_state)
    best_n_factors = tuning_result.best_params.get("n_factors", 18)
    resolved_n_factors = (
        int(best_n_factors) if isinstance(best_n_factors, (int, float, str)) else 18
    )
    tuned_classifier_params = {
        key: value
        for key, value in tuning_result.best_params.items()
        if key not in FA_PARAM_NAMES
    }
    classifier_kwargs.update(tuned_classifier_params)
    return Pipeline(
        [
            (
                "factor_analysis",
                Factor_Analyzer_Transformer(
                    n_factors=resolved_n_factors,
                    rotation=cast(str | None, tuning_result.best_rotation),
                    method=cast(str, tuning_result.best_method or "minres"),
                ),
            ),
            ("classifier", XGBClassifier(**classifier_kwargs)),
        ]
    )
