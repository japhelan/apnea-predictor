"""CFA fit-index utilities.

Provides numerically stable computations of RMSEA, CFI, SRMR, and the
Satorra-Bentler scale factor for a fitted ConfirmatoryFactorAnalyzer.
"""

from __future__ import annotations

import numpy as np


def cfa_fit_indices(cfa) -> dict:
    """Compute global fit indices for a fitted ConfirmatoryFactorAnalyzer.

    Parameters
    ----------
    cfa : ConfirmatoryFactorAnalyzer
        A fitted factor_analyzer.ConfirmatoryFactorAnalyzer instance.

    Returns
    -------
    dict
        Keys: chi2, df, chi2_null, df_null, n_obs, n_vars, n_free,
              rmsea, cfi, srmr, R_obs, R_mod, R_res, lt_i, lt_j.
    """
    S = cfa.cov_
    Sigma = cfa.get_model_implied_cov()
    n = cfa.n_obs
    p = S.shape[0]

    # ML discrepancy function: F = log|Σ| − log|S| + tr(Σ⁻¹ S) − p
    _, ld_S = np.linalg.slogdet(S)
    _, ld_Sig = np.linalg.slogdet(Sigma)
    F_ml = ld_Sig - ld_S + np.trace(np.linalg.inv(Sigma) @ S) - p
    chi2 = n * F_ml

    # Degrees of freedom: data moments − free parameters
    n_free = (
        len(cfa.model.loadings_free)
        + len(cfa.model.error_vars_free)
        + len(cfa.model.factor_covs_free)
    )
    df = p * (p + 1) // 2 - n_free

    # Null (independence) model: Σ_null = diag(S), free params = p variances
    logdet_diag_S = np.sum(np.log(np.diag(S)))
    chi2_null = n * (logdet_diag_S - ld_S)
    df_null = p * (p - 1) // 2

    # RMSEA
    rmsea = float(np.sqrt(max(chi2 - df, 0.0) / (n * df)))

    # CFI (Bentler 1990): noncentrality-based incremental fit
    cfi = float(
        np.clip(
            1.0 - max(chi2 - df, 0.0) / max(chi2_null - df_null, 1e-10),
            0.0,
            1.0,
        )
    )

    # SRMR: standardised residual correlations (lower triangle incl. diagonal)
    D = np.diag(1.0 / np.sqrt(np.diag(S)))
    R_obs = D @ S @ D
    R_mod = D @ Sigma @ D
    R_res = R_obs - R_mod
    lt_i, lt_j = np.tril_indices(p, k=0)
    srmr = float(np.sqrt(np.mean(R_res[lt_i, lt_j] ** 2)))

    return {
        "chi2": chi2,
        "df": df,
        "chi2_null": chi2_null,
        "df_null": df_null,
        "n_obs": n,
        "n_vars": p,
        "n_free": n_free,
        "rmsea": rmsea,
        "cfi": cfi,
        "srmr": srmr,
        "R_obs": R_obs,
        "R_mod": R_mod,
        "R_res": R_res,
        "lt_i": lt_i,
        "lt_j": lt_j,
    }


def mardia_sb_scale(X: np.ndarray) -> float:
    """Compute the Satorra-Bentler scale factor from Mardia's multivariate kurtosis.

    Parameters
    ----------
    X : np.ndarray, shape (n, p)
        Data matrix (centred or uncentred; centering is applied internally).

    Returns
    -------
    float
        SB scale factor c = kappa_M / (p*(p+2)).
        A value near 1.0 indicates multivariate kurtosis consistent with
        normality; values > 1 indicate the ML chi2 is inflated.
    """
    n, p = X.shape
    Xc = X - X.mean(axis=0)
    S = np.cov(Xc, rowvar=False, ddof=0)
    Sinv = np.linalg.inv(S)
    # Squared Mahalanobis distances: delta_i = x_i^T S^{-1} x_i
    # Computed without building the full n×n distance matrix.
    delta = ((Xc @ Sinv) * Xc).sum(axis=1)  # (n,)
    kappa = float((delta**2).sum()) / n
    return kappa / (p * (p + 2))


def print_fit_indices(indices: dict, label: str = "") -> None:
    """Pretty-print CFA global fit indices.

    Parameters
    ----------
    indices : dict
        Dictionary returned by ``cfa_fit_indices``.
    label : str, optional
        Descriptive label appended to the header.
    """
    header = f"CFA Global Fit Indices{' — ' + label if label else ''}"
    print(header)
    print("=" * max(len(header) + 4, 50))
    n = indices["n_obs"]
    p = indices["n_vars"]
    df = indices["df"]
    n_free = indices["n_free"]
    chi2 = indices["chi2"]
    print(f"  χ²({df:>5d}) = {chi2:>10.2f}   (χ²/df = {chi2 / df:.2f})")
    print(f"  RMSEA      = {indices['rmsea']:.4f}   (good ≤ 0.06, acceptable ≤ 0.08)")
    print(f"  CFI        = {indices['cfi']:.4f}   (good ≥ 0.95)")
    print(f"  SRMR       = {indices['srmr']:.4f}   (good ≤ 0.08)")
    print(f"\n  n_obs = {n}   p = {p}   df = {df}   n_free = {n_free}")
