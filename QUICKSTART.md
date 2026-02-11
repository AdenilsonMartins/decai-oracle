# ⚡ DecAI Oracle - Quick Start Guide

Get up and running with DecAI Oracle in 5 minutes!

---

## 1️⃣ Installation

1.  **Clone Repo**:
    ```bash
    git clone https://github.com/yourusername/decai-oracle.git
    cd decai-oracle
    ```

2.  **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    pip install -r dashboard/requirements.txt
    ```

3.  **Install Node.js Dependencies (for Blockchain)**:
    ```bash
    cd contracts
    npm install
    cd ..
    ```

---

## 2️⃣ Development Setup (Local)

1.  **Start Local Blockchain**:
    Open a new terminal and run:
    ```bash
    cd contracts
    npx hardhat node
    ```

2.  **Deploy Smart Contract**:
    Open a second terminal and run:
    ```bash
    cd contracts
    npx hardhat run scripts/deploy.js --network localhost
    ```
    *Copy the deployed address (e.g., `0x5FbDB...`).*

3.  **Configure Environment**:
    Create `.env` file:
    ```ini
    SEPOLIA_RPC_URL="http://127.0.0.1:8545"
    PRIVATE_KEY="0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80" # Default Hardhat Key
    PREDICTION_ORACLE_ADDRESS="PASTE_YOUR_ADDRESS_HERE"
    BLOCKCHAIN_ENABLED=true
    ```

---

## 3️⃣ Run Applications

### 🔥 Real-Time Dashboard (Frontend)
Visual interface for predictions and verification.

```bash
streamlit run dashboard/app.py
```
*Open http://localhost:8501 in your browser.*

### 🤖 Automation (Backend)
Run the core prediction engine or Twitter bot.

```bash
# Run single prediction flow
python src/main.py

# Run Twitter bot (simulation)
python src/social/twitter_bot.py
```

---

## 4️⃣ Production Deployment (Sepolia)

Ready for public testnet? See [DEPLOY_GUIDE.md](./docs/DEPLOY_GUIDE.md).

---

**Need Help?**
Check [docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md) or join our [Discord](https://discord.gg/decai-oracle).
