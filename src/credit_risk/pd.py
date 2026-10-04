from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from credit_risk.features import FeatureSet


def build_logistic_pipeline(feature_set: FeatureSet, *, random_state: int = 42) -> Pipeline:
    """Build the interpretable logistic PD model pipeline used by the project."""
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, list(feature_set.numeric)),
            ("categorical", categorical_transformer, list(feature_set.categorical)),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", LogisticRegression(max_iter=1000, random_state=random_state)),
        ]
    )


def fit_pd_model(data: pd.DataFrame, target: str, feature_set: FeatureSet) -> Pipeline:
    """Fit a logistic PD model for a provided feature set."""
    model = build_logistic_pipeline(feature_set)
    model.fit(data[feature_set.columns], data[target])
    return model


def predict_pd(model: Pipeline, data: pd.DataFrame, feature_set: FeatureSet) -> pd.Series:
    """Return probability-of-default predictions from a fitted classifier pipeline."""
    probabilities = model.predict_proba(data[feature_set.columns])[:, 1]
    return pd.Series(probabilities, index=data.index, name="predicted_pd")
