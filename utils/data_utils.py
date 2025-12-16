'''
Docstring for python.functions
This module contains various utility functions used throughout the project.
'''

import pandas as pd
import numpy as np

def add_multi_index(df, display_names):
    """
    Adds a multi-level index to the DataFrame columns using display names.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    display_names (dict): A dictionary mapping column names to display names.

    Returns:
    pd.DataFrame: DataFrame with multi-level column index.
    """
    new_columns = []
    for col in df.columns:
        if col in display_names:
            new_columns.append((display_names[col], col))
        else:
            new_columns.append(('', col))
    
    df.columns = pd.MultiIndex.from_tuples(new_columns)
    return df


def inspect_structure(df):
    """
    Prints the structure of the DataFrame including column names and data types.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    """
    print(f"Structure of {df.name}:")
    print("Shape: ", df.shape[0], ' rows x ', df.shape[1], ' columns')
    print(df.info())


def check_duplicates(datasets):
    """
    Checks for duplicate rows in each DataFrame within the provided dictionary.
    Parameters:
    datasets (dict): A dictionary where keys are dataset names and values are DataFrames.
    """
    if isinstance(datasets, pd.DataFrame):
        datasets = {'Dataset': datasets}

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
        datasets = {'Dataset': datasets}

    for name, df in datasets.items():
        print(f"\n {name} - Null Values Check:")
        total_rows = len(df)
        null_counts = df.isnull().sum()
        null_percent = (null_counts / total_rows) * 100

        null_summary = pd.DataFrame({
            'Null Count': null_counts,
            'Null Percentage': null_percent
        })

        null_summary = null_summary[null_summary['Null Count'] > 0]
        
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

    Returns:
    list: List of column names with high null percentages.
    """
    total_rows = len(df)
    null_percent = df.isnull().sum() / total_rows
    high_nulls = null_percent[null_percent > threshold].index.tolist()

    if return_df:

        null_df = pd.DataFrame({
            'Column Name': high_nulls,
            'Null Percentage': null_percent[high_nulls] * 100
        })
        
        print(f"Columns with more than {threshold*100}% null values: {high_nulls}")
        return null_df
    else:
        print(f"Columns with more than {threshold*100}% null values: {high_nulls}")
        return high_nulls

def export_column_description_table(df, display_names, filepath):
    """
    Exports a markdown table describing the DataFrame columns, their display names, and data types. 
    Mostly used for documentation purposes.
    Parameters:
    df (pd.DataFrame): The input DataFrame.
    display_names (dict): A dictionary mapping column names to display names.
    filepath (str): The file path to save the markdown table.
    """

    data = {"Column Name": [], "Display Name": [], "Data Type": []}
    for col in df.columns:
        data["Column Name"].append(col)
        data["Display Name"].append(display_names.get(col, "N/A"))
        data["Data Type"].append(str(df[col].dtype))

    desc_df = pd.DataFrame(data)
    desc_df.to_markdown(filepath, index=False)
        
    
