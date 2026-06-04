import pandas as pd
import numpy as np


def preprocess_data(df):

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
    )

    df.drop_duplicates(
        inplace=True
    )

    numeric_cols = (
        df.select_dtypes(
            include=np.number
        )
        .columns
    )

    for col in numeric_cols:
        df[col] = (
            df[col]
            .fillna(
                df[col].median()
            )
        )

    current_year = 2026

    if "Year Founded" in df.columns:

        df["Startup Age"] = (
            current_year -
            df["Year Founded"]
        )

    if (
        "Funding Amount (M USD)"
        in df.columns
        and
        "Revenue (M USD)"
        in df.columns
    ):

        df["Revenue Efficiency"] = (
            df["Revenue (M USD)"]
            /
            df["Funding Amount (M USD)"]
        )

    if (
        "Valuation (M USD)"
        in df.columns
        and
        "Revenue (M USD)"
        in df.columns
    ):

        df["Valuation Multiple"] = (
            df["Valuation (M USD)"]
            /
            df["Revenue (M USD)"]
        )

    return df
