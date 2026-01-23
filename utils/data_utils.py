"""
Docstring for python.functions
This module contains various utility functions used throughout the project.
"""

import pandas as pd


def add_multi_index(df, display_names):
    """
    Adds a multi-level index to the DataFrame columns using display names.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    display_names (dict): A dictionary mapping column names to display names.

    Returns:
    pd.DataFrame: DataFrame with multi-level column index.
    """
    # check if already a multi index
    if isinstance(df.columns, pd.MultiIndex):
        return df
    new_columns = []
    for col in df.columns:
        if col in display_names:
            new_columns.append((display_names[col], col))
        else:
            new_columns.append(("", col))

    df.columns = pd.MultiIndex.from_tuples(new_columns)
    return df


def inspect_structure(df):
    """
    Prints the structure of the DataFrame including column names and data types.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    """
    if not hasattr(df, "name"):
        df.name = "DataFrame"
    print(f"Structure of {df.name}:")
    print("Shape: ", df.shape[0], " rows x ", df.shape[1], " columns")
    print(df.info())


def check_duplicates(datasets):
    """
    Checks for duplicate rows in each DataFrame within the provided dictionary.
    Parameters:
    datasets (dict): A dictionary where keys are dataset names and values are DataFrames.
    """
    if isinstance(datasets, pd.DataFrame):
        datasets = {"Dataset": datasets}

    for name, df in datasets.items():
        print(f"\n {name} - Duplicate Rows Check:")
        total_rows = len(df)
        dup_rows = df.duplicated()
        dup_count = dup_rows.sum()
        dup_percent = round((dup_count / total_rows) * 100, 2)

        if dup_count > 0:
            print(f"Found {dup_count} duplicate rows ({dup_percent}%)")
            print("Sample duplicates:\n", df[dup_rows].head())
        else:
            print("No duplicate rows detected.")


def check_nulls(datasets):
    """
    Checks for null values in each DataFrame within the provided dictionary.

    Parameters:
    datasets (dict): A dictionary where keys are dataset names and values are DataFrames.
    """
    if isinstance(datasets, pd.DataFrame):
        datasets = {"Dataset": datasets}

    for name, df in datasets.items():
        print(f"\n {name} - Null Values Check:")
        total_rows = len(df)
        null_counts = df.isnull().sum()
        null_percent = (null_counts / total_rows) * 100

        null_summary = pd.DataFrame(
            {"Null Count": null_counts, "Null Percentage": null_percent}
        )

        null_summary = null_summary[null_summary["Null Count"] > 0]

        if not null_summary.empty:
            print(null_summary)
        else:
            print("No null values detected.")


def flag_high_nulls(df, threshold=0.8, return_df=True):
    """
    Flags columns in the DataFrame that have a high percentage of null values.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    threshold (float): The threshold percentage (between 0 and 1) to flag columns.
    return_df (bool): If True, returns a DataFrame with details; otherwise returns a list of column names.

    Returns:
    pd.DataFrame or list: DataFrame with details if return_df is True, else list of column names with high null percentages.
    """
    total_rows = len(df)
    null_percent = df.isnull().sum() / total_rows
    high_nulls = null_percent[null_percent > threshold].index.tolist()

    high_null_pct = null_percent[null_percent > threshold]

    if return_df:

        dict = {
            "Column Name": [],
            "Column Description": [],
            "Null Percentage": [],
            "Index": [],
        }

        for i, col in enumerate(high_nulls):
            null_percentage = high_null_pct.iloc[i]
            index = high_nulls[i]
            name = index[1]
            desc = index[0]
            dict["Column Name"].append(name)
            dict["Column Description"].append(desc)
            dict["Null Percentage"].append(null_percentage)
            dict["Index"].append(index)

        null_df = pd.DataFrame.from_dict(dict, orient="columns")

        return null_df
    else:
        print(f"Columns with more than {threshold*100}% null values: {high_nulls}")
        return high_nulls


