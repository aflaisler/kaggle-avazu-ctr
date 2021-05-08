"""Store constant values such as filepaths."""

import pkg_resources

BUCKET = "aws-c4-bdap-ds-development"
KEY = "avazu_ctr_prediction"
PATH = f"s3://{BUCKET}/{KEY}"
PKG_PATH = pkg_resources.resource_filename("avazu_ctr_prediction", "")
CONF_PATH = f"{PKG_PATH}/conf/model.toml"

RANDOM_STATE = 42

# Preprocessing
FEATURES = ["C17",
            "C14"]

ALL_FEATURES = ["C1",
                "C14",
                "C15",
                "C16",
                "C17",
                "C18",
                "C19",
                "C20",  # removed for now as low signal and many missing entries
                "C21",
                "app_category",
                "app_domain",
                "app_id",
                "banner_pos",
                "device_conn_type",
                "device_id",
                "device_model",
                "device_type",
                "hour",
                "site_category",
                "site_domain",
                "site_id",
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
