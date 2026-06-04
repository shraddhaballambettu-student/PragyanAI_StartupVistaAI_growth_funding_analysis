import streamlit as st
import pandas as pd

from utils.data_loader import (
    load_and_prepare_data,
    get_kpis,
    generate_ai_insights
)

from components.kpis import display_kpis

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Startup Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOAD DATA
# =====================================================

df = load_and_prepare_data(
    "data/startup_data.csv"
)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🚀 Startup Analytics")

    st.markdown("---")

    st.markdown("### Navigation")

    st.page_link(
        "pages/1_Executive_Dashboard.py",
        label="Executive Dashboard",
        icon="📊"
    )

    st.page_link(
        "pages/2_Industry_Analytics.py",
        label="Industry Analytics",
        icon="🏭"
    )

    st.page_link(
        "pages/3_Funding_Insights.py",
        label="Funding Insights",
        icon="💰"
    )

    st.page_link(
        "pages/4_Valuation_Model.py",
        label="Valuation Model",
        icon="📈"
    )

    st.page_link(
        "pages/5_Regional_Analysis.py",
        label="Regional Analysis",
        icon="🌍"
    )

    st.page_link(
        "pages/6_Profitability_Analytics.py",
        label="Profitability Analytics",
        icon="💹"
    )

    st.page_link(
        "pages/7_AI_Insights.py",
        label="AI Insights",
        icon="🤖"
    )

    st.markdown("---")

    st.markdown("### Dataset Summary")

    st.write(f"Records: {len(df):,}")

# =====================================================
# HEADER
# =====================================================

st.title("🚀 Startup Intelligence Platform")

st.markdown(
"""
### Executive Analytics Platform

Analyze startup ecosystems using:

- Funding Analytics
- Industry Intelligence
- Regional Performance
- Profitability Metrics
- Valuation Prediction
- AI Generated Insights
"""
)

st.divider()

# =====================================================
# KPI SECTION
# =====================================================

display_kpis(df)

st.divider()

# =====================================================
# QUICK OVERVIEW
# =====================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("Dataset Information")

    st.write(
        f"""
        Total Startups: {len(df):,}

        Industries Covered: {df['Industry'].nunique()}

        Regions Covered: {df['Region'].nunique()}

        Average Startup Age:
        {round(df['Startup Age'].mean(),1)}
        """
    )

with col2:

    st.subheader("Startup Ecosystem")

    kpis = get_kpis(df)

    st.write(
        f"""
        Total Funding:
        ${kpis['total_funding']:,.0f}M

        Total Valuation:
        ${kpis['total_valuation']:,.0f}M

        Total Revenue:
        ${kpis['total_revenue']:,.0f}M
        """
    )

st.divider()

# =====================================================
# TOP STARTUPS
# =====================================================

st.subheader("🏆 Top 10 Startups by Valuation")

top_startups = (
    df.sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_startups[
        [
            "Startup Name",
            "Industry",
            "Region",
            "Funding Amount (M USD)",
            "Revenue (M USD)",
            "Valuation (M USD)"
        ]
    ],
    use_container_width=True
)

# =====================================================
# AI INSIGHTS
# =====================================================

st.divider()

st.subheader("🤖 AI Generated Insights")

insights = generate_ai_insights(df)

for insight in insights:

    st.success(insight)

# =====================================================
# INDUSTRY SUMMARY
# =====================================================

st.divider()

st.subheader("🏭 Industry Snapshot")

industry_summary = (
    df.groupby("Industry")
    .agg({
        "Funding Amount (M USD)": "mean",
        "Revenue (M USD)": "mean",
        "Valuation (M USD)": "mean"
    })
    .round(2)
)

st.dataframe(
    industry_summary,
    use_container_width=True
)

# =====================================================
# REGION SUMMARY
# =====================================================

st.divider()

st.subheader("🌍 Regional Snapshot")

region_summary = (
    df.groupby("Region")
    .agg({
        "Funding Amount (M USD)": "sum",
        "Revenue (M USD)": "sum",
        "Valuation (M USD)": "sum"
    })
    .round(2)
)

st.dataframe(
    region_summary,
    use_container_width=True
)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Startup Intelligence Platform | Streamlit + Plotly + Scikit-Learn"
)
