"""Custom exceptions.

All the exceptions raised by the code in avazu_ctr_prediction.* should derive from Avazu-Ctr-PredictionException
"""


class AvazuCtrPredictionException(Exception):
    """Mother class for common avazu_ctr_prediction exceptions."""

    pass


class MissingModelException(AvazuCtrPredictionException):
    """Exception raised when a parameter cannot be found in the configuration."""

    pass


class MissingConfigurationParamException(AvazuCtrPredictionException):
    """Exception raised when a parameter cannot be found in the configuration."""

    pass
