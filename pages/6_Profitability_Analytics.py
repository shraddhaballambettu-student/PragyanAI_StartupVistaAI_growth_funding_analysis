import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Profitability Analytics",
    page_icon="💹",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/startup_data.csv")

df = load_data()

st.title("💹 Profitability Analytics")

industry_profit = (
    df.groupby("Industry")
    ["Profitable"]
    .mean()
    .reset_index()
)

industry_profit["Profitable"] *= 100

fig = px.bar(
    industry_profit,
    x="Industry",
    y="Profitable",
    color="Industry",
    title="Industry Profitability Rate"
)

st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(
    df,
    x="Revenue (M USD)",
    y="Valuation (M USD)",
    color="Profitable",
    size="Employees",
    hover_name="Startup Name"
)

st.plotly_chart(fig, use_container_width=True)

df["Revenue Efficiency"] = (
    df["Revenue (M USD)"]
    /
    df["Funding Amount (M USD)"]
)

fig = px.box(
    df,
    x="Industry",
    y="Revenue Efficiency",
    color="Industry"
)

st.plotly_chart(fig, use_container_width=True)
