# 🔮 DecAI Oracle Network (DON)

> A Decentralized AI-Powered Prediction Infrastructure for Web3

[![Solidity](https://img.shields.io/badge/Solidity-0.8.24-blue)](https://soliditylang.org/)
[![Python](https://img.shields.io/badge/Python-3.12+-green)](https://python.org/)
[![Sepolia](https://img.shields.io/badge/Network-Sepolia-yellow)](https://sepolia.etherscan.io/)
[![License](https://img.shields.io/badge/License-MIT-purple)](./LICENSE)
[![Audit](https://img.shields.io/badge/Security-Slither_Passed-success)](./docs/security/AUDIT_REPORT_V2.md)

**DecAI Oracle Network (DON)** is a robust, decentralized price prediction infrastructure that bridges machine learning intelligence with blockchain integrity. It provides high-frequency price consensus with on-chain verification, multi-source data aggregation, and extreme resilience.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 DecAI Oracle Network System                  │
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

## 🛡️ Core Features

- **Multi-Source Aggregation**: Real-time price consensus from Binance, CoinGecko, and CoinCap with outlier detection.
- **Resilient ML Engine**: Linear regression models with confidence scoring and fallback mechanisms.
- **On-Chain Governance**: Roles-based access control (AccessControl) for Predictors, Verifiers, and Admins.
- **Advanced Monitoring**: Real-time observability via Prometheus and JSON-structured logging.
- **Premium Dashboard**: Custom-designed Streamlit interface for live monitoring and historical analysis.
- **Production Ready**: Full Docker orchestration and CI/CD pipelines.

## 📜 Smart Contract (V2)

| Property | Value |
|----------|-------|
| **Network** | Sepolia Testnet |
| **Address** | `0x0E8B23cb4Dcdd2AA3bc7a5db0070a2E9CB1c4252` |
| **Verification** | [Etherscan ✅](https://sepolia.etherscan.io/address/0x0E8B23cb4Dcdd2AA3bc7a5db0070a2E9CB1c4252#code) |
| **Security** | Audited via Slither (0 High/Med Issues) |

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- Docker (optional, for production)

### Installation

```bash
# Clone the network repo
git clone https://github.com/AdenilsonMartins/DecAi-Oracle-NetWork.git
cd DecAi-Oracle-NetWork

# Python dependencies
pip install -r requirements.txt

# Smart contract dependencies
cd contracts && npm install && cd ..

# Environment Setup
cp .env.example .env
# Fill in your private key and RPC provider
```

### Run Locally

```bash
# API Server (DecAI Backend)
python -m uvicorn src.api.main:app --port 8000

# Dashboard (separate terminal)
streamlit run dashboard/app.py 
```

## 🧪 Testing Suite

| Component | Status | Tool |
|-----------|--------|------|
| ML Engine | 11/11 ✅ | Pytest |
| Smart Contract | 9/9 ✅ | Hardhat |
| Integration | 4/4 ✅ | Web3.py |
| **Security Audit** | **Passed** ✅ | Slither |

## 📁 Repository Structure

```
DecAi-Oracle-NetWork/
├── contracts/              # Solidity V2 (Audited)
├── src/                    # Python Core Infrastructure
├── dashboard/              # Streamlit Premium Interface
├── tests/                  # Integrity test suites
├── scripts/                # Utility & DevOps scripts
├── docs/                   # Documentation & Audit Reports
└── .env.example            # Configuration template
```

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

**Built with passion by the DecAI Oracle Network Team.**
