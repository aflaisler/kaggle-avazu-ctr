"""Store constant values such as filepaths."""

import pkg_resources

BUCKET = "aws-c4-bdap-ds-development"
KEY = "avazu_ctr_prediction"
PATH = f"s3://{BUCKET}/{KEY}"
PKG_PATH = pkg_resources.resource_filename("avazu_ctr_prediction", "")
CONF_PATH = f"{PKG_PATH}/conf/model.toml"
CAT_PATH = f"{PKG_PATH}/conf/category.toml"
PKG_DIR = "/".join(PKG_PATH.split("/")[:-1])
MODEL_PATH = f"{PKG_DIR}/models/ctr_classifier.pickle"
DATA_PATH = f"{PKG_DIR}/data"

RANDOM_STATE = 42

# Preprocessing
CAT_FREQ_MIN = 0.005

FEATURES = [
    "hour",
    "C1",
    "banner_pos",
    "site_id",
    "site_domain",
    "site_category",
    "app_id",
    "app_domain",
    "app_category",
    "device_id",
    "device_model",
    "device_type",
    "device_conn_type",
    "C14",
    "C15",
    "C16",
    "C17",
    "C18",
    "C19",
    "C20",
    "C21",
]

TARGET = "click"

CAT_FEATURES = [
    "C17",
    "C14",
    "site_id",
    "site_domain",
    "C21",
    "app_id",
    "C19",
    "C18",
    "app_domain",
]
