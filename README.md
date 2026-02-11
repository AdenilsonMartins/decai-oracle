# 🔮 DecAI Oracle V2 - Resilient & Verifiable

DecAI Oracle is a decentralized, AI-powered price prediction system designed for maximum resilience and high-integrity data delivery.

## 🛡️ Resilient Architecture (V2)
The Version 2.0 release introduces a **Resilience Layer** that eliminates Single Points of Failure (SPOF):
- **Multi-Source Aggregation**: Real-time consensus between Binance, CoinGecko, and CoinCap.
- **Smart Outlier Detection**: Automatic removal of anomalous data (furthest-from-median) to prevent market manipulation.
- **Circuit Breaker Pattern**: Isolation of degraded data sources to preserve system performance.
- **On-Chain Hardening**: Optimized `PredictionOracleV2` contract with Access Control and Gas optimization.

## 🚀 Key Features
- **FastAPI Production Engine**: Asynchronous API with rate limiting and Redis caching.
- **Enterprise Monitoring**: Prometheus metrics for real-time observability.
- **Premium Dashboard**: Streamlit-based interface for visualizing market consensus and AI predictions.
- **Blockchain Integrity**: Automated storage of predictions on the Sepolia Testnet.

## 🛠️ Quick Start

### 1. Setup Environment
```bash
python scripts/setup.py
```
Ensure your `.env` contains `INFURA_API_KEY`, `PRIVATE_KEY`, and `PREDICTION_ORACLE_ADDRESS`.

### 2. Run the Dashboard
```bash
$env:PYTHONPATH="."
streamlit run src/dashboard/app.py
```

### 3. Start Production API
```bash
$env:PYTHONPATH="."
python src/api/main.py
```

## 📊 Dashboard Preview
The dashboard provides a real-time view of:
- **Price Consensus**: Aggregated price from multiple top-tier exchanges.
- **AI Prediction Horizon**: 24h price forecasts with confidence intervals.
- **Resilience Health**: Real-time status of all data connectors.
- **Blockchain Logs**: Verification of on-chain transaction integrity.

## 📄 Documentation
- [Planning V2](./docs/planning/v2/)
- [Implementation Status](./docs/planning/v2/IMPLEMENTATION_STATUS.md)
- [Resilient Architecture](./docs/planning/v2/RESILIENT_ARCHITECTURE.md)
- [Changelog](./CHANGELOG_V2.md)

---
**Version:** 2.0.0 (Production-Ready)  
**Status:** Phase 2 Complete (Resilience Integrated)
- 🏛️ **DAO Governance**: Token-based voting for protocol upgrades
- 📱 **Telegram Bot**: Interactive predictions via messaging
- 🔌 **REST API**: Public API for DApp integrations

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DecAI Oracle System                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌────────────┐ │
│  │ Data Sources │─────▶│  ML Engine   │─────▶│ Blockchain │ │
│  │              │      │              │      │            │ │
│  │ • CoinGecko  │      │ • Training   │      │ • Ethereum │ │
│  │ • APIs       │      │ • Prediction │      │ • Polygon  │ │
│  │ • On-chain   │      │ • Validation │      │ • Solana   │ │
│  └──────────────┘      └──────────────┘      └────────────┘ │
│         │                      │                     │       │
│         └──────────────────────┼─────────────────────┘       │
│                                │                             │
│                        ┌───────▼────────┐                    │
│                        │  IPFS Storage  │                    │
│                        │  (Pinata/W3S)  │                    │
│                        └────────────────┘                    │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Smart Contract Layer (Solidity)              │   │
│  │  • PredictionOracle.sol                              │   │
│  │  • Governance DAO                                    │   │
│  │  • ERC-20 Token (Incentives)                         │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+ (for smart contract deployment)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/decai-oracle.git
cd decai-oracle

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies (for smart contracts)
cd contracts
npm install
cd ..

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys (see SETUP_GUIDE.md)
```

### Run Features

```bash
# 1. Run basic prediction
python src/main.py

# 2. Launch interactive dashboard
streamlit run dashboard/app.py

# 3. Try gas fees predictor
python src/ml/gas_fees_predictor.py

# 4. Check accuracy tracking
python src/ml/accuracy_tracker.py

# 5. Simulate Twitter bot
python src/social/twitter_bot.py

