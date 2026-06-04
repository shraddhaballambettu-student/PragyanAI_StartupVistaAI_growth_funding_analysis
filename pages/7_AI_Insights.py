import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Insights",
    page_icon="🤖",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/startup_data.csv")

df = load_data()

st.title("🤖 AI Generated Startup Insights")

top_industry = (
    df.groupby("Industry")
    ["Valuation (M USD)"]
    .mean()
    .idxmax()
)

top_region = (
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

highest_funded = (
    df.loc[
        df["Funding Amount (M USD)"].idxmax(),
        "Startup Name"
    ]
)

profit_rate = (
    df["Profitable"].mean()
    * 100
)

st.success(
    f"🏆 Highest Valuation Industry: {top_industry}"
)

st.success(
    f"🌍 Strongest Startup Region: {top_region}"
)

st.success(
    f"💰 Highest Revenue Startup: {highest_revenue}"
)

st.success(
    f"🚀 Highest Funded Startup: {highest_funded}"
)

st.info(
    f"Profitability Rate: {profit_rate:.2f}%"
)

st.subheader("Strategic Recommendations")

st.markdown("""
### Growth Opportunities

- Increase funding allocation to high-performing industries.
- Focus on regions with strong valuation growth.
- Improve revenue efficiency before scaling.
- Benchmark low-performing startups against industry leaders.
- Use valuation prediction models during investment screening.

### Investor View

- Identify undervalued startups.
- Monitor high-growth industries.
- Compare valuation-to-revenue multiples.
- Track profitability trends.
""")

st.subheader("Dataset Snapshot")

st.dataframe(df.head(50))
