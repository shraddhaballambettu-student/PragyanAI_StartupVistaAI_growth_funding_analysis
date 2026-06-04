import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Funding Insights",
    page_icon="💰",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/startup_data.csv")

df = load_data()

st.title("💰 Funding Insights")

fig = px.histogram(
    df,
    x="Funding Amount (M USD)",
    nbins=40,
    title="Funding Distribution"
)

st.plotly_chart(fig, use_container_width=True)

fig = px.box(
    df,
    x="Industry",
    y="Funding Amount (M USD)",
    color="Industry",
    title="Funding Spread Across Industries"
)

st.plotly_chart(fig, use_container_width=True)

funding_region = (
    df.groupby("Region")
    ["Funding Amount (M USD)"]
    .sum()
    .reset_index()
)

fig = px.pie(
    funding_region,
    names="Region",
    values="Funding Amount (M USD)",
    title="Regional Funding Distribution"
)

st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(
    df,
    x="Funding Rounds",
    y="Funding Amount (M USD)",
    color="Industry",
    size="Valuation (M USD)",
    hover_name="Startup Name",
    title="Funding Rounds vs Funding"
)

st.plotly_chart(fig, use_container_width=True)

top_funded = (
    df.sort_values(
        "Funding Amount (M USD)",
        ascending=False
    )
    .head(20)
)

st.subheader("Top Funded Startups")

st.dataframe(top_funded)
