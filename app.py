import streamlit as st
import pandas as pd
from forecast import forecast_sales
from utils import calculate_risk
from decision import make_decision
from llm import get_ai_advice

st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #1c1f26;
}

.stMetric {
    text-align: center;
    font-size: 20px;
}

div.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="IntelliStock", layout="wide")

st.title("📦 IntelliStock – Smart Inventory Decision System")
st.subheader("📊 AI-Powered Inventory Insights Dashboard")

# Load data
data = pd.read_csv("data.csv")

# Sidebar
page = st.sidebar.selectbox("Menu", ["Dashboard", "Forecast", "AI Advisor"])

product = st.selectbox("Select Product", data['product'].unique())
filtered = data[data['product'] == product]

# Get latest stock
stock = int(filtered['stock'].iloc[-1])

# Forecast
forecast = forecast_sales(filtered)
predicted = forecast['yhat'].iloc[-1]

# What-if simulation
growth = st.slider("📈 Demand Increase %", 0, 100, 0)
predicted = predicted * (1 + growth/100)

# Risk + Decision
risk = calculate_risk(predicted, stock)
decision = make_decision(predicted, stock)

# Dashboard
if page == "Dashboard":
    col1, col2, col3 = st.columns(3)

    col1.metric("Predicted Demand", f"{predicted:.2f}")
    col2.metric("Current Stock", stock)
    col3.metric("Risk Level", risk)

    st.subheader("📦 Decision")
    st.info(decision)

    # Risk display
    if risk == "HIGH":
        st.error("⚠️ Immediate Action Required!")
    elif risk == "MEDIUM":
        st.warning("⚡ Monitor Closely")
    else:
        st.success("✅ Stock is Safe")

    # Loss estimation
    loss = max(0, predicted - stock) * 100
    st.metric("💰 Potential Loss", f"₹{int(loss)}")

# Forecast page
elif page == "Forecast":
    st.subheader("📊 Sales Forecast")
    st.line_chart(forecast.set_index('ds')['yhat'])

# AI Advisor
elif page == "AI Advisor":
    st.subheader("🤖 AI Decision Advisor")

    summary = f"""
    Product: {product}
    Predicted Demand: {predicted}
    Stock: {stock}
    Risk: {risk}
    Decision: {decision}
    """

    if st.button("Get AI Advice"):
        advice = get_ai_advice(summary)
        st.success(advice)