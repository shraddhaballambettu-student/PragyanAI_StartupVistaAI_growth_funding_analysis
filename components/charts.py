import plotly.express as px
import numpy as np


def funding_distribution(df):

    fig = px.histogram(
        df,
        x="Funding Amount (M USD)",
        nbins=40,
        title="Funding Distribution"
    )

    return fig


def valuation_distribution(df):

    fig = px.histogram(
        df,
        x="Valuation (M USD)",
        nbins=40,
        title="Valuation Distribution"
    )

    return fig


def funding_vs_valuation(df):

    fig = px.scatter(
        df,
        x="Funding Amount (M USD)",
        y="Valuation (M USD)",
        color="Industry",
        size="Revenue (M USD)",
        hover_name="Startup Name"
    )

    return fig


def region_sunburst(df):

    fig = px.sunburst(
        df,
        path=["Region","Industry"],
        values="Valuation (M USD)"
    )

    return fig


def region_treemap(df):

    fig = px.treemap(
        df,
        path=["Region","Industry"],
        values="Revenue (M USD)"
    )

    return fig


def correlation_heatmap(df):

    numeric_df = df.select_dtypes(
        include=np.number
    )

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=True
    )

    return fig


def industry_valuation(df):

    industry_val = (
        df.groupby("Industry")
        ["Valuation (M USD)"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        industry_val,
        x="Industry",
        y="Valuation (M USD)",
        color="Industry"
    )

    return fig
