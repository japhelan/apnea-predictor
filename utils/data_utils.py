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


