"""Entry point for avazu_ctr_prediction library."""
import pickle
import pprint

import click
import numpy as np
import pandas as pd
from loguru import logger
from sklearn.metrics import log_loss

import avazu_ctr_prediction.configuration
from avazu_ctr_prediction.constants import (
    FEATURES,
    TARGET,
    MODEL_PATH,
    DATA_PATH,
    CAT_PATH,
    CAT_FREQ_MIN,
)
from avazu_ctr_prediction.exceptions import MissingModelException
from avazu_ctr_prediction.ml_pipeline import train
from avazu_ctr_prediction.preprocess import category_to_keep, map_rare_category
from avazu_ctr_prediction.utils import check_columns


@click.group()
def cli():
    """Run the main function of the package.

    To start using it run a command like:

    "avazu_ctr_prediction train --data-location="data/train.csv" --debug"
    """
    pass


@cli.command(name="train")
@click.argument("data_location", type=click.Path(exists=True), required=True)
def cmd_train(data_location: str):
    """Train the CTR model.

    :params data_location: str, path to the data
    """
    model_config = avazu_ctr_prediction.configuration.load_conf("model_catboost.toml")
    run_dict = avazu_ctr_prediction.configuration.initialise_run(model_config)
    logger.info(f"Running model {model_config['model']['class']}")

    df_data = pd.read_csv(data_location)
    # Transform Hour column to effectively keep only hours (ie: 23 for 23:00)
    df_data.loc[:, "hour"] = df_data.loc[:, "hour"].map(lambda x: str(int(str(x)[-2:])))
    check_columns(df_data, FEATURES + [TARGET])
    X = df_data[FEATURES]
    y = df_data[TARGET]
    logger.info(
        f"Some columns have a very high cardinality. We will mask under "
        f"the same category the ones with a frequency < {CAT_FREQ_MIN}"
    )
    category_to_keep(X, CAT_PATH, CAT_FREQ_MIN)
    X = map_rare_category(X)
    model = train(X, y, model_config)

    logger.info(
        f"Log loss on the training set: {np.round(model[-1].best_score_['learn']['Logloss'], 4)}"
    )

    # Saving model
    logger.info(f"Saving model here: {MODEL_PATH}")
    with open(MODEL_PATH, "wb") as pickle_file:
        pickle.dump(model, pickle_file)
    logger.info(f"Run's metadata: {pprint.pformat(run_dict)}")

    logger.info("End of the run.")


@cli.command(name="predict")
@click.argument("data_location", type=click.Path(exists=True), required=True)
def cmd_predict(data_location: str):
    """Predict probability of a click from the CTR model.

    :params data_location: str, path to the data to predict. Check the constant FEATURES for the expected columns.
    """
    logger.info(f"Loading model from {MODEL_PATH}")

    df_data = pd.read_csv(data_location)
    # Transform Hour column to effectively keep only hours (ie: 23 for 23:00)
    df_data.loc[:, "hour"] = df_data.loc[:, "hour"].map(lambda x: str(x)[-2:])
    check_columns(df_data, FEATURES)
    X = df_data[FEATURES]
    X = map_rare_category(X)

    # Load model
    try:
        with open(f"{MODEL_PATH}", "rb") as pickle_file:
            model = pickle.load(pickle_file)
    except FileNotFoundError:
        raise MissingModelException("Model is not found. Please first train the model.")

    predictions = model.predict_proba(X)

    # Saving predictions
    predictions_path = f"{DATA_PATH}/predictions.csv"
    logger.info(f"Saving predictions to {predictions_path}")
    df_predictions = pd.DataFrame(predictions, columns=["0", "1"])
    df_predictions.to_csv(predictions_path, index=False)
    logger.info("End of the run")


@cli.command(name="eval")
@click.argument("data_location", type=click.Path(exists=True), required=True)
def cmd_eval(data_location: str):
    """Calculate the Logloss from the latest prediction run.

    :params data_location: str, path to the data to evaluate (click - binary)..
    """
    y_data = pd.read_csv(data_location)
    predictions_path = f"{DATA_PATH}/predictions.csv"
    predictions = pd.read_csv(predictions_path)
    logger.info(
        f"Log loss on the test set: {np.round(log_loss(y_data, predictions), 4)}"
    )
