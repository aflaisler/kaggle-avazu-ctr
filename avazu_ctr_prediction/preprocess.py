"""Prepare data for modelling tasks."""

import pandas as pd
import toml
from loguru import logger
from sklearn.base import BaseEstimator, TransformerMixin

from avazu_ctr_prediction.constants import CAT_PATH


def category_to_keep(df: pd.DataFrame, output_filepath: str, freq_min: float) -> None:
    """Save the category to keep."""
    d_final = {}
    for column in df.columns:
        logger.info(f"Finding categories to keep for {column}")
        freq = df[column].value_counts() / df.shape[0]
        d = {column: list(freq[freq > freq_min].index)}
        d_final.update(d)
    logger.info(f"Saving column category to keep here: {output_filepath}")
    with open(output_filepath, "w") as conf_file:
        toml.dump(d_final, conf_file)


def map_rare_category(df: pd.DataFrame) -> pd.DataFrame:
    """Replace low frequency categories with <column>_rare."""
    with open(CAT_PATH) as conf_file:
        map_col_cat = toml.load(conf_file)
    for column in df.columns:
        logger.info(f"Mapping rare categories for the column: {column}")
        # TODO: create a new dataframe object?
        df.loc[:, column] = (
            df.loc[:, column]
            .map(
                lambda cat: f"{column}_rare" if cat not in map_col_cat[column] else cat
            )
            .astype(str)
        )

    return df


class ColumnFilter(BaseEstimator, TransformerMixin):
    def __init__(self, columns_to_keep):
        self.columns_to_keep = columns_to_keep

    def transform(self, X):
        return X[self.columns_to_keep]

    def fit(self, X, y=None, **fit_params):
        return self

    def fit_transform(self, X, y=None, **fit_params):
        return X[self.columns_to_keep]
