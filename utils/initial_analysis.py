"""
Initial Dataset Analysis Utilities

This module provides functions for conducting initial exploratory data analysis
on the STAGES dataset and other sleep apnea prediction datasets.
"""

from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def dataset_overview(df: pd.DataFrame, name: str = "Dataset") -> None:
    """
    Provide a comprehensive overview of the dataset structure and basic statistics.

    Parameters:
    -----------
    df : pd.DataFrame
        The dataset to analyze
    name : str
        Name of the dataset for display purposes
    """
    print(f"\n{'='*50}")
    print(f"{name.upper()} OVERVIEW")
    print(f"{'='*50}")

    print("\n📊 Basic Information:")
    print(f"   Shape: {df.shape[0]:,} rows × {df.shape[1]:,} columns")
    print(f"   Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    # Data types summary
    dtype_counts = df.dtypes.value_counts()
    print("\n📋 Data Types:")
    for dtype, count in dtype_counts.items():
        print(f"   {dtype}: {count} columns")

    # Missing data summary
    missing_summary = missing_data_analysis(df, display=False)
    if not missing_summary.empty:
        total_missing_cols = len(missing_summary)
        high_missing_cols = len(
            missing_summary[missing_summary["Missing_Percentage"] > 80]
        )
        print("\n❌ Missing Data:")
        print(f"   Columns with missing data: {total_missing_cols}")
        print(f"   Columns with >80% missing: {high_missing_cols}")

    # Duplicate rows
    duplicates = df.duplicated().sum()
    print("\n🔄 Duplicates:")
    print(f"   Duplicate rows: {duplicates:,}")

    # Numeric vs categorical split
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns
    print("\n🔢 Column Types:")
    print(f"   Numeric columns: {len(numeric_cols)}")
    print(f"   Categorical columns: {len(categorical_cols)}")


def missing_data_analysis(
    df: pd.DataFrame, display: bool = True, threshold: float = 80.0
) -> pd.DataFrame:
    """
    Analyze missing data patterns in the dataset.

    Parameters:
    -----------
    df : pd.DataFrame
        The dataset to analyze
    display : bool
        Whether to display the results
    threshold : float
        Percentage threshold for highlighting high missing columns

    Returns:
    --------
    pd.DataFrame
        Summary of missing data by column
    """
    missing_data = df.isnull().sum()
    missing_data = missing_data[missing_data > 0].sort_values(ascending=False)

    if missing_data.empty:
        if display:
            print("✅ No missing data found!")
        return pd.DataFrame()

    # Calculate percentages
    missing_percent = (missing_data / len(df)) * 100

    # Create summary dataframe
    missing_summary = pd.DataFrame(
        {"Missing_Count": missing_data, "Missing_Percentage": missing_percent}
    )

    if display:
        print(f"\n{'='*50}")
        print("MISSING DATA ANALYSIS")
        print(f"{'='*50}")

        high_missing = missing_summary[
            missing_summary["Missing_Percentage"] > threshold
        ]
        if not high_missing.empty:
            print(f"\n⚠️  Columns with >{threshold}% missing data:")
            print(high_missing.to_string())

        moderate_missing = missing_summary[
            (missing_summary["Missing_Percentage"] <= threshold)
            & (missing_summary["Missing_Percentage"] > 10)
        ]
        if not moderate_missing.empty:
            print(f"\n📊 Columns with 10-{threshold}% missing data:")
            print(moderate_missing.head(10).to_string())

        low_missing = missing_summary[missing_summary["Missing_Percentage"] <= 10]
        if not low_missing.empty:
            print(f"\n✅ Columns with <10% missing data: {len(low_missing)} columns")

    return missing_summary


def plot_missing_data(
    df: pd.DataFrame, max_cols: int = 30, figsize: Tuple[int, int] = (12, 8)
) -> None:
    """
    Create visualizations for missing data patterns.

    Parameters:
    -----------
    df : pd.DataFrame
        The dataset to analyze
    max_cols : int
        Maximum number of columns to display in the plot
    figsize : tuple
        Figure size for matplotlib plots
    """
    missing_data = df.isnull().sum()
    missing_data = missing_data[missing_data > 0].sort_values(ascending=False)

    if missing_data.empty:
        print("✅ No missing data to visualize!")
        return

    # Limit to top missing columns
    missing_data_plot = missing_data.head(max_cols)
    missing_percent = (missing_data_plot / len(df)) * 100

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)

    # Bar plot of missing counts
    ax1.bar(
        range(len(missing_data_plot)),
        missing_data_plot.values,
        color="skyblue",
        alpha=0.7,
    )
    ax1.set_title(
        f"Top {len(missing_data_plot)} Columns by Missing Value Count",
        fontsize=14,
        fontweight="bold",
    )
    ax1.set_ylabel("Missing Value Count")
    ax1.set_xticks(range(len(missing_data_plot)))
    ax1.set_xticklabels(missing_data_plot.index, rotation=45, ha="right")

    # Bar plot of missing percentages
    colors = [
        "red" if x > 80 else "orange" if x > 50 else "yellow" if x > 10 else "green"
        for x in missing_percent
    ]
    ax2.bar(
        range(len(missing_percent)), missing_percent.values, color=colors, alpha=0.7
    )
    ax2.set_title("Missing Value Percentages", fontsize=14, fontweight="bold")
    ax2.set_ylabel("Missing Percentage (%)")
    ax2.set_xticks(range(len(missing_percent)))
    ax2.set_xticklabels(missing_percent.index, rotation=45, ha="right")
    ax2.axhline(y=80, color="red", linestyle="--", alpha=0.5, label="80% threshold")
    ax2.legend()

    plt.tight_layout()
    plt.show()


