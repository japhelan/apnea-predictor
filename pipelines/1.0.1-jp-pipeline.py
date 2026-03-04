import pickle as pkl

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
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


class TupleNameRemover(BaseEstimator, TransformerMixin):
    def __init__(self, sep="__", lowercase=False):
        self.sep = sep
        self.lowercase = lowercase

    def fit(self, X, y=None):
        return self

    def _flatten_name(self, col):
        if isinstance(col, tuple):
            parts = [str(p) for p in col if p is not None and str(p) != ""]
            name = self.sep.join(parts)
        else:
            name = str(col)
        return name.lower() if self.lowercase else name

    def transform(self, X):
        # Keep non-DataFrame inputs unchanged
        if not isinstance(X, pd.DataFrame):
            return X

        X_out = X.copy()

        # Handle MultiIndex columns and tuple columns
        if isinstance(X_out.columns, pd.MultiIndex):
            X_out.columns = [self._flatten_name(c) for c in X_out.columns.to_list()]
        else:
            X_out.columns = [self._flatten_name(c) for c in X_out.columns]

        return X_out


def main():
    # load data
    df = load_data("./data/interim/eda_1_0_1_df.pkl")

    df = df.dropna(subset=[df.columns[-1]])

    x = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    y = y.mask(y < 5, 0)
    y = y.mask(y >= 5, 1)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

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
            ("tuple_name_remover", TupleNameRemover()),
        ]
    )

    # fit and transform data
    x_train_transformed = pipe.transform(x_train)

    base_reg = LogisticRegression(max_iter=10000, solver="liblinear")

    base_reg.fit(x_train_transformed, y_train)

    preds = base_reg.predict(pipe.transform(x_test))

    train_preds = base_reg.predict(x_train_transformed)

    acc = (preds == y_test).mean()
    print(f"Test Accuracy: {acc:.4f}")

    train_acc = (train_preds == y_train).mean()
    print(f"Train Accuracy: {train_acc:.4f}")


if __name__ == "__main__":
    main()
