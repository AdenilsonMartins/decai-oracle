# DecAI Oracle Project Structure

decai-oracle/
├── .github/
│   └── workflows/
│       ├── ci.yml                 # CI/CD pipeline
│       ├── tests.yml              # Automated testing
│       └── deploy.yml             # Deployment automation
│
├── contracts/                     # Smart contracts
│   ├── src/
│   │   ├── PredictionOracle.sol   # Main oracle contract
│   │   ├── DecAIToken.sol         # ERC-20 governance token
│   │   └── DecAIDAO.sol           # DAO governance
│   ├── test/
│   │   ├── PredictionOracle.test.js
│   │   └── DecAIToken.test.js
│   ├── scripts/
│   │   ├── deploy.js              # Deployment script
│   │   └── verify.js              # Etherscan verification
│   ├── hardhat.config.js
│   └── package.json
│
├── src/                           # Python backend
│   ├── ml/                        # Machine learning
│   │   ├── __init__.py
│   │   ├── data_collector.py     # Fetch crypto data
│   │   ├── feature_engineering.py
│   │   ├── models.py              # ML models
│   │   ├── predictor.py           # Prediction engine
│   │   └── evaluator.py           # Model evaluation
│   ├── blockchain/                # Blockchain integration
│   │   ├── __init__.py
│   │   ├── web3_client.py         # Web3 connection
│   │   ├── contract_manager.py    # Contract interactions
│   │   └── transaction_handler.py
│   ├── storage/                   # IPFS integration
│   │   ├── __init__.py
│   │   ├── ipfs_client.py
│   │   └── pinata_manager.py
│   ├── api/                       # REST API
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI app
│   │   ├── routes/
│   │   │   ├── predictions.py
│   │   │   ├── models.py
│   │   │   └── health.py
│   │   └── middleware/
│   │       ├── auth.py
│   │       └── rate_limit.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration
│   │   ├── logger.py              # Logging
│   │   └── validators.py
│   └── main.py                    # Main entry point
│
├── frontend/                      # Web dashboard (Next.js)
│   ├── app/
│   │   ├── page.tsx               # Home page
│   │   ├── dashboard/
│   │   ├── api/
│   │   └── layout.tsx
│   ├── components/
│   │   ├── PredictionCard.tsx
│   │   ├── ChartView.tsx
│   │   └── ConnectWallet.tsx
│   ├── lib/
│   │   ├── web3.ts
│   │   └── api.ts
│   ├── public/
│   ├── package.json
│   └── next.config.js
│
├── notebooks/                     # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_model_training.ipynb
│   └── 03_evaluation.ipynb
│
├── tests/                         # Python tests
│   ├── unit/
│   │   ├── test_data_collector.py
│   │   ├── test_models.py
│   │   └── test_predictor.py
│   ├── integration/
│   │   ├── test_blockchain.py
│   │   └── test_api.py
│   └── e2e/
│       └── test_full_flow.py
│
├── docs/                          # Documentation
│   ├── SETUP_GUIDE.md             ✅ Created
│   ├── ROADMAP.md                 ✅ Created
│   ├── COMMERCIAL_STRATEGY.md     ✅ Created
│   ├── API.md                     # API documentation
│   ├── ARCHITECTURE.md            # Technical architecture
│   └── CONTRIBUTING.md            # Contribution guide
│
├── scripts/                       # Utility scripts
│   ├── setup_env.sh               # Environment setup
│   ├── run_tests.sh               # Test runner
│   └── deploy_mainnet.sh          # Mainnet deployment
│
├── .env.example                   # Environment template
├── .gitignore
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Python project config
├── LICENSE                        # MIT License
└── README.md                      ✅ Created
