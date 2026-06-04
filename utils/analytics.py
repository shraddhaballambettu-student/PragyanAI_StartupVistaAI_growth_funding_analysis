import pandas as pd


def funding_summary(df):

    return {
        "total_funding":
        df["Funding Amount (M USD)"].sum(),

        "avg_funding":
        df["Funding Amount (M USD)"].mean(),

        "max_funding":
        df["Funding Amount (M USD)"].max()
    }


def valuation_summary(df):

    return {
        "total_valuation":
        df["Valuation (M USD)"].sum(),

        "avg_valuation":
        df["Valuation (M USD)"].mean(),

        "max_valuation":
        df["Valuation (M USD)"].max()
    }


def profitability_summary(df):

    return {
        "profitability_rate":
        (
            df["Profitable"].mean()
            * 100
        )
    }


def top_startups(df,n=10):

    return (
        df.sort_values(
            "Valuation (M USD)",
            ascending=False
        )
        .head(n)
    )


def top_industries(df):

    return (
        df.groupby("Industry")
        ["Valuation (M USD)"]
        .mean()
        .sort_values(
            ascending=False
        )
    )


def regional_performance(df):

    return (
        df.groupby("Region")
        .agg({
            "Funding Amount (M USD)":"sum",
            "Revenue (M USD)":"sum",
            "Valuation (M USD)":"sum"
        })
        .reset_index()
    )
