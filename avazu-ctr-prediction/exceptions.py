"""Custom exceptions.

All the exceptions raised by the code in avazu-ctr-prediction.* should derive from Avazu-Ctr-PredictionException
"""


class AvazuCtrPredictionException(Exception):
    """Mother class for common avazu-ctr-prediction exceptions."""

    pass


class MissingConfigurationParamException(AvazuCtrPredictionException):
    """Exception raised when a parameter cannot be found in the configuration."""

    pass
