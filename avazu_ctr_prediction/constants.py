"""Store constant values such as filepaths."""

import pkg_resources

BUCKET = "aws-c4-bdap-ds-development"
KEY = "avazu_ctr_prediction"
PATH = f"s3://{BUCKET}/{KEY}"
PKG_PATH = pkg_resources.resource_filename("avazu_ctr_prediction", "")
CONF_PATH = f"{PKG_PATH}/conf/model.toml"
