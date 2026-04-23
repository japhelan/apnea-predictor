"""
holds all transformers for piplines. wip as of 4/2
"""

# 1.1.1 jp pipeline transfomrers
import re
from typing import cast

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from factor_analyzer import FactorAnalyzer


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


class Factor_Analyzer_Transformer(BaseEstimator, TransformerMixin):
    """
    2.1.0-jp-pipeline transformer that applies factor analysis to numeric features
    params gotten from the 2.1-jp-feature-engineering notebook
    """

    def __init__(
        self,
        n_factors: int = 18,
        rotation: str | None = "promax",
        method: str = "minres",
    ):
        self.n_factors = n_factors
        self.rotation = rotation
        self.method = method

    def fit(self, X, y=None):
        numeric_cols = X.select_dtypes(include=["number"]).columns
        variances = X[numeric_cols].var()
        self.columns_ = variances[variances > 1e-10].index
        self.fa_ = FactorAnalyzer(
            n_factors=self.n_factors,
            rotation=cast(str, self.rotation),
            method=cast(str, self.method),
        )
        self.fa_.fit(X.loc[:, self.columns_])
        return self

    def transform(self, X):
        X_transformed = X.copy()
        factors = self.fa_.transform(X_transformed.loc[:, self.columns_])
        factor_cols = [f"factor_{i+1}" for i in range(self.n_factors)]
        factors_df = pd.DataFrame(factors, columns=factor_cols, index=X.index)
        return pd.concat(
            [X_transformed.drop(columns=self.columns_), factors_df], axis=1
        )

    def get_factor_loadings(self):
        loadings = pd.DataFrame(
            self.fa_.loadings_,
            index=self.columns_,
            columns=[f"factor_{i+1}" for i in range(self.n_factors)],
        )
        return loadings

    def get_top_loadings(self):
        loadings = self.get_factor_loadings()
        loadings_df = pd.DataFrame(loadings, index=self.columns_)
        loadings_df.columns = [f"Factor_{i+1}" for i in range(loadings_df.shape[1])]
        loadings_df.head(10)

        for i in range(loadings.shape[1]):
            print(f"Top loadings for Factor_{i+1}:")
            print(
                loadings_df[f"Factor_{i+1}"].abs().sort_values(ascending=False).head(8)
            )
            print("\n")
