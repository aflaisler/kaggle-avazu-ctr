"""Common package utilities."""
import pandas as pd
from typing import List


def check_columns(df: pd.DataFrame, columns: List[str]) -> None:
    """Check that the dataframe provided contains the expected columns."""

    try:
        assert set(columns).issubset(df.columns)
    except AssertionError:
        sym_difference = set(columns).difference(set(df.columns))
        raise KeyError(
            f"The column names of the dataset are not the one we are expecting. "
            f"The following are missing: {sym_difference}."
        )
