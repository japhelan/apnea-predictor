"""Shared fixtures for the apnea-predictor test suite."""

import pytest
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def project_root():
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def raw_df(project_root):
    """Load Stage 1 output once for the whole test session."""
    from src.features.raw_data_loader import load_and_clean_raw

    return load_and_clean_raw(project_root)


@pytest.fixture(scope="session")
def encoded_df(raw_df):
    """Load Stage 2 output once for the whole test session."""
    from src.features.feature_encoder import encode_features

    return encode_features(raw_df)
