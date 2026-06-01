import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

### Univariate + Simple visualization methods


def make_histogram(df, column, bins=10, discrete=False, kde=False):
    """
    makes a histogram for a df column

    Parameters:
    df: The input DataFrame.
    column (str): The column name for which to create the histogram.
    bins:  The number of bins for the histogram.
    discrete (bool): If True, treats the data as discrete and adjusts the bins accordingly.
    kde (bool): If True, adds a Kernel Density Estimate (KDE) curve to the histogram.

    Returns:
    matplotlib.axes.Axes: The axes object of the histogram plot.
    """
    desc = ""
    sns.set_style("whitegrid")

    if discrete:
        unique_values = df[column].nunique()
        bins = unique_values + 1
        sns.histplot(df[column], bins=bins, kde=kde, discrete=True)
    else:
        sns.histplot(df[column], bins=bins, kde=kde)
    if isinstance(column, tuple):
        desc = column[0]
        column = column[1]  # for multi indexes
    plt.title(f"Histogram of {column}" + (f" ({desc})" if desc else ""))
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.show()

    return plt.gca()


def make_boxplot(df, column):
    """
    Creates a boxplot for the specified column in the DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    column (str): The column name for which to create the boxplot.

    Returns:
    matplotlib.axes.Axes: The axes object of the boxplot.
    """
    desc = ""
    feature = column

    if isinstance(column, tuple):
        desc = column[0]
        feature = column[1]  # for multi indexes

    plt.figure(figsize=(10, 6))
    ax = df.boxplot(column=column)
    ax.set_title(f"Boxplot of {feature}" + (f" ({desc})" if desc else ""))
    ax.set_ylabel(feature)
    plt.grid(True)
    plt.show()
    return ax


def make_scatterplot(df, x_col, y_col):
    """
    Creates a scatter plot for the specified x and y columns in the DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    x_col (str): The column name for the x-axis.
    y_col (str): The column name for the y-axis.

    Returns:
    matplotlib.axes.Axes: The axes object of the scatter plot.
    """
    x_desc = ""
    y_desc = ""

    if isinstance(x_col, tuple):
        x_desc = x_col[0]
        x_col = x_col[1]  # for multi indexes

    if isinstance(y_col, tuple):
        y_desc = y_col[0]
        y_col = y_col[1]  # for multi indexes

    plt.figure(figsize=(10, 6))
    ax = sns.scatterplot(data=df, x=x_col, y=y_col)
    ax.set_title(
        f"Scatter Plot of {y_col} vs {x_col}"
        + (f" ({y_desc} vs {x_desc})" if y_desc or x_desc else "")
    )
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    plt.grid(True)
    plt.show()
    return ax


def make_countplot(df, column, order_by_count=False):
    """
    Creates a count plot for the specified column in the DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    column (str): The column name for which to create the count plot.
    order_by_count (bool): If True, orders the bars by count.

    Returns:
    matplotlib.axes.Axes: The axes object of the count plot.
    """
    desc = ""
    feature = column

    if isinstance(column, tuple):
        desc = column[0]
        feature = column[1]  # for multi indexes

    plt.figure(figsize=(10, 6))
    if isinstance(df[column].dtype, pd.BooleanDtype):
        df[column] = df[column].astype(
            str
        )  # this raises a warning but its okay (i think) because it's not supposed to be permanent
    if df[column].nunique() > 20:
        print(
            f"Warning: Column '{feature}' has more than 20 unique values. Count plot may be cluttered."
        )

    if pd.api.types.is_datetime64_any_dtype(df[column]):
        converted_col = df[column].dt.time  # Direct conversion to time objects

        if order_by_count:
            order = converted_col.value_counts().index
            ax = sns.countplot(x=converted_col, order=order)
        else:
            ax = sns.countplot(x=converted_col)

        ax.set_title(f"Count Plot of {feature}" + (f" ({desc})" if desc else ""))
        ax.set_xlabel(feature)
        ax.set_ylabel("Count")
        plt.grid(True)
        plt.show()
        return ax
    else:

        if order_by_count:
            order = df[column].value_counts().index
            ax = sns.countplot(data=df, x=column, order=order)
        else:
            ax = sns.countplot(data=df, x=column)

        ax.set_title(f"Count Plot of {feature}" + (f" ({desc})" if desc else ""))
        ax.set_xlabel(feature)
        ax.set_ylabel("Count")
        return ax


