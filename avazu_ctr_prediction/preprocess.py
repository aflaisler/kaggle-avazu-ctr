"""Prepare data for modelling tasks."""

import pandas as pd
import toml
from loguru import logger

from avazu_ctr_prediction.constants import CAT_PATH, CAT_FREQ_MIN


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
        logger.info(f"Mapping categories under {CAT_FREQ_MIN} for the column: {column}")
        df.loc[:, column] = (
            df[column]
            .map(
                lambda cat: f"{column}_rare" if cat not in map_col_cat[column] else cat
            )
            .astype(str)
        )

    return df
