# 🚀 Deployment Guide

This guide explains how to deploy the **DecAI Oracle** smart contracts to a live blockchain network (e.g., Sepolia Testnet).

---

## 📋 Prerequisites

1.  **Node.js & npm** installed.
2.  **Infura/Alchemy API Key** (or any RPC provider).
3.  **MetaMask Private Key** with testnet ETH (Sepolia).

---

## 1️⃣ Configure Environment

Create or edit your `.env` file in the root directory:

```ini
# RPC URL (e.g., from Infura)
SEPOLIA_RPC_URL="https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID"

# Wallet Private Key (Must have Sepolia ETH)
# ⚠️ NEVER SHARE THIS KEY! Use a dedicated test wallet.
PRIVATE_KEY="0x..."

# Enable Blockchain
BLOCKCHAIN_ENABLED=true
```

---

## 2️⃣ Get Sepolia ETH

You need testnet ETH to pay for gas fees. Get it from a faucet:
- [Google Cloud Web3 Faucet](https://cloud.google.com/application/web3/faucet/ethereum/sepolia)
- [Alchemy Sepolia Faucet](https://www.alchemy.com/faucets/ethereum-sepolia)
- [Infura Faucet](https://www.infura.io/faucet/sepolia)

---

## 3️⃣ Deploy Contract

Run the deployment script using Hardhat:

```bash
cd contracts
npx hardhat run scripts/deploy.js --network sepolia
```

**Expected Output:**

```text
🚀 Deploying DecAI Oracle contracts...
Deploying with account: 0xYourAddress
Account balance: 1.5 ETH

📝 Deploying PredictionOracle...
✅ PredictionOracle deployed to: 0xContractAddress

⏳ Waiting for block confirmations...

✨ Deployment complete!
```

---

## 4️⃣ Update Configuration

Copy the deployed contract address and update your `.env` file:

```ini
PREDICTION_ORACLE_ADDRESS="0xContractAddress"
```

---

## 5️⃣ Verify on Etherscan (Optional)

To publish your source code on Etherscan:

1.  Add `ETHERSCAN_API_KEY` to your `.env`.
2.  Run:

```bash
npx hardhat verify --network sepolia 0xContractAddress
```

---

## 6️⃣ Run the Application

Now your Python backend and Dashboard will interact with the live Sepolia contract!

```bash
# Run backend
python src/main.py

# Run dashboard
streamlit run dashboard/app.py
```

---

**Troubleshooting:**
- **Insufficient Funds**: Ensure your wallet has enough Sepolia ETH (>0.01 ETH).
- **RPC Error**: Check if your Infura/Alchemy API key is correct.
- **Nonce Error**: Reset your MetaMask transaction history or check pending transactions.
