"""
Module creating the modelling pipeline from the configuration parameters.
"""
import importlib

import numpy as np
import pandas as pd
from loguru import logger
from sklearn.compose import ColumnTransformer
from sklearn.metrics import log_loss
from sklearn.pipeline import Pipeline

from avazu_ctr_prediction.constants import FEATURES


def object_from_dict(object_definition: dict) -> object:
    """Create a python object from dictionary.

    Parameters
    ----------
    object_definition : dictionary containing the following keys: {"module", "class", "params"}

    """
    module = importlib.import_module(object_definition["module"])
    class_ = getattr(module, object_definition["class"])
    object_ = class_(**object_definition["params"])
    return object_


def make_pipeline(steps: list) -> Pipeline:
    """Create unfitted sklearn pipeline object as defined in config."""
    steps = [(step["name"], object_from_dict(step)) for step in steps if step]
    return Pipeline(steps)


def make_preprocessor(config: dict) -> ColumnTransformer:
    """Create sklearn preprocessor object as defined in config."""
    preprocessors = [
        (str(i), make_pipeline(definition["steps"]), definition["features"])
        for i, definition in enumerate(config["preprocessing"])
    ]
    processed_features = [d["features"] for d in config["preprocessing"]]
    processed_features = list(pd.core.common.flatten(processed_features))
    unprocessed_feats = [x for x in FEATURES if x not in processed_features]

    preprocessors.append(("passthrough", "passthrough", unprocessed_feats))
    return ColumnTransformer(preprocessors)


def train(X_train: pd.DataFrame, y_train: pd.DataFrame, config: dict) -> Pipeline:
    """Fit the transformers and model."""
    preprocessor = make_preprocessor(config)

    pipeline = Pipeline(
        [("preprocess", preprocessor), ("model", object_from_dict(config["model"]))]
    )

    pipeline.fit(X_train, y_train, **config["fit_params"])

    return pipeline


def train_and_predict(
    X_train: pd.DataFrame, y_train: pd.DataFrame, X_test: pd.DataFrame, config: dict
) -> (Pipeline, np.array):
    """Return model and prediction probability for X_test."""
    logger.info(f"Training the classification.")
    model = train(X_train, np.ravel(y_train), config)
    test_proba_predictions = model.predict_proba(X_test)

    return model, test_proba_predictions
