"""Entry point for avazu_ctr_prediction library."""
import click
from loguru import logger
import pandas as pd
from sklearn.model_selection import train_test_split

import avazu_ctr_prediction.configuration
from avazu_ctr_prediction.constants import FEATURES, TARGET, RANDOM_STATE
from avazu_ctr_prediction.ml_pipeline import train_and_predict
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
@click.option("--debug/--no-debug", default=False)
def cmd_train(data_location: str, debug: bool):
    """Train the CTR model.

    :params segment:
    """
    model_config = avazu_ctr_prediction.configuration.load_conf()
    run_dict = avazu_ctr_prediction.configuration.initialise_run(model_config)
    logger.info(f"Running model {model_config['model']['class']}")

    df_data = pd.read_csv(data_location)
    check_columns(df_data, FEATURES + [TARGET])
    X = df_data[FEATURES]
    y = df_data[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=RANDOM_STATE)
    model, predictons = train_and_predict(
        X_train, y_train, X_test, model_config
    )

    logger.info("End of the run.")

    # train(data_location, debug=debug)
