"""
=========================================================
File: data_loader.py
Purpose: Load, Validate, Clean and Prepare Startup Data
=========================================================
"""

import pandas as pd
import numpy as np
import streamlit as st


# =====================================================
# REQUIRED COLUMNS
# =====================================================

REQUIRED_COLUMNS = [
    "Startup Name",
    "Industry",
    "Region",
    "Year Founded",
    "Funding Rounds",
    "Funding Amount (M USD)",
    "Valuation (M USD)",
    "Revenue (M USD)",
    "Employees",
    "Market Share (%)",
    "Profitable",
    "Exit Status"
]


# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data(show_spinner=False)
def load_data(
    file_path="data/startup_data.csv"
):
    """
    Load CSV dataset
    """

    try:

        df = pd.read_csv(file_path)

        df.columns = (
            df.columns
            .str.strip()
        )

        return df

    except FileNotFoundError:

        st.error(
            f"Dataset not found: {file_path}"
        )

        return pd.DataFrame()

    except Exception as e:

        st.error(
            f"Error loading data: {e}"
        )

        return pd.DataFrame()


# =====================================================
# VALIDATE DATASET
# =====================================================

def validate_data(df):

    missing_columns = []

    for col in REQUIRED_COLUMNS:

        if col not in df.columns:

            missing_columns.append(col)

    if len(missing_columns) > 0:

        st.error(
            f"""
            Missing Columns:

            {missing_columns}
            """
        )

        return False

    return True


# =====================================================
# CLEAN DATA
# =====================================================

@st.cache_data(show_spinner=False)
def clean_data(df):

    df = df.copy()

    # -----------------------------------------
    # Remove duplicates
    # -----------------------------------------

    df.drop_duplicates(
        inplace=True
    )

    # -----------------------------------------
    # Missing Values
    # -----------------------------------------

    numeric_columns = (
        df.select_dtypes(
            include=np.number
        )
        .columns
    )

    for col in numeric_columns:

        df[col] = (
            df[col]
            .fillna(
                df[col].median()
            )
        )

    object_columns = (
        df.select_dtypes(
            include="object"
        )
        .columns
    )

    for col in object_columns:

        df[col] = (
            df[col]
            .fillna("Unknown")
        )

    # -----------------------------------------
    # Profitable Column
    # -----------------------------------------

    if (
        "Profitable"
        in df.columns
    ):

        if (
            df["Profitable"].dtype
            == "object"
        ):

            df["Profitable"] = (
                df["Profitable"]
                .astype(str)
                .str.lower()
                .map({
                    "yes":1,
                    "no":0,
                    "true":1,
                    "false":0,
                    "1":1,
                    "0":0
                })
                .fillna(0)
            )

    return df


# =====================================================
# FEATURE ENGINEERING
# =====================================================

@st.cache_data(show_spinner=False)
def create_features(df):

    df = df.copy()

    current_year = 2026

    # -----------------------------------------
    # Startup Age
    # -----------------------------------------

    if (
        "Year Founded"
        in df.columns
    ):

        df["Startup Age"] = (
            current_year
            - df["Year Founded"]
        )

    # -----------------------------------------
    # Revenue Efficiency
    # -----------------------------------------

    if (
        "Revenue (M USD)"
        in df.columns
        and
        "Funding Amount (M USD)"
        in df.columns
    ):

        df["Revenue Efficiency"] = (
            df["Revenue (M USD)"]
            /
            df[
                "Funding Amount (M USD)"
            ]
            .replace(0,np.nan)
        )

    # -----------------------------------------
    # Valuation Multiple
    # -----------------------------------------

    if (
        "Valuation (M USD)"
        in df.columns
        and
        "Revenue (M USD)"
        in df.columns
    ):

        df["Valuation Multiple"] = (
            df["Valuation (M USD)"]
            /
            df[
                "Revenue (M USD)"
            ]
            .replace(0,np.nan)
        )

    # -----------------------------------------
    # Revenue Per Employee
    # -----------------------------------------

    if (
        "Employees"
        in df.columns
        and
        "Revenue (M USD)"
        in df.columns
    ):

        df["Revenue Per Employee"] = (
            df["Revenue (M USD)"]
            /
            df["Employees"]
            .replace(0,np.nan)
        )

    # -----------------------------------------
    # Funding Per Employee
    # -----------------------------------------

    if (
        "Employees"
        in df.columns
        and
        "Funding Amount (M USD)"
        in df.columns
    ):

        df["Funding Per Employee"] = (
            df[
                "Funding Amount (M USD)"
            ]
            /
            df["Employees"]
            .replace(0,np.nan)
        )

    # -----------------------------------------
    # Unicorn Flag
    # -----------------------------------------

    if (
        "Valuation (M USD)"
        in df.columns
    ):

        df["Unicorn"] = np.where(
            df["Valuation (M USD)"]
            >= 1000,
            "Yes",
            "No"
        )

    return df


