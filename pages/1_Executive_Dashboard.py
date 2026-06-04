import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="🚀",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/startup_data.csv")
    return df

df = load_data()

# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------

df.columns = df.columns.str.strip()

current_year = 2026

if "Year Founded" in df.columns:
    df["Startup Age"] = current_year - df["Year Founded"]

if (
    "Revenue (M USD)" in df.columns
    and
    "Funding Amount (M USD)" in df.columns
):
    df["Revenue Efficiency"] = (
        df["Revenue (M USD)"] /
        df["Funding Amount (M USD)"]
    )

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

industry_filter = st.sidebar.multiselect(
    "Industry",
    options=df["Industry"].unique(),
    default=df["Industry"].unique()
)

region_filter = st.sidebar.multiselect(
    "Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

exit_filter = st.sidebar.multiselect(
    "Exit Status",
    options=df["Exit Status"].unique(),
    default=df["Exit Status"].unique()
)

df = df[
    (df["Industry"].isin(industry_filter))
    &
    (df["Region"].isin(region_filter))
    &
    (df["Exit Status"].isin(exit_filter))
]

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🚀 Executive Dashboard")

st.markdown(
"""
Comprehensive Startup Ecosystem Intelligence Dashboard
"""
)

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

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

avg_market_share = df[
    "Market Share (%)"
].mean()

profitability_rate = (
    df["Profitable"].mean() * 100
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
    "Market Share",
    f"{avg_market_share:.2f}%"
)

col6.metric(
    "Unicorns",
    unicorns
)

st.divider()

# --------------------------------------------------
# ROW 1
# --------------------------------------------------

col1,col2 = st.columns(2)

with col1:

    st.subheader("Funding Distribution")

    fig = px.histogram(
        df,
        x="Funding Amount (M USD)",
        nbins=40,
        color_discrete_sequence=["#3B82F6"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader("Valuation Distribution")

    fig = px.histogram(
        df,
        x="Valuation (M USD)",
        nbins=40,
        color_discrete_sequence=["#10B981"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# ROW 2
# --------------------------------------------------

col1,col2 = st.columns(2)

with col1:

    st.subheader("Industry Valuation")

    industry_val = (
        df.groupby("Industry")
        ["Valuation (M USD)"]
        .mean()
        .reset_index()
        .sort_values(
            "Valuation (M USD)",
            ascending=False
        )
    )

    fig = px.bar(
        industry_val,
        x="Industry",
        y="Valuation (M USD)",
        color="Industry"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader("Regional Valuation")

    region_val = (
        df.groupby("Region")
        ["Valuation (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        region_val,
        names="Region",
        values="Valuation (M USD)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# ROW 3
# --------------------------------------------------

st.subheader(
    "Funding vs Valuation Analysis"
)

fig = px.scatter(
    df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Revenue (M USD)",
    hover_name="Startup Name",
    size_max=40
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# ROW 4
# --------------------------------------------------

col1,col2 = st.columns(2)

with col1:

    st.subheader(
        "Top 15 Startups by Revenue"
    )

    top_rev = (
        df.sort_values(
            "Revenue (M USD)",
            ascending=False
        )
        .head(15)
    )

    fig = px.bar(
        top_rev,
        x="Startup Name",
        y="Revenue (M USD)",
        color="Industry"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader(
        "Top 15 Startups by Valuation"
    )

    top_val = (
        df.sort_values(
            "Valuation (M USD)",
            ascending=False
        )
        .head(15)
    )

    fig = px.bar(
        top_val,
        x="Startup Name",
        y="Valuation (M USD)",
        color="Industry"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# CORRELATION HEATMAP
# --------------------------------------------------

st.subheader(
    "Startup Metrics Correlation"
)

numeric_df = df.select_dtypes(
    include=np.number
)

corr = numeric_df.corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# SUNBURST ANALYTICS
# --------------------------------------------------

st.subheader(
    "Region → Industry Breakdown"
)

fig = px.sunburst(
    df,
    path=["Region","Industry"],
    values="Valuation (M USD)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# AI INSIGHTS SECTION
# --------------------------------------------------

st.subheader("🤖 Executive Insights")

highest_industry = (
    df.groupby("Industry")
    ["Valuation (M USD)"]
    .mean()
    .idxmax()
)

highest_region = (
    df.groupby("Region")
    ["Valuation (M USD)"]
    .sum()
    .idxmax()
)

highest_revenue = (
    df.loc[
        df["Revenue (M USD)"].idxmax(),
        "Startup Name"
    ]
)

highest_funding = (
    df.loc[
        df["Funding Amount (M USD)"].idxmax(),
        "Startup Name"
    ]
)

st.success(
    f"🏆 Highest Valuation Industry: {highest_industry}"
)

st.success(
    f"🌍 Top Startup Region: {highest_region}"
)

st.success(
    f"💰 Highest Revenue Startup: {highest_revenue}"
)

st.success(
    f"🚀 Highest Funded Startup: {highest_funding}"
)

st.info(
    f"""
    Total Funding Raised:
    ${total_funding:,.0f}M
    """
)

st.info(
    f"""
    Total Ecosystem Valuation:
    ${total_valuation:,.0f}M
    """
)

st.info(
    f"""
    Profitability Rate:
    {profitability_rate:.2f}%
    """
)

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------

with st.expander("View Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )
