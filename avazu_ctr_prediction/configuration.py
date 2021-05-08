"""Load configuration."""
import toml
import uuid
import datetime
import pkg_resources
from subprocess import STDOUT, call
import os

from loguru import logger


import avazu_ctr_prediction.constants


def load_conf() -> dict:
    """Read toml file."""
    with open(avazu_ctr_prediction.constants.CONF_PATH) as conf_file:
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
    # TODO: figure out if we keep
    # if call(["git", "branch"], stderr=STDOUT, stdout=open(os.devnull, "w")) != 0:
    #     # If we aren't inside a git repo, set to the package version
    #     run_dict["git_commit"] = str(
    #         pkg_resources.get_distribution("c4.avazu_ctr_prediction")
    #     )
    # else:
    #     run_dict["git_commit"] = (
    #         spanner.utils.git_sha_short().decode("utf-8").strip("\n")
    #     )

    return run_dict


def finalise_run_and_log_to_resultsdb(run_dict, metrics={}, merge=False):
    """
    Create records of results and log to ResultsDB.

    Parameters
    ----------
    run_dict : dict
        Run dictionary of configurations
    metrics : dict
        Dictionary of evaluation performance metrics
    merge : bool
        if True, any uuid that is passed that is already
        in the database will be overwritten.

    Returns
    -------
    None

    """
    logger.info("Starting writing run to results database.")

    if run_dict["conf"]["model"].get("module", "") == "tpot":
        run_dict["conf"]["model"].pop("params")

    run_dict["results"] = metrics
    run_dict["end_ts"] = datetime.datetime.now()
    # TODO: save run metadata
    logger.info("Finished writing run results.")
