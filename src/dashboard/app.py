import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import asyncio
import json

from src.data.data_aggregator import MultiSourceAggregator
from src.ml.predictor import Predictor
from src.ml.data_collector import DataCollector
from src.blockchain.contract_manager import ContractManager

# Page Config
st.set_page_config(
    page_title="DecAI Oracle V2 | Premium Dashboard",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3e4259;
    }
    .status-card {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    h1, h2, h3 {
        color: #00ffcc !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔮 DecAI Oracle V2")
st.sidebar.markdown("---")
asset_id = st.sidebar.selectbox("Select Asset", ["bitcoin", "ethereum", "solana"])
days_back = st.sidebar.slider("Historical Days", 7, 90, 30)
update_btn = st.sidebar.button("Update Oracle Data", use_container_width=True)

# Initialize Core
@st.cache_resource
def get_core():
    return {
        "aggregator": MultiSourceAggregator(),
        "collector": DataCollector(),
        "contract": ContractManager()
    }

core = get_core()

async def fetch_dashboard_data(asset):
    # 1. Multi-source Price
    symbol_map = {"bitcoin": "BTC/USD", "ethereum": "ETH/USD", "solana": "SOL/USD"}
    price_data = await core["aggregator"].get_price(symbol_map[asset])
    
    # 2. Historical Data for Chart
    hist_prices = await core["collector"].fetch_asset_data(asset, days=days_back)
    
    # 3. ML Prediction
    predictor = Predictor()
    predictor.train(hist_prices)
    prediction = predictor.predict_next_day()
    confidence = predictor.get_confidence()
    
    return {
        "price_data": price_data,
        "hist_prices": hist_prices,
        "prediction": prediction,
        "confidence": confidence,
        "health": core["aggregator"].get_health_report()
    }

# App Layout
st.title("🛡️ Resilient DecAI Oracle Dashboard")
st.markdown(f"**Last Sync:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if 'data' not in st.session_state or update_btn:
    with st.spinner("Synchronizing with multiple data sources and blockchain..."):
        st.session_state.data = asyncio.run(fetch_dashboard_data(asset_id))

data = st.session_state.data

# Top Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Current Price (USD)", f"${data['price_data'].price:,.2f}", 
              delta=f"{data['price_data'].metadata.get('price_change_pct', 0):.2f}%")
with col2:
    st.metric("24h Prediction", f"${data['prediction']:,.2f}", 
              delta=f"{(data['prediction']/data['price_data'].price - 1)*100:+.2f}%")
with col3:
    st.metric("Confidence Score", f"{data['confidence']*100:.1f}%")
with col4:
    active_sources = data['health']['healthy_sources']
    st.metric("Healthy Sources", f"{active_sources}/3")

# Main Chart
st.subheader("📈 Price Prediction Horizon")
hist_df = pd.DataFrame(data['hist_prices'], columns=['Price'])
hist_df['Date'] = [datetime.now() - timedelta(hours=(len(data['hist_prices'])-i)) for i in range(len(data['hist_prices']))]

fig = go.Figure()
# Historical
fig.add_trace(go.Scatter(x=hist_df['Date'], y=hist_df['Price'], name="Market Price", line=dict(color='#00ffcc', width=2)))
# Prediction
pred_date = hist_df['Date'].iloc[-1] + timedelta(hours=24)
fig.add_trace(go.Scatter(x=[hist_df['Date'].iloc[-1], pred_date], 
                         y=[hist_df['Price'].iloc[-1], data['prediction']], 
                         name="AI Prediction", line=dict(color='#ff0066', width=3, dash='dot')))

fig.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=20, b=0), height=400,
                  xaxis_title="Time", yaxis_title="Price (USD)")
st.plotly_chart(fig, use_container_width=True)

# Grid Layout
c_left, c_right = st.columns([1, 1])

with c_left:
    st.subheader("🛡️ Resilience Health Report")
    for source in data['health']['sources']:
        color = "green" if source['status'] == "healthy" else "orange" if source['status'] == "degraded" else "red"
        st.markdown(f"""
        <div style="background-color: #1e2130; padding: 15px; border-radius: 8px; border-left: 5px solid {color}; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between;">
                <b>{source['name']}</b>
                <span>{source['success_rate']} success</span>
            </div>
            <div style="font-size: 0.8em; color: #888;">Response: {source['avg_response_time_ms']}ms | Status: {source['status'].upper()}</div>
        </div>
        """, unsafe_allow_html=True)

with c_right:
    st.subheader("⛓️ Blockchain Integrity")
    try:
        total_preds = core["contract"].contract.functions.predictionCount().call()
        is_connected = core["contract"].w3.is_connected()
        
        st.write(f"**Network:** Sepolia Testnet")
        st.write(f"**Contract Address:** `{core['contract'].contract.address}`")
        st.write(f"**Oracle Status:** {'🟢 ACTIVE' if is_connected else '🔴 DISCONNECTED'}")
        st.write(f"**Total Predictions Stored:** {total_preds}")
        
    except Exception as e:
        st.error(f"Blockchain module offline: {e}")

# Detailed Data Table
with st.expander("View Raw Aggregated Data"):
    st.json(data['price_data'].metadata)

st.sidebar.markdown("---")
st.sidebar.info("DecAI Oracle V2 - Enterprise Grade Resilience Layer Active.")
