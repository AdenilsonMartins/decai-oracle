"""
DecAI Oracle Network — Dashboard
Real-time view of on-chain predictions, wallet status, and ML engine.
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import requests

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
load_dotenv(ROOT_DIR / ".env")

from web3 import Web3

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DecAI Oracle Network",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Global */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #0d1117 40%, #0f1923 100%);
    }
    
    /* Cards */
    .metric-card {
        background: linear-gradient(145deg, rgba(22,27,45,0.9), rgba(15,20,35,0.95));
        border: 1px solid rgba(56,189,248,0.15);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: rgba(56,189,248,0.4);
        box-shadow: 0 0 20px rgba(56,189,248,0.1);
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #f1f5f9;
        font-size: 1.8rem;
        font-weight: 700;
        font-family: 'SF Mono', 'Fira Code', monospace;
    }
    .metric-value.green { color: #34d399; }
    .metric-value.blue { color: #38bdf8; }
    .metric-value.amber { color: #fbbf24; }
    .metric-value.red { color: #f87171; }
    
    /* Header */
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .hero-sub {
        color: #64748b;
        font-size: 1rem;
    }
    
    /* Status badge */
    .status-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-online {
        background: rgba(52,211,153,0.15);
        color: #34d399;
        border: 1px solid rgba(52,211,153,0.3);
    }
    .status-offline {
        background: rgba(248,113,113,0.15);
        color: #f87171;
        border: 1px solid rgba(248,113,113,0.3);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #0f1923 100%);
        border-right: 1px solid rgba(56,189,248,0.1);
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Table */
    .prediction-row {
        background: rgba(22,27,45,0.6);
        border: 1px solid rgba(56,189,248,0.08);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Blockchain connection
# ─────────────────────────────────────────────
@st.cache_resource(ttl=60)
def get_web3_connection():
    """Cached Web3 connection"""
    rpc_url = os.getenv("SEPOLIA_RPC_URL")
    if not rpc_url:
        return None, None, None
    
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    contract_address = os.getenv("PREDICTION_ORACLE_ADDRESS")
    wallet_address = os.getenv("WALLET_ADDRESS")
    
    return w3, contract_address, wallet_address


def load_contract(w3, contract_address):
    """Load contract with ABI"""
    abi_path = ROOT_DIR / "contracts" / "artifacts" / "src" / "PredictionOracle.sol" / "PredictionOracle.json"
    
    if abi_path.exists():
        import json
        with open(abi_path) as f:
            artifact = json.load(f)
        return w3.eth.contract(
            address=Web3.to_checksum_address(contract_address),
            abi=artifact["abi"]
        )
    return None


def get_predictions(contract, count):
    """Fetch predictions from the contract"""
    predictions = []
    for i in range(1, count + 1):
        try:
            result = contract.functions.getPrediction(i).call()
            predictions.append({
                "id": i,
                "predicted_price": result[0] / 10**8,
                "timestamp": datetime.fromtimestamp(result[1]),
                "confidence": result[2] / 100,
                "verified": result[3],
                "predictor": result[4],
                "actual_price": result[5] / 10**8,
                "asset": result[6],
            })
        except Exception:
            break
    return predictions


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔮 DecAI Oracle Network")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["📊 Dashboard", "🔗 On-Chain Data", "🤖 ML Predict", "⚙️ System"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown(
        '<p style="color:#64748b;font-size:0.75rem;">Sepolia Testnet · v2.0</p>',
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────
# Data Loading
# ─────────────────────────────────────────────
w3, contract_address, wallet_address = get_web3_connection()
is_connected = w3.is_connected() if w3 else False
contract = load_contract(w3, contract_address) if (w3 and is_connected and contract_address) else None

balance_eth = 0.0
prediction_count = 0
chain_id = 0
latest_block = 0

if is_connected:
    try:
        balance_wei = w3.eth.get_balance(Web3.to_checksum_address(wallet_address))
        balance_eth = float(Web3.from_wei(balance_wei, "ether"))
        chain_id = w3.eth.chain_id
        latest_block = w3.eth.block_number
    except Exception:
        pass

if contract:
    try:
        prediction_count = contract.functions.predictionCount().call()
    except Exception:
        pass


# ─────────────────────────────────────────────
# PAGES
# ─────────────────────────────────────────────

if page == "📊 Dashboard":
    # Header
    st.markdown('<p class="hero-title">DecAI Oracle Network</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-sub">Decentralized AI-Powered Prediction Oracle on Ethereum</p>',
        unsafe_allow_html=True
    )
    
    # Status
    status_class = "status-online" if is_connected else "status-offline"
    status_text = "● Online" if is_connected else "● Offline"
    st.markdown(
        f'<span class="status-badge {status_class}">{status_text}</span>',
        unsafe_allow_html=True
    )
    st.markdown("")
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Wallet Balance</div>
            <div class="metric-value green">{balance_eth:.4f} ETH</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Predictions On-Chain</div>
            <div class="metric-value blue">{prediction_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Network</div>
            <div class="metric-value amber">Sepolia</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Latest Block</div>
            <div class="metric-value">{latest_block:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Contract Info
    st.markdown("### 📜 Contract")
    c1, c2 = st.columns(2)
    with c1:
        st.code(contract_address or "Not configured", language=None)
    with c2:
        if contract_address:
            st.markdown(
                f"[View on Etherscan ↗](https://sepolia.etherscan.io/address/{contract_address})"
            )
    
    # Recent Predictions Chart
    if contract and prediction_count > 0:
        st.markdown("### 📈 Prediction History")
        predictions = get_predictions(contract, min(prediction_count, 20))
        
        if predictions:
            df = pd.DataFrame(predictions)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["timestamp"],
                y=df["predicted_price"],
                mode="lines+markers",
                name="Predicted Price",
                line=dict(color="#38bdf8", width=2),
                marker=dict(size=8, color="#38bdf8"),
                fill="tozeroy",
                fillcolor="rgba(56,189,248,0.08)"
            ))
            
            if df["actual_price"].sum() > 0:
                fig.add_trace(go.Scatter(
                    x=df["timestamp"],
                    y=df["actual_price"],
                    mode="lines+markers",
                    name="Actual Price",
                    line=dict(color="#34d399", width=2, dash="dot"),
                    marker=dict(size=8, color="#34d399"),
                ))
            
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(gridcolor="rgba(56,189,248,0.06)"),
                yaxis=dict(gridcolor="rgba(56,189,248,0.06)", title="Price (USD)"),
                height=400,
                margin=dict(l=0, r=0, t=20, b=0),
                legend=dict(orientation="h", y=-0.15),
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Confidence gauge
            avg_conf = df["confidence"].mean()
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=avg_conf,
                title={"text": "Avg Confidence", "font": {"color": "#94a3b8"}},
                number={"suffix": "%", "font": {"color": "#f1f5f9"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#334155"},
                    "bar": {"color": "#38bdf8"},
                    "bgcolor": "rgba(15,20,35,0.8)",
                    "borderwidth": 1,
                    "bordercolor": "rgba(56,189,248,0.2)",
                    "steps": [
                        {"range": [0, 50], "color": "rgba(248,113,113,0.15)"},
                        {"range": [50, 75], "color": "rgba(251,191,36,0.15)"},
                        {"range": [75, 100], "color": "rgba(52,211,153,0.15)"},
                    ],
                }
            ))
            fig_gauge.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                height=250,
                margin=dict(l=30, r=30, t=50, b=0),
            )
            st.plotly_chart(fig_gauge, use_container_width=True)


elif page == "🔗 On-Chain Data":
    st.markdown('<p class="hero-title">On-Chain Predictions</p>', unsafe_allow_html=True)
    
    if not contract or prediction_count == 0:
        st.info("No predictions found on-chain yet.")
    else:
        predictions = get_predictions(contract, min(prediction_count, 50))
        
        for pred in reversed(predictions):
            verified_badge = "✅ Verified" if pred["verified"] else "⏳ Pending"
            verified_color = "#34d399" if pred["verified"] else "#fbbf24"
            
            st.markdown(f"""
            <div class="prediction-row">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="color:#38bdf8;font-weight:700;font-size:1.1rem;">#{pred['id']}</span>
                        <span style="color:#94a3b8;margin-left:12px;">{pred['asset']}</span>
                    </div>
                    <span style="color:{verified_color};font-size:0.85rem;">{verified_badge}</span>
                </div>
                <div style="display:flex;gap:32px;margin-top:12px;">
                    <div>
                        <span style="color:#64748b;font-size:0.75rem;">PREDICTED</span><br>
                        <span style="color:#f1f5f9;font-size:1.1rem;font-weight:600;">${pred['predicted_price']:,.2f}</span>
                    </div>
                    <div>
                        <span style="color:#64748b;font-size:0.75rem;">CONFIDENCE</span><br>
                        <span style="color:#38bdf8;font-size:1.1rem;font-weight:600;">{pred['confidence']:.1f}%</span>
                    </div>
                    <div>
                        <span style="color:#64748b;font-size:0.75rem;">TIME</span><br>
                        <span style="color:#94a3b8;font-size:0.9rem;">{pred['timestamp'].strftime('%Y-%m-%d %H:%M')}</span>
                    </div>
                </div>
                <div style="margin-top:8px;">
                    <span style="color:#475569;font-size:0.7rem;font-family:monospace;">{pred['predictor']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


elif page == "🤖 ML Predict":
    st.markdown('<p class="hero-title">ML Prediction Engine</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-sub">Generate a new prediction using the local API</p>',
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        asset = st.selectbox("Asset", ["bitcoin", "ethereum", "solana"])
    with col2:
        days = st.slider("Days of data", 7, 90, 30)
    with col3:
        horizon = st.selectbox("Horizon", [12, 24, 48, 72], index=1)
    
    if st.button("🔮 Generate Prediction", use_container_width=True, type="primary"):
        with st.spinner("Running ML engine..."):
            try:
                resp = requests.post(
                    "http://localhost:8000/api/v2/predict",
                    json={"asset_id": asset, "days_back": days, "horizon_hours": horizon},
                    timeout=30
                )
                
                if resp.status_code == 200:
                    data = resp.json()
                    
                    st.markdown("")
                    r1, r2, r3 = st.columns(3)
                    
                    with r1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Predicted Price</div>
                            <div class="metric-value green">${data['predicted_price']:,.2f}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with r2:
                        conf = data["confidence"] * 100
                        color = "green" if conf > 80 else "amber" if conf > 60 else "red"
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Confidence</div>
                            <div class="metric-value {color}">{conf:.1f}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with r3:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Model</div>
                            <div class="metric-value blue">{data['model_version']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("")
                    st.success(f"Prediction generated at {data['timestamp']}")
                else:
                    st.error(f"API returned {resp.status_code}: {resp.text}")
                    
            except requests.ConnectionError:
                st.error("❌ API not running. Start with: `python -m uvicorn src.api.main:app --port 8000`")
            except Exception as e:
                st.error(f"❌ Error: {e}")


elif page == "⚙️ System":
    st.markdown('<p class="hero-title">System Status</p>', unsafe_allow_html=True)
    
    # Connection status
    st.markdown("### 🔗 Blockchain")
    s1, s2, s3 = st.columns(3)
    
    with s1:
        status = "🟢 Connected" if is_connected else "🔴 Disconnected"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">RPC Status</div>
            <div class="metric-value {'green' if is_connected else 'red'}">{status}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with s2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Chain ID</div>
            <div class="metric-value blue">{chain_id}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with s3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Block Height</div>
            <div class="metric-value">{latest_block:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # API Health
    st.markdown("### 🖥️ API")
    try:
        health = requests.get("http://localhost:8000/api/v2/health", timeout=3).json()
        st.markdown(f"""
        <div class="metric-card" style="text-align:left;">
            <div style="display:flex;justify-content:space-between;">
                <span style="color:#94a3b8;">Status</span>
                <span style="color:#34d399;font-weight:600;">✅ {health['status']}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:8px;">
                <span style="color:#94a3b8;">Version</span>
                <span style="color:#f1f5f9;">{health['version']}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:8px;">
                <span style="color:#94a3b8;">Blockchain</span>
                <span style="color:{'#34d399' if health['blockchain_connected'] else '#f87171'};">
                    {'Connected' if health['blockchain_connected'] else 'Disconnected'}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        st.warning("⚠️ API is not running on localhost:8000")
    
    st.markdown("")
    
    # Addresses
    st.markdown("### 🔑 Addresses")
    st.markdown(f"""
    <div class="metric-card" style="text-align:left;">
        <div style="margin-bottom:12px;">
            <span style="color:#94a3b8;font-size:0.8rem;">CONTRACT</span><br>
            <code style="color:#38bdf8;font-size:0.85rem;">{contract_address or 'Not set'}</code>
        </div>
        <div>
            <span style="color:#94a3b8;font-size:0.8rem;">WALLET</span><br>
            <code style="color:#34d399;font-size:0.85rem;">{wallet_address or 'Not set'}</code>
        </div>
    </div>
    """, unsafe_allow_html=True)