def make_top_n_countplot(df, column, n=10, order_by_count=True):
    """
    Creates a count plot for the top n most frequent values in the specified column of the DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    column (str): The column name for which to create the count plot.
    n (int): The number of top categories to display in the count plot.

    Returns:
    matplotlib.axes.Axes: The axes object of the count plot.
    """
    top_n = df[column].value_counts().nlargest(n).index
    make_countplot(df[df[column].isin(top_n)], column, order_by_count=order_by_count)


### Other


def convert_dt_object(df, dt_cols=None, return_all=False, singular=False):
    """
    Converts all datetime columns in a selected dataframe to objects of dt.time type.
    Primarily used for visualizations that don't handle datetime types well, such as countplots.

    Parameters:
    df: The input DataFrame.
    dt_cols: A list of datetime column names to convert. If None, all datetime columns will be converted.
    return_all: If True, returns the entire DataFrame with converted datetime columns; otherwise,
    singular: If True, returns only the converted datetime column as a Series. If multiple datetime columns are provided while singular=True, a ValueError is raised.

    Returns: the datetime columns or the entire dataframe if return_all is True.
    """

    if singular and dt_cols is not None and len(dt_cols) == 1:
        dt_col = dt_cols[0]
        return df[dt_col].dt.time
    elif singular and dt_cols is not None and len(dt_cols) > 1:
        raise ValueError(
            "Multiple datetime columns provided while singular=True. Please provide only one column."
        )
    elif singular and dt_cols is None:
        raise ValueError(
            "No datetime columns provided while singular=True. Please provide one column."
        )
    elif df is None or df.empty:
        print("The DataFrame is empty or None. No datetime columns to convert.")
        return pd.DataFrame() if return_all else pd.Series(dtype="object")

    df_copy = df.copy()

    if dt_cols is None:
        dt_cols = df_copy.select_dtypes(include=["datetime64[ns]"]).columns

    dt_names = dt_cols.tolist()

    df_copy.loc[:, dt_cols] = df_copy.loc[:, dt_cols].apply(lambda x: x.dt.time)

    obj_cols = df_copy.loc[:, dt_names]
    if singular:
        return obj_cols.iloc[:, 0]

    obj_df = pd.DataFrame(obj_cols)

    if return_all:
        return df_copy
    return obj_df


### Bivariate/Multivariate Visualizations


def make_correlation_heatmap(df, columns):
    """
    Creates a correlation heatmap for the specified columns in the DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    columns (list of str): The list of column names for which to create the correlation heatmap.

    Returns:
    matplotlib.axes.Axes: The axes object of the correlation heatmap.
    """
    corr = df[columns].corr()
    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_title("Correlation Heatmap")
    plt.show()
    return ax


def correlation_above_threshold(df, threshold=0.5, return_table=False):
    """
    Identifies pairs of columns in the DataFrame that have a correlation coefficient above a specified threshold.

    Parameters:
    df : The input DataFrame.
    threshold : The correlation coefficient threshold for identifying correlated pairs.
    return_table : If True, returns a DataFrame of correlated pairs with their correlation values.

    Returns:
    if return_table: df with columns + their correlation value
    else: list of tuples of pairs of columns that are above the threshold
    """
    corr_matrix = df.corr().abs()
    mask = np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)

    # Find indices where mask is True and correlation exceeds threshold
    indices = np.argwhere(mask)
    correlated_pairs = [
        (corr_matrix.columns[j], corr_matrix.index[i], corr_matrix.iloc[i, j])
        for i, j in indices
        if corr_matrix.iloc[i, j] > threshold
    ]

    if return_table:
        return pd.DataFrame(
            correlated_pairs, columns=["Column 1", "Column 2", "Correlation"]
        )
    else:
        return [(col1, col2) for col1, col2, _ in correlated_pairs]


### Outlier detection utilities


def get_iqr_stats(df: pd.DataFrame):
    """Compute Q1, Q3, and IQR for every numeric column in *df*.

    Returns
    -------
    tuple[pd.Series, pd.Series, pd.Series]
        (Q1, Q3, IQR) indexed by column name.
    """
    num_cols = df.select_dtypes(include="number").columns
    q1 = df[num_cols].quantile(0.25)
    q3 = df[num_cols].quantile(0.75)
    iqr = q3 - q1
    return q1, q3, iqr


def flag_iqr_outliers(
    df: pd.DataFrame,
    q1: pd.Series,
    q3: pd.Series,
    iqr: pd.Series,
    multiplier: float = 1.5,
) -> pd.DataFrame:
    """Return a boolean DataFrame — True where a value is an IQR outlier.

    Only checks columns present in both *df* and the IQR stats index.

    Parameters
    ----------
    df : pd.DataFrame
        Data to check.
    q1, q3, iqr : pd.Series
        Output of :func:`get_iqr_stats`.
    multiplier : float, default 1.5
        Use 1.5 for mild outliers, 3.0 for extreme outliers.
    """
    shared_cols = df.columns.intersection(q1.index)
    sub = df[shared_cols]
    return (sub < (q1[shared_cols] - multiplier * iqr[shared_cols])) | (
        sub > (q3[shared_cols] + multiplier * iqr[shared_cols])
    )


