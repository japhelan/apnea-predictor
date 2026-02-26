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
    if isinstance(df[column].dtype, pd.BooleanDtype):  # handle boolean columns
        df[column] = df[column].astype(str)
    if df[column].nunique() > 20:  # handle high cardinality columns
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
    upper_triangle = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )
    correlated_pairs = [
        (col1, col2)
        for col1 in upper_triangle.columns
        for col2 in upper_triangle.index
        if upper_triangle.loc[col2, col1] > threshold
    ]

    if return_table:
        correlated_pairs = [
            (col1, col2, upper_triangle.loc[col2, col1])
            for col1, col2 in correlated_pairs
        ]

        return pd.DataFrame(
            correlated_pairs, columns=["Column 1", "Column 2", "Correlation"]
        )
    else:
        return correlated_pairs