# =====================================================
# FILTER DATA
# =====================================================

def filter_data(
    df,
    industries=None,
    regions=None,
    exit_status=None
):

    filtered_df = df.copy()

    if industries:

        filtered_df = (
            filtered_df[
                filtered_df["Industry"]
                .isin(industries)
            ]
        )

    if regions:

        filtered_df = (
            filtered_df[
                filtered_df["Region"]
                .isin(regions)
            ]
        )

    if exit_status:

        filtered_df = (
            filtered_df[
                filtered_df["Exit Status"]
                .isin(exit_status)
            ]
        )

    return filtered_df


# =====================================================
# KPI METRICS
# =====================================================

def get_kpis(df):

    kpis = {

        "total_startups":
        len(df),

        "total_funding":
        df[
            "Funding Amount (M USD)"
        ].sum(),

        "total_valuation":
        df[
            "Valuation (M USD)"
        ].sum(),

        "total_revenue":
        df[
            "Revenue (M USD)"
        ].sum(),

        "avg_market_share":
        df[
            "Market Share (%)"
        ].mean(),

        "profitability_rate":
        (
            df["Profitable"]
            .mean()
            * 100
        ),

        "unicorn_count":
        (
            df["Valuation (M USD)"]
            >= 1000
        ).sum()
    }

    return kpis


# =====================================================
# AI INSIGHTS
# =====================================================

def generate_ai_insights(df):

    insights = []

    try:

        top_industry = (
            df.groupby("Industry")
            ["Valuation (M USD)"]
            .mean()
            .idxmax()
        )

        insights.append(
            f"🏆 Highest valuation industry: {top_industry}"
        )

    except:
        pass

    try:

        top_region = (
            df.groupby("Region")
            ["Valuation (M USD)"]
            .sum()
            .idxmax()
        )

        insights.append(
            f"🌍 Strongest startup region: {top_region}"
        )

    except:
        pass

    try:

        highest_revenue = (
            df.loc[
                df[
                    "Revenue (M USD)"
                ].idxmax(),
                "Startup Name"
            ]
        )

        insights.append(
            f"💰 Highest revenue startup: {highest_revenue}"
        )

    except:
        pass

    try:

        highest_funding = (
            df.loc[
                df[
                    "Funding Amount (M USD)"
                ].idxmax(),
                "Startup Name"
            ]
        )

        insights.append(
            f"🚀 Highest funded startup: {highest_funding}"
        )

    except:
        pass

    try:

        profitability = (
            df["Profitable"]
            .mean()
            * 100
        )

        insights.append(
            f"📈 Profitability rate: {profitability:.2f}%"
        )

    except:
        pass

    return insights


# =====================================================
# COMPLETE PIPELINE
# =====================================================

@st.cache_data(show_spinner=True)
def load_and_prepare_data(
    file_path="data/startup_data.csv"
):

    df = load_data(file_path)

    if df.empty:

        return df

    if not validate_data(df):

        return pd.DataFrame()

    df = clean_data(df)

    df = create_features(df)

    return df
