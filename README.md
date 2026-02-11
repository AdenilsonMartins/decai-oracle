# 🔮 DecAI Oracle

> Decentralized AI-Powered Prediction Oracle on Ethereum

[![Solidity](https://img.shields.io/badge/Solidity-0.8.24-blue)](https://soliditylang.org/)
[![Python](https://img.shields.io/badge/Python-3.12+-green)](https://python.org/)
[![Sepolia](https://img.shields.io/badge/Network-Sepolia-yellow)](https://sepolia.etherscan.io/)
[![License](https://img.shields.io/badge/License-MIT-purple)](./LICENSE)

DecAI Oracle is a decentralized, AI-powered price prediction system with on-chain verification.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DecAI Oracle System                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Data Sources  │───▶│  ML Engine   │───▶│  Blockchain  │  │
│  │              │    │              │    │              │  │
│  │ • Binance    │    │ • Training   │    │ • Ethereum   │  │
│  │ • CoinGecko  │    │ • Prediction │    │ • Sepolia    │  │
│  │ • CoinCap    │    │ • Validation │    │ • Verified   │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                    │                   │          │
│         └────────────────────┼───────────────────┘          │
│                              │                              │
│                     ┌────────▼────────┐                     │
│                     │   FastAPI + UI  │                     │
│                     │ Dashboard/API   │                     │
│                     └─────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## 🛡️ Features

- **Multi-Source Aggregation**: Real-time price consensus from Binance, CoinGecko, and CoinCap
- **ML Prediction Engine**: Linear regression with confidence scoring
- **On-Chain Storage**: Predictions stored and verifiable on Ethereum (Sepolia)
- **Hardened Smart Contract**: AccessControl, Pausable, ReentrancyGuard, Custom Errors
- **FastAPI Backend**: Production-ready API with rate limiting and monitoring
- **Streamlit Dashboard**: Real-time visualization of predictions and blockchain data
- **Prometheus Metrics**: Built-in observability

## 📜 Smart Contract

| Property | Value |
|----------|-------|
| **Network** | Sepolia Testnet |
| **Address** | `0x0E8B23cb4Dcdd2AA3bc7a5db0070a2E9CB1c4252` |
| **Etherscan** | [Verified ✅](https://sepolia.etherscan.io/address/0x0E8B23cb4Dcdd2AA3bc7a5db0070a2E9CB1c4252#code) |
| **Gas (store)** | ~109-126k |

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+

### Installation

```bash
# Clone
git clone https://github.com/AdenilsonMartins/decai-oracle.git
cd decai-oracle

# Python dependencies
pip install -r requirements.txt

# Smart contract dependencies
cd contracts && npm install && cd ..

# Environment
cp .env.example .env
# Edit .env with your API keys
```

### Run

```bash
# API Server
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000

# Dashboard (separate terminal)
streamlit run dashboard/app.py --server.port 8501

# Run all tests
python -m pytest tests/ -v
cd contracts && npx hardhat test
```

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v2/health` | System health check |
| `POST` | `/api/v2/predict` | Generate ML prediction |
| `GET` | `/api/v2/stats/{address}` | Predictor statistics |
| `GET` | `/api/v2/docs` | Swagger documentation |
| `GET` | `/metrics` | Prometheus metrics |

## 🧪 Tests

| Suite | Count | Engine |
|-------|-------|--------|
| ML Engine (pytest) | 11/11 ✅ | Python |
| E2E Blockchain | 4/4 ✅ | Python ↔ Sepolia |
| Smart Contract (Hardhat) | 9/9 ✅ | Solidity |
| **Total** | **24/24** | — |

## 📁 Project Structure

```
decai-oracle/
├── contracts/              # Solidity smart contracts
│   ├── src/                # Contract source files
│   ├── test/               # Hardhat tests
│   └── scripts/            # Deploy scripts
├── src/                    # Python backend
│   ├── api/                # FastAPI endpoints
│   ├── blockchain/         # Web3 contract manager
│   ├── data/               # Multi-source data aggregation
│   ├── ml/                 # ML prediction engine
│   ├── monitoring/         # Prometheus metrics
│   └── utils/              # Config, logging
├── dashboard/              # Streamlit dashboard
├── tests/                  # Python test suites
├── .env.example            # Environment template
└── requirements.txt        # Python dependencies
```

## 🔒 Security

- AccessControl with role-based permissions (PREDICTOR, VERIFIER, ADMIN)
- Pausable for emergency stops
- ReentrancyGuard on all state-changing functions
- Custom Errors for gas-efficient reverts

## 📄 License

MIT License — see [LICENSE](./LICENSE) for details.

---

**⭐ Star this repo if you find it useful!**