def distribution_analysis(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    max_cols: int = 10,
    figsize: Tuple[int, int] = (15, 10),
) -> None:
    """
    Analyze and visualize distributions of numeric columns.

    Parameters:
    -----------
    df : pd.DataFrame
        The dataset to analyze
    columns : list, optional
        Specific columns to analyze. If None, uses all numeric columns
    max_cols : int
        Maximum number of columns to plot
    figsize : tuple
        Figure size for the plot
    """
    if columns is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    else:
        numeric_cols = [col for col in columns if col in df.columns]

    # Remove columns with all missing values
    numeric_cols = [col for col in numeric_cols if df[col].notna().sum() > 0]

    if not numeric_cols:
        print("❌ No numeric columns found for distribution analysis!")
        return

    # Limit number of columns to plot
    cols_to_plot = numeric_cols[:max_cols]

    print(f"\n{'='*50}")
    print(f"DISTRIBUTION ANALYSIS - TOP {len(cols_to_plot)} NUMERIC COLUMNS")
    print(f"{'='*50}")

    # Calculate number of rows and columns for subplots
    n_cols = min(3, len(cols_to_plot))
    n_rows = (len(cols_to_plot) + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_rows == 1 and n_cols == 1:
        axes = [axes]
    elif n_rows == 1:
        axes = axes
    else:
        axes = axes.flatten()

    for i, col in enumerate(cols_to_plot):
        data = df[col].dropna()

        if len(data) == 0:
            continue

        ax = axes[i] if len(cols_to_plot) > 1 else axes

        # Create histogram with density curve
        ax.hist(
            data, bins=30, alpha=0.7, color="skyblue", density=True, edgecolor="black"
        )

        # Add density curve if enough data points
        if len(data) > 10:
            try:
                data_sorted = np.sort(data)
                density = stats.gaussian_kde(data)
                ax.plot(data_sorted, density(data_sorted), "r-", linewidth=2)
            except:
                pass

        ax.set_title(
            f"{col}\nMean: {data.mean():.2f}, Std: {data.std():.2f}", fontsize=10
        )
        ax.set_xlabel("Value")
        ax.set_ylabel("Density")

        # Add basic statistics as text
        stats_text = (
            f"Min: {data.min():.2f}\nMax: {data.max():.2f}\nMedian: {data.median():.2f}"
        )
        ax.text(
            0.02,
            0.98,
            stats_text,
            transform=ax.transAxes,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
            fontsize=8,
        )

    # Hide empty subplots
    for i in range(len(cols_to_plot), len(axes)):
        if len(cols_to_plot) > 1:
            axes[i].set_visible(False)

    plt.tight_layout()
    plt.show()


def correlation_analysis(
    df: pd.DataFrame,
    method: str = "pearson",
    threshold: float = 0.5,
    figsize: Tuple[int, int] = (12, 10),
    target_col: Optional[str] = None,
) -> pd.DataFrame:
    """
    Analyze correlations between numeric variables.

    Parameters:
    -----------
    df : pd.DataFrame
        The dataset to analyze
    method : str
        Correlation method ('pearson', 'spearman', 'kendall')
    threshold : float
        Minimum correlation coefficient to highlight
    figsize : tuple
        Figure size for the heatmap
    target_col : str, optional
        Target column for focused correlation analysis

    Returns:
    --------
    pd.DataFrame
        Correlation matrix
    """
    numeric_df = df.select_dtypes(include=[np.number])

    if numeric_df.shape[1] < 2:
        print("❌ Need at least 2 numeric columns for correlation analysis!")
        return pd.DataFrame()

    # Calculate correlation matrix
    corr_matrix = numeric_df.corr(method=method)

    print(f"\n{'='*50}")
    print(f"CORRELATION ANALYSIS ({method.upper()})")
    print(f"{'='*50}")

    # Find high correlations
    high_corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) >= threshold:
                high_corr_pairs.append(
                    {
                        "Variable_1": corr_matrix.columns[i],
                        "Variable_2": corr_matrix.columns[j],
                        "Correlation": corr_val,
                    }
                )

    if high_corr_pairs:
        high_corr_df = pd.DataFrame(high_corr_pairs)
        high_corr_df = high_corr_df.sort_values("Correlation", key=abs, ascending=False)
        print(f"\n🔗 Variable pairs with |correlation| >= {threshold}:")
        print(high_corr_df.to_string(index=False))
    else:
        print(f"\n📊 No variable pairs found with |correlation| >= {threshold}")

    # Create heatmap
    plt.figure(figsize=figsize)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(
        corr_matrix,
        mask=mask,
        annot=True,
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=0.1,
        cbar_kws={"shrink": 0.5},
        fmt=".2f",
    )
    plt.title(
        f"Correlation Matrix ({method.capitalize()})", fontsize=16, fontweight="bold"
    )
    plt.tight_layout()
    plt.show()

    # Target-focused analysis if specified
    if target_col and target_col in corr_matrix.columns:
        target_corr = (
            corr_matrix[target_col].abs().sort_values(ascending=False)[1:]
        )  # Exclude self-correlation
        print(f"\n🎯 Top correlations with '{target_col}':")
        print(target_corr.head(10).to_string())

    return corr_matrix


