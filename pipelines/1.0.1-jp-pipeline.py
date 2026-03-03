import pickle as pkl

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

"""
pipeline for turning 1.0.1 dataset into a format that can be used for training and
evaluation.
by jack phelan (not japanese just my initials)
"""


""" 
planned steps:
1. load data (from 1.0.1 pickle i guess)
2. turn binary categorical variables into 0/1 
3. turn categorical variables with more than 2 categories into one-hot encoding
3.5 handle date time stuff (maybe just drop for now)
4. (for 1.0.1) drop featues above a certain missing threshold, impute the rest
5. remove multiindex upper level 
"""


def load_data(file_path):
    with open(file_path, "rb") as f:
        data = pkl.load(f)
    return data


class BinaryCategoricalTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, boolean_cols):
        self.boolean_cols = boolean_cols

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_transformed = X.copy()
        for col in self.boolean_cols:
            X_transformed[col] = X_transformed[col].map({True: 1, False: 0})
        return X_transformed


class MultiCategoryTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, categorical_cols):
        self.categorical_cols = categorical_cols

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_transformed = X.copy()
        for col in self.categorical_cols:
            dummies = pd.get_dummies(X_transformed[col], prefix=col)
            X_transformed = pd.concat([X_transformed, dummies], axis=1)
            X_transformed.drop(col, axis=1, inplace=True)
        return X_transformed


class DateTimeTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, datetime_cols):
        self.datetime_cols = datetime_cols

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_transformed = X.copy()
        X_transformed = X_transformed.drop(self.datetime_cols, axis=1)
        return X_transformed


class MissingValueTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, missing_threshold=0.5):
        self.missing_threshold = missing_threshold

    def fit(self, X, y=None):
        self.cols_to_drop_ = X.columns[
            X.isnull().mean() > self.missing_threshold
        ].tolist()
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_transformed = X.copy()

        for col in X_transformed.columns:
            if X_transformed[col].isna().any():
                # Check if column is boolean type
                if (
                    X_transformed[col].dtype == "boolean"
                    or X_transformed[col].dtype == bool
                ):
                    # Fill boolean columns with mode (most common value) or False
                    fill_value = (
                        X_transformed[col].mode()[0]
                        if not X_transformed[col].mode().empty
                        else False
                    )
                    X_transformed[col] = X_transformed[col].fillna(fill_value)
                # Check if column is integer type
                elif pd.api.types.is_integer_dtype(X_transformed[col]):
                    # Round median to nearest integer
                    fill_value = round(X_transformed[col].median())
                    X_transformed[col] = X_transformed[col].fillna(fill_value)
                else:
                    # Fill numeric columns with median
                    X_transformed[col] = X_transformed[col].fillna(
                        X_transformed[col].median()
                    )

        return X_transformed


def main():
    # load data
    df = load_data("./data/interim/eda_1_0_1_df.pkl")

    x = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    bools = df.columns[df.dtypes == "bool"].tolist()
    cats = df.columns[df.dtypes == "object"].tolist()
    dts = df.columns[df.dtypes == "datetime64[ns]"].tolist()

    # create pipeline
    pipe = Pipeline(
        [
            ("multi_category", MultiCategoryTransformer(categorical_cols=cats)),
            ("binary_categorical", BinaryCategoricalTransformer(boolean_cols=bools)),
            ("datetime", DateTimeTransformer(datetime_cols=dts)),
            ("missing_value", MissingValueTransformer(missing_threshold=0.5)),
        ]
    )

    # fit and transform data
    transformed_data = pipe.fit_transform(x)

    print(transformed_data.head())


if __name__ == "__main__":
    main()
