"""
model training pipeline for use with data 1.1.1
"""

from pyexpat import model
import re

import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


""" 
transformer for the "x per y" columns to make them easier to one-hot encode
used for data version 1.1.1 
might experiment with per week ratio instead of column encoding 
"""


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
            X_transformed["numbers"] = re.findall(r"\d+", X_transformed[col])
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
        self.encoder = OneHotEncoder(handle_unknown="ignore")

    def fit(self, X, y=None):
        self.columns = [
            col
            for col in X.columns
            if X[col].dtype == "bool"
            or (X[col].dtype == "int64" and X[col].nunique() == 2)
            or (X[col].dtype == "object" and X[col].nunique() < 10)
        ]
        self.encoder.fit(X.loc[:, self.columns])
        return self

    def transform(self, X):
        return self.encoder.transform(X.loc[:, self.columns])


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


def main():
    # import data

    df = joblib.load("data/interim/fe_1_1_1_data.pkl")

    y = df["ahi"].where(df["ahi"] >= 5, 0).where(df["ahi"] < 5, 1)
    X = df.drop(columns=["ahi"])

    " ima figure these out later o7"
    datetime_cols = X.select_dtypes(include=["datetime", "datetime64"]).columns

    X = X.drop(columns=datetime_cols)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    type_transformer = Type_Transformer()
    median_imputer = Median_Imputer()
    frequency_imputer = Frequency_Imputer()
    cat_bucketizer = Column_Categorical_Bucketizer()
    ohe = One_Hot_Encoder()

    data_pipeline = Pipeline(
        steps=[
            ("type_transformer", type_transformer),
            ("median_imputer", median_imputer),
            ("frequency_imputer", frequency_imputer),
            ("cat_bucketizer", cat_bucketizer),
            ("one_hot_encoder", ohe),
        ]
    )

    data_pipeline_fitted = data_pipeline.fit(X_train, y_train)

    model = RandomForestClassifier(random_state=42)

    model.fit(data_pipeline_fitted.transform(X_train), y_train)

    y_pred = model.predict(data_pipeline_fitted.transform(X_test))
    print(classification_report(y_test, y_pred))

    # feature importance

    def feature_importance(model, data_pipeline, X_train):
        feature_names = data_pipeline.named_steps[
            "one_hot_encoder"
        ].encoder.get_feature_names_out(
            data_pipeline.named_steps["one_hot_encoder"].columns
        )
        importances = model.feature_importances_
        feature_importance_df = pd.DataFrame(
            {"feature": feature_names, "importance": importances}
        ).sort_values(by="importance", ascending=False)
        return feature_importance_df

    feature_importance_df = feature_importance(model, data_pipeline_fitted, X_train)
    print(feature_importance_df.head(20))


if __name__ == "__main__":
    main()
