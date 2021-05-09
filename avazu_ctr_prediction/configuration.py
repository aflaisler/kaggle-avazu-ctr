"""Load configuration."""
import datetime
import os
import uuid

import pkg_resources
import toml

from avazu_ctr_prediction.constants import PKG_PATH


def load_conf(filename: str) -> dict:
    """
    Read toml file from the /conf folder.

    :params filename: str, name of the toml with the extension, ie: model_1.toml
    """
    with open(os.path.join(PKG_PATH, f"conf/{filename}")) as conf_file:
        conf = toml.load(conf_file)
    return conf


def initialise_run(config: dict) -> dict:
    """
    Create run dict at the start of a run.

    Parameters
    ----------
    config: configuration of the model
    """
    run_dict = dict()
    run_dict["conf"] = config
    run_dict["start_ts"] = datetime.datetime.now()
    # Model id
    run_dict["uuid"] = uuid.uuid4()
    run_dict["project"] = "avazu_ctr_prediction"
    run_dict["packaged_version"] = str(
        pkg_resources.get_distribution("avazu_ctr_prediction")
    )
    # TODO: add git commit sha
    return run_dict
