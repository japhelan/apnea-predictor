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
from src.features.transformers import (
    Type_Transformer,
    Column_Categorical_Bucketizer,
    Column_Weekly_Ratio_Transformer,
    One_Hot_Encoder,
    Median_Imputer,
    Frequency_Imputer,
)
import joblib


""" 
transformer for the "x per y" columns to make them easier to one-hot encode
used for data version 1.1.1 
might experiment with per week ratio instead of column encoding 
"""


def main():
    # import data

    df = joblib.load("data/interim/fe_1_1_1_data.pkl")

    y = df["ahi"].where(df["ahi"] >= 5, 1).where(df["ahi"] < 5, 0)
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
        transformed = data_pipeline.transform(X_train)
        feature_names = transformed.columns
        importances = model.feature_importances_
        feature_importance_df = pd.DataFrame(
            {"feature": feature_names, "importance": importances}
        ).sort_values(by="importance", ascending=False)
        return feature_importance_df

    feature_importance_df = feature_importance(model, data_pipeline_fitted, X_train)
    print(feature_importance_df.head(20))

    joblib.dump(model, "./data/interim/models/1_1_1_rf_model.pkl")
    joblib.dump(data_pipeline_fitted, "./data/interim/models/1_1_1_data_pipeline.pkl")


if __name__ == "__main__":
    main()
