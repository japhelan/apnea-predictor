"""Item Response Theory (IRT) scoring utilities.

Implements EAP (Expected A Posteriori) person scoring for the
Graded Response Model (GRM).
"""

import numpy as np
from scipy.special import expit


def grm_score_eap(data, discrimination, difficulty, n_quad=61):
    """EAP person scoring for a fitted Graded Response Model.

    Parameters
    ----------
    data : np.ndarray of shape (n_items, n_persons)
        0-indexed integer response array.
    discrimination : np.ndarray of shape (n_items,)
        Item discrimination parameters.
    difficulty : np.ndarray of shape (n_items, n_thresholds)
        Item difficulty parameters.
    n_quad : int, default 61
        Number of quadrature points on the theta grid [-4, 4].

    Returns
    -------
    theta_eap : np.ndarray of shape (n_persons,)
        EAP latent trait estimates.
    """
    theta_grid = np.linspace(-4, 4, n_quad)
    n_items, n_persons = data.shape

    # N(0,1) prior over theta grid, normalised to sum to 1
    prior = np.exp(-0.5 * theta_grid ** 2)
    prior /= prior.sum()

    log_lik = np.zeros((n_persons, n_quad))

    for i in range(n_items):
        a = discrimination[i]
        b = difficulty[i]  # (n_thresholds,)

        # P(X >= k | theta): shape (n_thresholds, n_quad)
        p_ge = expit(a * (theta_grid[None, :] - b[:, None]))
        # Boundary rows: P(X >= 0) = 1, P(X >= n_cat) = 0
        p_ge = np.vstack([np.ones((1, n_quad)), p_ge, np.zeros((1, n_quad))])

        # P(X = k | theta) = P(X >= k) - P(X >= k+1): (n_categories, n_quad)
        p_cat = np.clip(p_ge[:-1] - p_ge[1:], 1e-10, 1.0)

        # Accumulate log-likelihood for each person's observed response
        log_lik += np.log(p_cat[data[i, :], :])  # (n_persons, n_quad)

    log_post = log_lik + np.log(prior)
    log_post -= log_post.max(axis=1, keepdims=True)   # numerical stability
    post = np.exp(log_post)
    post /= post.sum(axis=1, keepdims=True)

    return (post * theta_grid).sum(axis=1)
