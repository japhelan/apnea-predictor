"""Tests for Stage 1: raw_data_loader.load_and_clean_raw."""

import pandas as pd
import numpy as np


class TestLoadAndCleanRawShape:
    """Verify the overall shape and structure of Stage 1 output."""

    def test_returns_dataframe(self, raw_df):
        assert isinstance(raw_df, pd.DataFrame)

    def test_row_count(self, raw_df):
        assert raw_df.shape[0] == 1880

    def test_column_count(self, raw_df):
        assert raw_df.shape[1] == 409

    def test_no_all_na_rows(self, raw_df):
        assert raw_df.dropna(how="all").shape[0] == raw_df.shape[0]


class TestMultiIndex:
    """Verify the 3-level MultiIndex on columns."""

    def test_multiindex_type(self, raw_df):
        assert isinstance(raw_df.columns, pd.MultiIndex)

    def test_multiindex_levels(self, raw_df):
        assert raw_df.columns.nlevels == 3

    def test_multiindex_names(self, raw_df):
        assert list(raw_df.columns.names) == ["descriptive", "original", "subset"]


class TestSubsets:
    """Verify all expected subsets are present with correct column counts."""

    EXPECTED_SUBSETS = {
        "demographics": 14,
        "medhx": 40,
        "parasomnias": 27,
        "sleep_patterns": 58,
        "health": 90,
        "rls": 18,
        "narc": 39,
        "insomnia": 35,
        "sleep_questions": 68,
        "sleep_treatment": 19,
        "output": 1,
    }

    def test_subset_names(self, raw_df):
        subsets = set(raw_df.columns.get_level_values("subset"))
        assert subsets == set(self.EXPECTED_SUBSETS.keys())

    def test_subset_column_counts(self, raw_df):
        for subset, expected_count in self.EXPECTED_SUBSETS.items():
            actual = raw_df.xs(subset, level="subset", axis=1).shape[1]
            assert (
                actual == expected_count
            ), f"Subset '{subset}': expected {expected_count} cols, got {actual}"


class TestDemographicsEngineering:
    """Verify demographics cleaning and feature engineering."""

    def test_age_column_present(self, raw_df):
        originals = raw_df.columns.get_level_values("original")
        assert "modified_dem_0110" in originals

    def test_age_dtype_numeric(self, raw_df):
        age = raw_df.xs("demographics", level="subset", axis=1)
        age_col = age.xs("modified_dem_0110", level="original", axis=1)
        assert pd.api.types.is_numeric_dtype(age_col.iloc[:, 0])

    def test_bias_columns_removed(self, raw_df):
        """Race, ethnicity, language columns should be dropped."""
        originals = set(raw_df.columns.get_level_values("original"))
        bias_cols = {
            "dem_0900",
            "dem_0910",
            "dem_1000",
            "dem_1010",
            "dem_1100",
            "dem_1120",
        }
        assert bias_cols.isdisjoint(originals)

    def test_ahi_column_present(self, raw_df):
        output = raw_df.xs("output", level="subset", axis=1)
        assert "ahi" in output.columns.get_level_values("original")

    def test_sched_9910_disambiguation(self, raw_df):
        """sched_9910 appears twice — both should be present."""
        originals = list(raw_df.columns.get_level_values("original"))
        assert originals.count("sched_9910") == 2


class TestDatetimeConversions:
    """Verify datetime columns are properly converted."""

    def test_sleep_schedule_datetimes(self, raw_df):
        sleep = raw_df.xs("sleep_patterns", level="subset", axis=1)
        for col_id in ["sched_0900", "sched_1000", "sched_1900", "sched_2000"]:
            if col_id in sleep.columns.get_level_values("original"):
                series = sleep.xs(col_id, level="original", axis=1).iloc[:, 0]
                assert pd.api.types.is_datetime64_any_dtype(
                    series
                ), f"{col_id} should be datetime"