def run_detector_ensemble(X: pd.DataFrame, contamination: float = 0.05) -> pd.DataFrame:
    """Fit IForest, LOF, and ECOD on *X* and return a vote DataFrame.

    Requires ``pyod``.

    Parameters
    ----------
    X : pd.DataFrame
        Feature matrix (no target column).
    contamination : float, default 0.05
        Expected fraction of outliers passed to each detector.

    Returns
    -------
    pd.DataFrame
        Boolean columns IForest / LOF / ECOD (True = outlier) plus
        an integer ``n_votes`` column.
    """
    from pyod.models.iforest import IForest
    from pyod.models.lof import LOF
    from pyod.models.ecod import ECOD

    arr = X.to_numpy()
    results = {}
    for name, det in [
        ("IForest", IForest(contamination=contamination, random_state=42)),
        ("LOF", LOF(contamination=contamination)),
        ("ECOD", ECOD(contamination=contamination)),
    ]:
        det.fit(arr)
        results[name] = det.labels_.astype(bool)  # True = outlier

    votes = pd.DataFrame(results, index=X.index)
    votes["n_votes"] = votes.sum(axis=1)
    return votes


def class_conditional_iforest(
    X,
    class_labels: pd.Series,
    contamination: float = 0.05,
    n_estimators: int = 200,
    random_state: int = 42,
    verbose: bool = True,
) -> np.ndarray:
    """Run IsolationForest independently within each class.

    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        Feature matrix.
    class_labels : pd.Series
        Per-row class membership (e.g. AHI severity strings).
    contamination : float, default 0.05
    n_estimators : int, default 200
    random_state : int, default 42
    verbose : bool, default True
        Print per-class outlier counts.

    Returns
    -------
    np.ndarray of int
        sklearn convention: 1 = normal, -1 = outlier.
    """
    from sklearn.ensemble import IsolationForest

    X_arr = X if isinstance(X, np.ndarray) else np.asarray(X)
    labels = np.ones(len(X_arr), dtype=int)

    if verbose:
        print(f"Class-conditional IsolationForest (contamination={contamination}):")

    for cls in sorted(class_labels.unique()):
        mask = (class_labels == cls).values
        if mask.sum() == 0:
            continue
        clf = IsolationForest(
            n_estimators=n_estimators,
            contamination=contamination,
            random_state=random_state,
        )
        clf.fit(X_arr[mask])
        preds = clf.predict(X_arr[mask])
        labels[mask] = preds
        if verbose:
            n = mask.sum()
            n_out = (preds == -1).sum()
            print(
                f"  {cls:8s} (n={n:4d}): {n_out:3d} outliers ({100 * n_out / n:.1f}%)"
            )

    if verbose:
        n_out_total = (labels == -1).sum()
        print(
            f"\nTotal: {n_out_total} outliers ({100 * n_out_total / len(labels):.1f}%)"
        )

    return labels


def build_outlier_flags(label_dict: dict, index=None) -> pd.DataFrame:
    """Build a boolean outlier membership DataFrame.

    Parameters
    ----------
    label_dict : dict
        Mapping of method name → boolean array/series (True = outlier).
    index : array-like, optional
        Row index for the resulting DataFrame.

    Returns
    -------
    pd.DataFrame
        Boolean columns per method plus an integer ``n_methods`` column.
    """
    df = pd.DataFrame(label_dict, index=index)
    df["n_methods"] = df.sum(axis=1)
    return df


def jaccard_similarity_matrix(flag_df: pd.DataFrame) -> pd.DataFrame:
    """Compute pairwise Jaccard similarity between boolean columns.

    Parameters
    ----------
    flag_df : pd.DataFrame
        DataFrame of boolean columns (True = outlier). Must not contain
        non-boolean columns like ``n_methods``.

    Returns
    -------
    pd.DataFrame
        Square matrix of Jaccard scores (1.0 = identical outlier sets).
    """
    cols = flag_df.columns.tolist()
    matrix = pd.DataFrame(index=cols, columns=cols, dtype=float)
    for a in cols:
        for b in cols:
            both = (flag_df[a] & flag_df[b]).sum()
            union = (flag_df[a] | flag_df[b]).sum()
            matrix.loc[a, b] = both / union if union > 0 else 1.0
    return matrix
