"""Models configuration for each segment."""
from typing import Union

from avazu_ctr_prediction.configuration import load_conf
from avazu_ctr_prediction.constants import CONF_PATH
from avazu_ctr_prediction.exceptions import MissingConfigurationParamException


def get_segment_parameter(segment: str, param: str) -> Union[str, float, dict]:
    """Extract the matching value for the segment parameter raise an error if can't find it."""
    try:
        return segments[segment][param]
    except KeyError:
        raise MissingConfigurationParamException(
            f"Can't find the parameter {param} in conf/segments_model_conf.py"
        )


segments = load_conf(CONF_PATH)
