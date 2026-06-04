def generate_insights(df):

    insights = []

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

    highest_funding = (
        df.loc[
            df["Funding Amount (M USD)"].idxmax(),
            "Startup Name"
        ]
    )

    insights.append(
        f"Highest valuation industry: {top_industry}"
    )

    insights.append(
        f"Top startup region: {top_region}"
    )

    insights.append(
        f"Highest revenue startup: {highest_revenue}"
    )

    insights.append(
        f"Highest funded startup: {highest_funding}"
    )

    return insights
