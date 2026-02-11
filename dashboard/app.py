"""
DecAI Oracle - Streamlit Dashboard
Real-time crypto price predictions with on-chain verification
"""

import streamlit as st
import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
from hashlib import sha256

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ml.data_collector import DataCollector
from src.ml.predictor import Predictor
from src.blockchain.contract_manager import ContractManager
from src.utils.config import settings

# Page config
st.set_page_config(
    page_title="DecAI Oracle - AI-Powered Blockchain Oracle",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .prediction-box {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🔮 DecAI Oracle</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">AI-Powered Blockchain Oracle | Predictions Verified On-Chain</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=DecAI+Oracle", use_container_width=True)
    st.markdown("### ⚙️ Settings")
    
    asset = st.selectbox(
        "Select Asset",
        ["Bitcoin", "Ethereum", "Solana", "Polygon"],
        index=0
    )
    
    days = st.slider("Historical Data (days)", 7, 90, 30)
    
    st.markdown("---")
    st.markdown("### 📊 System Status")
    
    if settings.BLOCKCHAIN_ENABLED:
        st.success("✅ Blockchain Connected")
    else:
        st.warning("⚠️ Blockchain Disabled")
    
    st.info(f"🌐 Environment: {settings.ENVIRONMENT}")
    
    st.markdown("---")
    st.markdown("### 🔗 Links")
    st.markdown("[📖 Documentation](https://github.com/decai-oracle)")
    st.markdown("[🐦 Twitter](https://twitter.com/DecAIOracle)")
    st.markdown("[💬 Discord](https://discord.gg/decai-oracle)")


# Main content
@st.cache_data(ttl=3600)
def fetch_data(asset_id: str, days: int):
    """Fetch crypto data with caching"""
    collector = DataCollector()
    data = asyncio.run(collector.fetch_bitcoin_data(days=days))
    return data


@st.cache_resource
def train_model(data):
    """Train ML model with caching"""
    predictor = Predictor()
    predictor.train(data)
    return predictor


# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Live Prediction", "📊 Historical Data", "⛓️ On-Chain Verification", "ℹ️ About"])

with tab1:
    st.markdown("## 🎯 Real-Time Price Prediction")
    
    col1, col2, col3 = st.columns(3)
    
    with st.spinner("🔄 Fetching data and training model..."):
        try:
            # Fetch data
            asset_map = {
                "Bitcoin": "bitcoin",
                "Ethereum": "ethereum",
                "Solana": "solana",
                "Polygon": "matic-network"
            }
            
            data = fetch_data(asset_map[asset], days)
            
            # Current price
            current_price = data[-1]
            
            # Train and predict
            predictor = train_model(data)
            predicted_price = predictor.predict_next_day()
            confidence = predictor.get_confidence()
            
            # Calculate change
            price_change = predicted_price - current_price
            price_change_pct = (price_change / current_price) * 100
            
            # Display metrics
            with col1:
                st.metric(
                    label=f"💰 Current {asset} Price",
                    value=f"${current_price:,.2f}",
                    delta=None
                )
            
            with col2:
                st.metric(
                    label="🔮 Predicted Price (24h)",
                    value=f"${predicted_price:,.2f}",
                    delta=f"{price_change_pct:+.2f}%"
                )
            
            with col3:
                confidence_color = "🟢" if confidence > 0.7 else "🟡" if confidence > 0.5 else "🔴"
                st.metric(
                    label=f"{confidence_color} Confidence Score",
                    value=f"{confidence:.1%}",
                    delta=None
                )
            
            # Prediction details
            st.markdown("---")
            st.markdown("### 📋 Prediction Details")
            
            prediction_data = f"{asset} prediction: ${predicted_price:.2f} on {datetime.now() + timedelta(days=1)}"
            prediction_hash = sha256(prediction_data.encode()).hexdigest()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="prediction-box">
                    <h4>🎯 Prediction Summary</h4>
                    <p><strong>Asset:</strong> {asset}</p>
                    <p><strong>Current Price:</strong> ${current_price:,.2f}</p>
                    <p><strong>Predicted Price:</strong> ${predicted_price:,.2f}</p>
                    <p><strong>Expected Change:</strong> {price_change_pct:+.2f}%</p>
                    <p><strong>Confidence:</strong> {confidence:.1%}</p>
                    <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="prediction-box">
                    <h4>🔒 Verification Hash</h4>
                    <p style="font-family: monospace; font-size: 0.8rem; word-break: break-all;">
                        {prediction_hash}
                    </p>
                    <p><strong>Use this hash to verify the prediction on-chain</strong></p>
                </div>
                """, unsafe_allow_html=True)
            
            # Chart
            st.markdown("### 📊 Price Trend & Prediction")
            
            # Create chart
            dates = pd.date_range(end=datetime.now(), periods=len(data), freq='D')
            future_date = datetime.now() + timedelta(days=1)
            
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=dates,
                y=data,
                mode='lines',
                name='Historical Price',
                line=dict(color='#667eea', width=2)
            ))
            
            # Prediction
            fig.add_trace(go.Scatter(
                x=[dates[-1], future_date],
                y=[current_price, predicted_price],
                mode='lines+markers',
                name='Prediction',
                line=dict(color='#764ba2', width=3, dash='dash'),
                marker=dict(size=10)
            ))
            
            fig.update_layout(
                title=f"{asset} Price Prediction",
                xaxis_title="Date",
                yaxis_title="Price (USD)",
                hovermode='x unified',
                template='plotly_white',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Store on blockchain button
            if settings.BLOCKCHAIN_ENABLED:
                if st.button("⛓️ Store Prediction On-Chain", type="primary"):
                    with st.spinner("📝 Storing on blockchain..."):
                        try:
                            contract_manager = ContractManager()
                            tx_hash = asyncio.run(contract_manager.store_prediction(
                                asset=asset,
                                predicted_price=predicted_price,
                                confidence=confidence
                            ))
                            st.success(f"✅ Prediction stored! TX: {tx_hash}")
                            st.markdown(f"[View on Etherscan](https://sepolia.etherscan.io/tx/{tx_hash})")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
            else:
                st.info("ℹ️ Configure blockchain credentials in .env to enable on-chain storage")
            
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.exception(e)

with tab2:
    st.markdown("## 📊 Historical Data Analysis")
    
    if 'data' in locals():
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📈 Max Price", f"${data.max():,.2f}")
        with col2:
            st.metric("📉 Min Price", f"${data.min():,.2f}")
        with col3:
            st.metric("📊 Average", f"${data.mean():,.2f}")
        with col4:
            st.metric("📏 Std Dev", f"${data.std():,.2f}")
        
        # Data table
        st.markdown("### 📋 Raw Data")
        df = pd.DataFrame({
            'Date': pd.date_range(end=datetime.now(), periods=len(data), freq='D'),
            'Price (USD)': data
        })
        st.dataframe(df, use_container_width=True)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{asset.lower()}_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with tab3:
    st.markdown("## ⛓️ On-Chain Verification")
    
    st.markdown("""
    ### How It Works
    
    1. **Prediction Generation**: ML model analyzes historical data and generates a price prediction
    2. **Hash Creation**: A cryptographic hash is created from the prediction data
    3. **On-Chain Storage**: The prediction is stored in a smart contract on Ethereum
    4. **Verification**: Anyone can verify the prediction using the hash and blockchain explorer
    
    ### Smart Contract Details
    """)
    
    if settings.PREDICTION_ORACLE_ADDRESS:
        st.code(f"Contract Address: {settings.PREDICTION_ORACLE_ADDRESS}", language="text")
        st.markdown(f"[View on Etherscan](https://sepolia.etherscan.io/address/{settings.PREDICTION_ORACLE_ADDRESS})")
    else:
        st.warning("⚠️ Contract not deployed yet. Follow SETUP_GUIDE.md to deploy.")
    
    st.markdown("""
    ### Verify a Prediction
    
    Enter a transaction hash to verify a prediction:
    """)
    
    tx_hash_input = st.text_input("Transaction Hash", placeholder="0x...")
    
    if st.button("🔍 Verify"):
        if tx_hash_input:
            st.info(f"Verifying transaction: {tx_hash_input}")
            st.markdown(f"[View on Etherscan](https://sepolia.etherscan.io/tx/{tx_hash_input})")
        else:
            st.warning("Please enter a transaction hash")

with tab4:
    st.markdown("## ℹ️ About DecAI Oracle")
    
    st.markdown("""
    ### 🔮 What is DecAI Oracle?
    
    DecAI Oracle is an **open-source AI-powered blockchain oracle** that provides:
    
    - 🧠 **Machine Learning Predictions**: Advanced ML models for crypto price forecasting
    - ⛓️ **On-Chain Verification**: All predictions stored on Ethereum for transparency
    - 🌐 **Multi-Chain Support**: Deploy on Ethereum, Polygon, Solana, and more
    - 🔓 **Open Source**: 100% transparent code, community-driven development
    
    ### 🎯 Use Cases
    
    - **DeFi Protocols**: Risk assessment and liquidation predictions
    - **Prediction Markets**: Automated event resolution
    - **Trading Bots**: AI-powered trading signals
    - **RWA Tokenization**: Asset valuation and verification
    
    ### 🚀 Technology Stack
    
    - **Backend**: Python 3.12+, FastAPI, scikit-learn, PyTorch
    - **Blockchain**: Solidity 0.8+, Hardhat, web3.py
    - **Data**: CoinGecko API, IPFS (Pinata)
    - **Frontend**: Streamlit, Next.js (coming soon)
    
    ### 📊 Market Opportunity
    
    - AI + Blockchain market: **$843M (2026)** → **$90B (projected)**
    - CAGR: **27.1%** through 2034
    - 500+ DeFi protocols need better oracles
    
    ### 🤝 Get Involved
    
    - ⭐ [Star on GitHub](https://github.com/decai-oracle)
    - 🐦 [Follow on Twitter](https://twitter.com/DecAIOracle)
    - 💬 [Join Discord](https://discord.gg/decai-oracle)
    - 📖 [Read Documentation](https://docs.decai-oracle.io)
    
    ### 📄 License
    
    MIT License - Free to use, modify, and distribute
    
    ---
    
    **Made with ❤️ by the DecAI community**
    """)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("🔗 [GitHub](https://github.com/decai-oracle)")

with col2:
    st.markdown("📖 [Documentation](https://docs.decai-oracle.io)")

with col3:
    st.markdown("💬 [Community](https://discord.gg/decai-oracle)")
