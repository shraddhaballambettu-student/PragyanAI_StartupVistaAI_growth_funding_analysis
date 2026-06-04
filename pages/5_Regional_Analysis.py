import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Regional Analysis",
    page_icon="🌍",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/startup_data.csv")

df = load_data()

st.title("🌍 Regional Analysis")

region_metrics = (
    df.groupby("Region")
    .agg({
        "Funding Amount (M USD)":"sum",
        "Valuation (M USD)":"sum",
        "Revenue (M USD)":"sum"
    })
    .reset_index()
)

fig = px.bar(
    region_metrics,
    x="Region",
    y="Valuation (M USD)",
    color="Region",
    title="Regional Valuation"
)

st.plotly_chart(fig, use_container_width=True)

fig = px.sunburst(
    df,
    path=["Region","Industry"],
    values="Valuation (M USD)",
    title="Region → Industry Valuation"
)

st.plotly_chart(fig, use_container_width=True)

fig = px.treemap(
    df,
    path=["Region","Industry"],
    values="Revenue (M USD)"
)

st.plotly_chart(fig, use_container_width=True)
