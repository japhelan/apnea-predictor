"""Tests for Stage 2: feature_encoder.encode_features."""

import pandas as pd
import numpy as np
import pytest


# ═══════════════════════════════════════════════════════════════════════════════
# End-to-end output checks
# ═══════════════════════════════════════════════════════════════════════════════


class TestEncodeOutput:
    """Verify the overall shape and properties of Stage 2 output."""

    def test_returns_dataframe(self, encoded_df):
        assert isinstance(encoded_df, pd.DataFrame)

    def test_row_count(self, encoded_df):
        """1880 raw rows → 1687 after dropping missing AHI."""
        assert encoded_df.shape[0] == 1687

    def test_column_count(self, encoded_df):
        """~147 factor cols + ahi + 2 OHE dream recall = 149 (with eating_impact_alertness deduplicated)."""
        assert encoded_df.shape[1] == 149

    def test_flat_columns(self, encoded_df):
        """Columns should be plain strings, not tuples."""
        for c in encoded_df.columns:
            assert isinstance(c, str)

    def test_no_multiindex(self, encoded_df):
        assert not isinstance(encoded_df.columns, pd.MultiIndex)

    def test_all_numeric_dtypes(self, encoded_df):
        for col in encoded_df.columns:
            assert pd.api.types.is_numeric_dtype(
                encoded_df[col]
            ), f"Column '{col}' has non-numeric dtype: {encoded_df[col].dtype}"

    def test_no_nulls_after_imputation(self, encoded_df):
        total_nulls = encoded_df.isnull().sum().sum()
        assert total_nulls == 0

    def test_no_placeholder_values(self, encoded_df):
        """Placeholder values -55 and -66 should have been removed."""
        for col in encoded_df.columns:
            vals = encoded_df[col]
            assert -55 not in vals.values, f"Column '{col}' still contains -55"
            assert -66 not in vals.values, f"Column '{col}' still contains -66"

    def test_ahi_column_present(self, encoded_df):
        assert "ahi" in encoded_df.columns


# ═══════════════════════════════════════════════════════════════════════════════
# Encoding correctness
# ═══════════════════════════════════════════════════════════════════════════════


class TestSexEncoding:
    def test_sex_is_binary(self, encoded_df):
        assert set(encoded_df["sex"].unique()).issubset({0.0, 1.0})


class TestExerciseEncoding:
    def test_exercise_is_binary(self, encoded_df):
        assert set(encoded_df["exercise_amt_or_time"].dropna().unique()).issubset(
            {0.0, 1.0}
        )


class TestNapEncoding:
    def test_nap_col_renamed(self, encoded_df):
        assert "frequent_naps" in encoded_df.columns
        assert "nap_num" not in encoded_df.columns

    def test_nap_is_binary(self, encoded_df):
        assert set(encoded_df["frequent_naps"].unique()).issubset({0.0, 1.0})


class TestDaytimeSleepinessEncoding:
    def test_sleepiness_col_renamed(self, encoded_df):
        assert "frequent_daytime_sleepiness" in encoded_df.columns
        assert (
            "difficulty_staying_awake_during_the_day_number_of_times"
            not in encoded_df.columns
        )

    def test_sleepiness_is_binary(self, encoded_df):
        assert set(encoded_df["frequent_daytime_sleepiness"].unique()).issubset(
            {0.0, 1.0}
        )


class TestDreamRecallEncoding:
    def test_ohe_columns_present(self, encoded_df):
        assert "dream_recall_frequency_infrequent" in encoded_df.columns
        assert "dream_recall_frequency_rarely_or_never" in encoded_df.columns

    def test_original_column_dropped(self, encoded_df):
        assert "dream_recall_frequency" not in encoded_df.columns
        assert "remember_dreams_times" not in encoded_df.columns

    def test_ohe_values_binary(self, encoded_df):
        for col in [
            "dream_recall_frequency_infrequent",
            "dream_recall_frequency_rarely_or_never",
        ]:
            assert set(encoded_df[col].unique()).issubset({0.0, 1.0})


class TestBooleanConversion:
    def test_never_smoked_is_int(self, encoded_df):
        assert pd.api.types.is_numeric_dtype(encoded_df["never_smoked"])
        assert set(encoded_df["never_smoked"].unique()).issubset({0.0, 1.0})

    def test_never_feel_rested_is_int(self, encoded_df):
        assert pd.api.types.is_numeric_dtype(encoded_df["never_feel_rested"])
        assert set(encoded_df["never_feel_rested"].unique()).issubset({0.0, 1.0})

    def test_mdhx_bools_are_numeric(self, encoded_df):
        mdhx_cols = [c for c in encoded_df.columns if c.endswith("_mdhx")]
        for col in mdhx_cols:
            assert pd.api.types.is_numeric_dtype(
                encoded_df[col]
            ), f"mdhx column '{col}' is not numeric"