def categorical_analysis(
    df: pd.DataFrame,
    max_categories: int = 20,
    max_cols: int = 6,
    figsize: Tuple[int, int] = (15, 12),
) -> None:
    """
    Analyze categorical variables in the dataset.

    Parameters:
    -----------
    df : pd.DataFrame
        The dataset to analyze
    max_categories : int
        Maximum number of categories to show per variable
    max_cols : int
        Maximum number of columns to analyze
    figsize : tuple
        Figure size for plots
    """
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    if not categorical_cols:
        print("❌ No categorical columns found!")
        return

    print(f"\n{'='*50}")
    print("CATEGORICAL VARIABLES ANALYSIS")
    print(f"{'='*50}")

    cols_to_analyze = categorical_cols[:max_cols]

    # Summary table
    cat_summary = []
    for col in cols_to_analyze:
        unique_count = df[col].nunique()
        missing_count = df[col].isnull().sum()
        missing_pct = (missing_count / len(df)) * 100

        # Get top categories
        if unique_count <= max_categories:
            top_cats = df[col].value_counts().head(5).to_dict()
        else:
            top_cats = f"{unique_count} unique values"

        cat_summary.append(
            {
                "Column": col,
                "Unique_Values": unique_count,
                "Missing_Count": missing_count,
                "Missing_Pct": f"{missing_pct:.1f}%",
                "Top_Categories": str(top_cats),
            }
        )

    summary_df = pd.DataFrame(cat_summary)
    print("\n📊 Categorical Variables Summary:")
    print(summary_df.to_string(index=False))

    # Create visualizations for columns with reasonable number of categories
    plottable_cols = [
        col for col in cols_to_analyze if df[col].nunique() <= max_categories
    ]

    if plottable_cols:
        n_cols = min(2, len(plottable_cols))
        n_rows = (len(plottable_cols) + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        if n_rows == 1 and n_cols == 1:
            axes = [axes]
        elif n_rows == 1:
            axes = axes
        else:
            axes = axes.flatten()

        for i, col in enumerate(plottable_cols):
            ax = axes[i] if len(plottable_cols) > 1 else axes

            value_counts = df[col].value_counts()
            colors = plt.cm.Set3(np.linspace(0, 1, len(value_counts)))

            bars = ax.bar(
                range(len(value_counts)), value_counts.values, color=colors, alpha=0.8
            )
            ax.set_title(
                f"{col}\n({len(value_counts)} categories)",
                fontsize=12,
                fontweight="bold",
            )
            ax.set_xlabel("Categories")
            ax.set_ylabel("Count")
            ax.set_xticks(range(len(value_counts)))
            ax.set_xticklabels(value_counts.index, rotation=45, ha="right")

            # Add value labels on bars
            for bar, value in zip(bars, value_counts.values):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + value * 0.01,
                    f"{value}",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                )

        # Hide empty subplots
        for i in range(len(plottable_cols), len(axes)):
            if len(plottable_cols) > 1:
                axes[i].set_visible(False)

        plt.tight_layout()
        plt.show()


