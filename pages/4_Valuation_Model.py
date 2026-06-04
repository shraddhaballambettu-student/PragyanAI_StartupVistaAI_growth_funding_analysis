import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

st.set_page_config(
    page_title="Valuation Model",
    page_icon="📈",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/startup_data.csv")

df = load_data()

st.title("📈 Startup Valuation Prediction")

features = [
    "Funding Amount (M USD)",
    "Revenue (M USD)",
    "Employees",
    "Funding Rounds",
    "Market Share (%)"
]

X = df[features]

y = df["Valuation (M USD)"]

X_train,X_test,y_train,y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

model.fit(X_train,y_train)

preds = model.predict(X_test)

score = r2_score(
    y_test,
    preds
)

st.metric(
    "Model Accuracy (R²)",
    round(score,3)
)

importance = pd.DataFrame({
    "Feature":features,
    "Importance":model.feature_importances_
})

fig = px.bar(
    importance.sort_values("Importance"),
    x="Importance",
    y="Feature",
    title="Feature Importance"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Predict Valuation")

c1,c2,c3 = st.columns(3)

funding = c1.number_input(
    "Funding",
    value=100.0
)

revenue = c2.number_input(
    "Revenue",
    value=50.0
)

employees = c3.number_input(
    "Employees",
    value=500
)

rounds = st.number_input(
    "Funding Rounds",
    value=5
)

share = st.slider(
    "Market Share (%)",
    0.0,
    100.0,
    10.0
)

prediction = model.predict([[
    funding,
    revenue,
    employees,
    rounds,
    share
]])

st.success(
    f"Predicted Valuation: ${prediction[0]:,.2f}M"
)