def make_column_description_table(
    df,
    add_display_names=False,
    display_names=None,
    return_df=True,
    show_null_pct=False,
    return_md=False,
    filepath=None,
):
    """
    Creates a DataFrame describing the DataFrame columns, their display names, and data types.
    Mostly used for documentation purposes.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    add_display_names (bool): If True, adds display names to the description table.
    display_names (dict): A dictionary mapping column names to display names.
    return_df (bool): If True, returns the description DataFrame; otherwise prints it.
    show_null_pct (bool): If True, includes a column for the percentage of null values in each column.
    return_md (bool): If True, exports the description as a markdown file.
    filepath (str): The file path to save the markdown table if return_md is True.

    Returns:
    pd.DataFrame or None: Description DataFrame if return_df is True, else None.
    """

    if show_null_pct:
        total_rows = len(df)
        null_percent = (df.isnull().sum() / total_rows) * 100
        df.loc["Null Percentage"] = null_percent

        data = {
            "Column Name": [],
            "Display Name": [],
            "Data Type": [],
            "Null Percentage": [],
        }
    else:
        data = {"Column Name": [], "Display Name": [], "Data Type": []}

    for col in df.columns:
        data["Column Name"].append(
            col[1] if isinstance(col, tuple) else col
        )  # for multi indexes
        if add_display_names:
            if display_names is not None:
                if isinstance(display_names, pd.Index):  # use pandas indexing
                    display_name = display_names[df.columns.get_loc(col)]
                else:  # not a pandas index
                    display_name = display_names.get(col, "")
                data["Display Name"].append(display_name)
            else:  # no display names provided
                data["Display Name"].append("")
        else:  # not using display names
            data["Display Name"].append("")
        data["Data Type"].append(str(df[col].dtype))
        if show_null_pct:  # if showing null percentage
            null_pct = round((df[col].isnull().sum() / len(df)) * 100, 2)
            null_pct = f"{null_pct}%"
            data["Null Percentage"].append(null_pct)

    desc_df = pd.DataFrame(data)

    if return_df:
        return desc_df
    else:
        print(desc_df)

    if return_md and filepath:
        desc_df.to_markdown(filepath, index=False)


def strip_text_sub(text):
    """
    Strips leading and trailing whitespace from the input text.

    Parameters:
    text (str): The input text.

    Returns:
    str: The stripped text.
    """
    if isinstance(text, str):
        text = text.lower()
        text = text.replace(" - ", "_")
        text = text.replace("?", "")
        text = text.replace(" ", "_")
        text = text.replace("'", "")
        text = text.replace(",", "")
        text = text.replace(":", "")

        text = text.strip()
        text = text.rstrip("_")

        return text
    else:
        # Handle pandas Series
        text = text.str.lower()
        text = text.str.replace(" - ", "_")
        text = text.str.replace("?", "")
        text = text.str.replace(" ", "_")
        text = text.str.replace("'", "")
        text = text.str.replace(",", "")
        text = text.str.replace(":", "")
        text = text.str.strip()
        text = text.str.rstrip("_")

        return text


def strip_text(text):
    """
    Strips leading and trailing whitespace from the input text, Series, DataFrame, list, or dict.
    Parameters:
    text (str, pd.Series, pd.DataFrame, list, dict): The input text or collection of texts.
    Returns:
    str, pd.Series, pd.DataFrame, list, dict: The stripped text or collection of texts.
    """
    if isinstance(text, str):
        text = strip_text_sub(text)
    elif isinstance(text, pd.Series):
        text = text.apply(strip_text_sub)
    elif isinstance(text, pd.DataFrame):
        text = text.apply(strip_text_sub)
    elif isinstance(text, list):
        text = [strip_text_sub(t) for t in text]
    elif isinstance(text, dict):
        text = {k: strip_text_sub(v) for k, v in text.items()}
    elif hasattr(text, "__iter__") and not isinstance(
        text, (str, pd.Series, pd.DataFrame)
    ):
        # Handle dict_values, dict_keys, and other iterables
        text = [strip_text_sub(t) for t in text]
    return text


def df_quality_check(df):
    """
    Performs a quality check on the DataFrame by checking for duplicates and null values.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    """
    print("Performing Data Quality Check...")
    check_duplicates(df)
    check_nulls(df)