def outlier_detection(
    df: pd.DataFrame,
    method: str = "iqr",
    columns: Optional[List[str]] = None,
    threshold: float = 1.5,
    display_top: int = 10,
) -> Dict[str, pd.Series]:
    """
    Detect outliers in numeric columns using various methods.

    Parameters:
    -----------
    df : pd.DataFrame
        The dataset to analyze
    method : str
        Method for outlier detection ('iqr', 'zscore', 'modified_zscore')
    columns : list, optional
        Specific columns to analyze
    threshold : float
        Threshold for outlier detection (1.5 for IQR, 3 for z-score)
    display_top : int
        Number of top outlier columns to display

    Returns:
    --------
    dict
        Dictionary with outlier indices for each column
    """
    if columns is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    else:
        numeric_cols = [
            col
            for col in columns
            if col in df.columns and df[col].dtype in ["int64", "float64"]
        ]

    if not numeric_cols:
        print("❌ No numeric columns found for outlier detection!")
        return {}

    print(f"\n{'='*50}")
    print(f"OUTLIER DETECTION ({method.upper()} METHOD)")
    print(f"{'='*50}")

    outliers_dict = {}
    outlier_summary = []

    for col in numeric_cols:
        data = df[col].dropna()
        if len(data) == 0:
            continue

        if method == "iqr":
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            outliers = data[(data < lower_bound) | (data > upper_bound)]

        elif method == "zscore":
            z_scores = np.abs((data - data.mean()) / data.std())
            outliers = data[z_scores > threshold]

        elif method == "modified_zscore":
            median = data.median()
            mad = np.median(np.abs(data - median))
            modified_z_scores = 0.6745 * (data - median) / mad
            outliers = data[np.abs(modified_z_scores) > threshold]

        else:
            raise ValueError("Method must be 'iqr', 'zscore', or 'modified_zscore'")

        outliers_dict[col] = outliers
        outlier_pct = (len(outliers) / len(data)) * 100

        outlier_summary.append(
            {
                "Column": col,
                "Outlier_Count": len(outliers),
                "Outlier_Percentage": f"{outlier_pct:.2f}%",
                "Data_Points": len(data),
            }
        )

    # Sort by outlier count and display top results
    summary_df = pd.DataFrame(outlier_summary)
    summary_df["Outlier_Count_Numeric"] = summary_df["Outlier_Count"]
    summary_df_sorted = summary_df.sort_values("Outlier_Count_Numeric", ascending=False)

    print(f"\n📊 Outlier Summary (Top {display_top}):")
    print(
        summary_df_sorted.drop("Outlier_Count_Numeric", axis=1)
        .head(display_top)
        .to_string(index=False)
    )

    return outliers_dict


def generate_data_quality_report(df: pd.DataFrame, name: str = "Dataset") -> None:
    """
    Generate a comprehensive data quality report.

    Parameters:
    -----------
    df : pd.DataFrame
        The dataset to analyze
    name : str
        Name of the dataset for the report
    """
    print(f"\n{'='*60}")
    print(f"DATA QUALITY REPORT: {name.upper()}")
    print(f"{'='*60}")

    # Basic overview
    dataset_overview(df, name)

    # Data quality checks
    print("\n🔍 DATA QUALITY CHECKS:")

    # Check for completely empty rows
    empty_rows = df.isnull().all(axis=1).sum()
    print(f"   Empty rows: {empty_rows}")

    # Check for constant columns (all values the same)
    constant_cols = []
    for col in df.columns:
        unique_vals = df[col].nunique()
        if unique_vals <= 1:
            constant_cols.append(col)

    print(f"   Constant/single-value columns: {len(constant_cols)}")
    if constant_cols and len(constant_cols) <= 10:
        print(f"     {constant_cols}")

    # Check for high cardinality categorical columns
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns
    high_cardinality = []
    for col in categorical_cols:
        cardinality_ratio = df[col].nunique() / len(df)
        if cardinality_ratio > 0.8:  # More than 80% unique values
            high_cardinality.append(
                (col, df[col].nunique(), f"{cardinality_ratio:.2%}")
            )

    if high_cardinality:
        print(f"   High cardinality categorical columns: {len(high_cardinality)}")
        for col, unique_count, ratio in high_cardinality[:5]:
            print(f"     {col}: {unique_count} unique ({ratio})")

    # Memory usage insights
    memory_usage = df.memory_usage(deep=True) / 1024**2  # MB
    largest_cols = memory_usage.nlargest(5)
    print("\n💾 MEMORY USAGE:")
    print(f"   Total: {memory_usage.sum():.2f} MB")
    print("   Largest columns:")
    for col, size in largest_cols.items():
        if col != "Index":
            print(f"     {col}: {size:.2f} MB")

    print(f"\n{'='*60}")


# Import scipy.stats for distribution analysis
try:
    from scipy import stats
except ImportError:
    print("⚠️  scipy not available. Some statistical functions may be limited.")
    stats = None