# ═══════════════════════════════════════════════════════════════════════════════
# Key columns presence
# ═══════════════════════════════════════════════════════════════════════════════


class TestExpectedColumns:
    """Spot-check that key columns made it through the pipeline."""

    @pytest.mark.parametrize(
        "col",
        [
            "age",
            "bmi",
            "sex",
            "sw_9am_start_diff",
            "sw_5pm_end_diff",
            "exercise_amt_or_time",
            "daily_caffeine_servings",
            "never_smoked",
            "ess_total_score",
            "isi_total_score",
            "map_score",
            "rmeq_total_score",
            "ahi",
        ],
    )
    def test_column_present(self, encoded_df, col):
        assert col in encoded_df.columns

    def test_no_duplicate_columns(self, encoded_df):
        assert len(encoded_df.columns) == len(set(encoded_df.columns))


# ═══════════════════════════════════════════════════════════════════════════════
# Unit tests for internal helpers (using small synthetic data)
# ═══════════════════════════════════════════════════════════════════════════════


class TestTimeDiffInHours:
    def test_same_time(self):
        from src.features.feature_encoder import _time_diff_in_hours

        assert _time_diff_in_hours("09:00:00", "09:00:00") == 0.0

    def test_one_hour_later(self):
        from src.features.feature_encoder import _time_diff_in_hours

        assert _time_diff_in_hours("10:00:00", "09:00:00") == 1.0

    def test_half_hour_before(self):
        from src.features.feature_encoder import _time_diff_in_hours

        assert _time_diff_in_hours("08:30:00", "09:00:00") == -0.5


class TestMergeExercise:
    def test_rarely_or_never_applied(self):
        from src.features.feature_encoder import _merge_exercise

        df = pd.DataFrame(
            {
                "exercise_rarely_or_never": [True, False, True],
                "exercise_time_of_day": [np.nan, 0, np.nan],
            }
        )
        result = _merge_exercise(df)
        assert "exercise_amt_or_time" in result.columns
        assert "exercise_time_of_day" not in result.columns
        assert result["exercise_amt_or_time"].iloc[0] == "rarely_or_never"
        assert result["exercise_amt_or_time"].iloc[1] == "early morning"


class TestMergeCaffeine:
    def test_rarely_sets_zero(self):
        from src.features.feature_encoder import _merge_caffeine

        df = pd.DataFrame(
            {
                "caffeine_consumption_rarely_or_never": [True, False],
                "daily_caffeine_servings": [3.0, 2.0],
            }
        )
        result = _merge_caffeine(df)
        assert result["daily_caffeine_servings"].iloc[0] == 0
        assert result["daily_caffeine_servings"].iloc[1] == 2.0
        assert "caffeine_consumption_rarely_or_never" not in result.columns


class TestMergeNaps:
    def test_nap_merge(self):
        from src.features.feature_encoder import _merge_naps

        df = pd.DataFrame({"nap_num": [2, 3], "nap_freq_period": [0, 1]})
        result = _merge_naps(df)
        assert result["nap_num"].iloc[0] == "2 per week"
        assert result["nap_num"].iloc[1] == "3 per month"


class TestReplacePlaceholders:
    def test_replaces_neg55_and_neg66(self):
        from src.features.feature_encoder import _replace_placeholders

        df = pd.DataFrame(
            {
                "slp_quality_sw": [-66, 3, 4],
                "feel_sleep_not_sound_isq": [-55, 2, 1],
                "feel_sleep_unrefreshing_isq": [3, -55, 1],
            }
        )
        result = _replace_placeholders(df)
        assert pd.isna(result["slp_quality_sw"].iloc[0])
        assert result["slp_quality_sw"].iloc[1] == 3
        assert pd.isna(result["feel_sleep_not_sound_isq"].iloc[0])
        assert pd.isna(result["feel_sleep_unrefreshing_isq"].iloc[1])


class TestFlattenMultiindex:
    def test_collapses_tuples_to_strings(self):
        from src.features.feature_encoder import _flatten_multiindex

        idx = pd.MultiIndex.from_tuples(
            [
                ("participants_age", "modified_dem_0110", "demographics"),
                ("participants_sex", "dem_0500", "demographics"),
            ],
            names=["descriptive", "original", "subset"],
        )
        df = pd.DataFrame([[25, "M"], [30, "F"]], columns=idx)
        result = _flatten_multiindex(df)
        assert list(result.columns) == ["age", "sex"]
        assert not isinstance(result.columns, pd.MultiIndex)
