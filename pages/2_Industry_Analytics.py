import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Industry Analytics",
    page_icon="🏭",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/startup_data.csv")

df = load_data()

st.title("🏭 Industry Analytics")

industry_summary = (
    df.groupby("Industry")
    .agg({
        "Funding Amount (M USD)": "mean",
        "Valuation (M USD)": "mean",
        "Revenue (M USD)": "mean",
        "Employees": "mean"
    })
    .reset_index()
)

col1,col2 = st.columns(2)

with col1:
    fig = px.bar(
        industry_summary,
        x="Industry",
        y="Funding Amount (M USD)",
        color="Industry",
        title="Average Funding by Industry"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        industry_summary,
        x="Industry",
        y="Valuation (M USD)",
        color="Industry",
        title="Average Valuation by Industry"
    )
    st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(
    df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Revenue (M USD)",
    hover_name="Startup Name",
    title="Industry Valuation Landscape"
)

st.plotly_chart(fig, use_container_width=True)

fig = px.treemap(
    df,
    path=["Industry"],
    values="Revenue (M USD)",
    title="Revenue Contribution by Industry"
)

st.plotly_chart(fig, use_container_width=True)
