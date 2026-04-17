import pandas as pd
import joblib
from src.features.feature_encoder import encode_features
from src.features.raw_data_loader import load_and_clean_raw
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from src.utils.data_utils import convert_ahi
from src.features.transformers import Factor_Analyzer_Transformer
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score


def main():
    # Load and clean raw data
    raw_df = load_and_clean_raw(".")

    # Encode features
    encoded_df = encode_features(raw_df)

    # Separate features and target
    X = encoded_df.drop(columns=["ahi"])
    y = encoded_df["ahi"]

    y = convert_ahi(y)  # Convert AHI to binary target (apnea vs no apnea)

    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Create a pipeline with the Factor Analyzer transformer
    pipeline = Pipeline(
        [
            (
                "factor_analysis",
                Factor_Analyzer_Transformer(n_factors=18, rotation="promax"),
            ),
            # You can add more steps here (e.g., imputation, scaling) if needed
        ]
    )

    # Fit the pipeline on the training data
    pipeline = pipeline.fit(X_train, y_train)

    X_train_transformed = pipeline.transform(X_train)
    X_test_transformed = pipeline.transform(X_test)

    # Train a simple model (e.g., XGBoost) on the transformed features
    model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    model.fit(X_train_transformed, y_train)
    y_pred = model.predict(X_test_transformed)
    y_proba = model.predict_proba(X_test_transformed)[:, 1]
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("ROC AUC Score:", roc_auc_score(y_test, y_proba))


if __name__ == "__main__":
    main()
