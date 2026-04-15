"""
holds all transformers for piplines. wip as of 4/2
"""

# 1.1.1 jp pipeline transfomrers
import re
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder


class Column_Categorical_Bucketizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self = self

    def fit(self, X, y=None):
        self.columns = [
            col
            for col in X.columns
            if X[col].dtype in ["string", "object"] and X[col].nunique() > 10
        ]
        return self

    def transform(self, X):
        X_transformed = X.copy()
        for col in self.columns:
            X_transformed[col] = np.where(
                X_transformed[col].str.contains("per week"),
                "frequent",
                np.where(
                    X_transformed[col].str.contains("per month"),
                    "occasional",
                    np.where(
                        X_transformed[col].str.contains("per year"),
                        "rare",
                        "never_unknown",
                    ),
                ),
            )

        return X_transformed


""" 
Also a transformer for "x per y" columns; instead of encoding calculates the weekly 
ratio based off of the string. will be compared to the bucketizer later
hasn't been tested at all 
"""


class Column_Weekly_Ratio_Transformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self = self

    def fit(self, X, y=None):
        self.columns = [
            col
            for col in X.columns
            if X[col].dtype in ["string", "object"] and X[col].nunique() > 10
        ]
        return self

    def transform(self, X):
        X_transformed = X.copy()
        for col in self.columns:
            X_transformed["numbers"] = (
                X_transformed[col].str.extract(r"(\d+)").astype(float)
            )
            # Further processing to calculate weekly ratio can be added here
            X_transformed[col] = np.where(
                X_transformed[col].str.contains("per week"),
                X_transformed["numbers"],
                np.where(
                    X_transformed[col].str.contains("per month"),
                    X_transformed["numbers"] / 4,
                    np.where(
                        X_transformed[col].str.contains("per year"),
                        X_transformed["numbers"] / 52,
                        0,
                    ),
                ),
            )

        return X_transformed.drop(columns=["numbers"])


""" 
one hot encoder that takes wonky categories into account
"""


class One_Hot_Encoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.encoder = OneHotEncoder(
            handle_unknown="ignore", sparse_output=False, drop="first"
        )

    def fit(self, X, y=None):
        self.columns_ = [
            col
            for col in X.columns
            if X[col].dtype == "bool"
            or (X[col].dtype == "int64" and X[col].nunique() == 2)
            or (X[col].dtype == "object" and X[col].nunique() < 10)
        ]
        self.encoder.fit(X.loc[:, self.columns_])
        return self

    def transform(self, X):
        encoded = pd.DataFrame(
            self.encoder.transform(X.loc[:, self.columns_]),
            columns=self.encoder.get_feature_names_out(self.columns_),
            index=X.index,
        )
        passthrough = X.drop(columns=self.columns_)
        return pd.concat([passthrough, encoded], axis=1)


class Median_Imputer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.imputer = SimpleImputer(strategy="median")

    def fit(self, X, y=None):
        self.columns = X.select_dtypes(include=["number"]).columns
        self.imputer.fit(X.loc[:, self.columns])
        return self

    def transform(self, X):
        X_transformed = X.copy()
        X_transformed.loc[:, self.columns] = self.imputer.transform(
            X_transformed.loc[:, self.columns]
        )
        return X_transformed


class Frequency_Imputer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.imputer = SimpleImputer(strategy="most_frequent")

    def fit(self, X, y=None):
        self.columns = X.select_dtypes(include=["object", "bool"]).columns
        self.imputer.fit(X.loc[:, self.columns])
        return self

    def transform(self, X):
        X_transformed = X.copy()
        X_transformed.loc[:, self.columns] = self.imputer.transform(
            X_transformed.loc[:, self.columns]
        )
        return X_transformed


class Type_Transformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self = self

    def fit(self, X, y=None):
        self.string_columns = X.select_dtypes(include=["string"]).columns
        self.Int_columns = X.select_dtypes(include=["Int64", "Int32"]).columns
        return self

    def transform(self, X):
        X_transformed = X.copy()
        for col in self.string_columns:
            X_transformed[col] = (
                X_transformed[col]
                .astype("object")
                .where(X_transformed[col].notna(), other=np.nan)
            )
        for col in self.Int_columns:
            X_transformed[col] = X_transformed[col].astype("float64")
        # Convert any remaining nullable extension dtypes for sklearn compatibility
        for col in X_transformed.columns:
            if pd.api.types.is_extension_array_dtype(X_transformed[col].dtype):
                if pd.api.types.is_numeric_dtype(X_transformed[col]):
                    X_transformed[col] = X_transformed[col].astype("float64")
                else:
                    X_transformed[col] = (
                        X_transformed[col].astype("object").fillna(np.nan)
                    )
        return X_transformed