# 6. Deploy smart contract to Sepolia testnet
cd contracts
npx hardhat run scripts/deploy.js --network sepolia
```

📖 **See [QUICKSTART.md](./QUICKSTART.md) for detailed 5-minute setup guide**

---

## 📚 Documentation

### Getting Started
- 📋 [**Executive Summary**](./docs/EXECUTIVE_SUMMARY.md) - ⭐ START HERE - Complete overview
- 🚀 [**Deployment Plan**](./docs/DEPLOYMENT_PLAN.md) - Step-by-step deployment guide
- 🔐 [**Environment Setup**](./docs/ENV_SETUP_GUIDE.md) - Configure .env correctly
- 🖥️ [**Streamlit Deployment**](./docs/STREAMLIT_DEPLOYMENT.md) - Publish dashboard online
- 📱 [**Social Media Templates**](./docs/SOCIAL_MEDIA_TEMPLATES.md) - Launch content ready to use

### Project Documentation
- 📖 [**Setup Guide**](./docs/SETUP_GUIDE.md) - Complete infrastructure setup
- 🗺️ [**Roadmap**](./docs/ROADMAP.md) - Development phases and timeline
- 📚 [**Features**](./docs/FEATURES.md) - Complete features documentation
- 💼 [**Commercial Strategy**](./docs/COMMERCIAL_STRATEGY.md) - Business model and monetization
- 🔧 [**API Documentation**](./docs/API.md) - REST API reference
- 🤝 [**Contributing**](./CONTRIBUTING.md) - How to contribute
- 📜 [**Architecture**](./docs/ARCHITECTURE.md) - Technical deep dive

---

## 💰 Commercial Model

DecAI Oracle operates on a **hybrid open-source model**:

### Free Tier (Open Source)
- ✅ Core ML engine and prediction algorithms
- ✅ Basic smart contracts
- ✅ Community support via GitHub

### Premium Tier (SaaS)
- 🚀 High-frequency API access (>1000 req/day)
- 🚀 Multi-chain deployment support
- 🚀 Priority support and custom integrations
- 🚀 Advanced analytics dashboard

### Token Economy
- 🪙 **$DECAI Token**: Governance and staking
- 🪙 **Staking Rewards**: Earn by contributing accurate predictions
- 🪙 **DAO Voting**: Community-driven protocol upgrades

See [COMMERCIAL_STRATEGY.md](./docs/COMMERCIAL_STRATEGY.md) for details.

---

## 🛣️ Roadmap

### Phase 1: MVP (Weeks 1-4) ✅ COMPLETED
- [x] Python ML engine with scikit-learn
- [x] Ethereum smart contract deployment
- [x] Basic API endpoints
- [x] Documentation
- [x] Web dashboard (Streamlit)
- [x] Blockchain Integration (Hardhat/Web3.py)

### Phase 2: Advanced Features (Months 2-3) 🔄
- [ ] IPFS integration for data storage
- [ ] Multi-chain support (Polygon, Solana)
- [ ] Advanced ML models (LSTM, Transformers)
- [ ] REST API with FastAPI

### Phase 3: Decentralization (Months 4-6) 📅
- [ ] Zero-Knowledge Proofs for model verification
- [ ] Federated Learning implementation
- [ ] DAO governance launch
- [ ] Token generation event (TGE)

### Phase 4: Scale (Months 7-12) 🚀
- [ ] Mainnet deployment
- [ ] Strategic partnerships (Chainlink, Aave)
- [ ] Security audits (CertiK, Trail of Bits)
- [ ] 1000+ active users

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Ways to Contribute
- 🐛 Report bugs and issues
- 💡 Propose new features
- 🔧 Submit pull requests
- 📖 Improve documentation
- 🌍 Translate to other languages

---

## 📊 Market Opportunity

- **AI + Blockchain Market**: $843M (2026) → $90B projected
- **CAGR**: 27.1% through 2034
- **Use Cases**: DeFi, RWAs, Prediction Markets, Supply Chain
- **Competitors**: Chainlink, ORA, Bittensor

**Differentiation**: Open-source, ML-native, developer-friendly Python toolkit.

---

## 🔒 Security

- All smart contracts will undergo professional audits before mainnet
- Bug bounty program (details TBA)
- Report vulnerabilities: security@decai-oracle.io

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](./LICENSE) for details.

---

## 🌐 Links

- **Website**: https://decai-oracle.io (TBA)
- **Documentation**: https://docs.decai-oracle.io (TBA)
- **Twitter**: [@DecAIOracle](https://twitter.com/DecAIOracle)
- **Discord**: [Join Community](https://discord.gg/decai-oracle)
- **GitHub**: [DecAI Oracle](https://github.com/yourusername/decai-oracle)

---

## 🙏 Acknowledgments

Built with ❤️ by the DecAI community.

Inspired by:
- [Chainlink](https://chain.link/) - Decentralized oracle networks
- [ORA](https://www.ora.io/) - On-chain ML verification
- [Bittensor](https://bittensor.com/) - Decentralized AI networks

---

**⭐ Star this repo if you find it useful!**
