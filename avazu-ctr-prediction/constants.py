"""Store constant values such as filepaths."""

import pkg_resources

BUCKET = "aws-c4-bdap-ds-development"
KEY = "avazu-ctr-prediction"
PATH = f"s3://{BUCKET}/{KEY}"
PKG_PATH = pkg_resources.resource_filename("avazu-ctr-prediction", "")
CONF_PATH = f"{PKG_PATH}/conf/model.toml"
