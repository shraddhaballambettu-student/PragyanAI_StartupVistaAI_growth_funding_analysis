import streamlit as st


def display_kpis(df):

    total_startups = len(df)

    total_funding = df[
        "Funding Amount (M USD)"
    ].sum()

    total_valuation = df[
        "Valuation (M USD)"
    ].sum()

    total_revenue = df[
        "Revenue (M USD)"
    ].sum()

    profitability = (
        df["Profitable"].mean()
        * 100
    )

    unicorns = len(
        df[
            df["Valuation (M USD)"] >= 1000
        ]
    )

    col1,col2,col3,col4,col5,col6 = st.columns(6)

    col1.metric(
        "Startups",
        f"{total_startups:,}"
    )

    col2.metric(
        "Funding",
        f"${total_funding:,.0f}M"
    )

    col3.metric(
        "Valuation",
        f"${total_valuation:,.0f}M"
    )

    col4.metric(
        "Revenue",
        f"${total_revenue:,.0f}M"
    )

    col5.metric(
        "Profitable %",
        f"{profitability:.2f}%"
    )

    col6.metric(
        "Unicorns",
        unicorns
    )
