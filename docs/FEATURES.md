# 📚 DecAI Oracle - Complete Features Documentation

**Version**: 1.0  
**Last Updated**: February 5, 2026

---

## 📋 Table of Contents

1. [Core Features](#core-features)
2. [Streamlit Dashboard](#streamlit-dashboard)
3. [Gas Fees Predictor](#gas-fees-predictor)
4. [Accuracy Tracking System](#accuracy-tracking-system)
5. [Twitter Bot](#twitter-bot)
6. [API Reference](#api-reference)
7. [Usage Examples](#usage-examples)

---

## 🎯 Core Features

### 1. Machine Learning Prediction Engine

**Location**: `src/ml/predictor.py`

**Features**:
- Linear regression baseline model
- Support for advanced models (LSTM, Transformers)
- Confidence scoring
- Model evaluation metrics (R², RMSE, MAE)

**Usage**:
```python
from src.ml.predictor import Predictor
from src.ml.data_collector import DataCollector
import asyncio

# Fetch data
collector = DataCollector()
data = asyncio.run(collector.fetch_bitcoin_data(days=30))

# Train and predict
predictor = Predictor()
predictor.train(data)
prediction = predictor.predict_next_day()
confidence = predictor.get_confidence()

print(f"Prediction: ${prediction:.2f}")
print(f"Confidence: {confidence:.2%}")
```

---

## 🖥️ Streamlit Dashboard

### Overview

Interactive web dashboard for real-time crypto predictions with beautiful UI and on-chain verification.

**Location**: `dashboard/app.py`

### Features

✅ **Real-Time Predictions**
- Live crypto price predictions
- Interactive charts with Plotly
- Confidence scoring
- Trend analysis

✅ **Multi-Asset Support**
- Bitcoin
- Ethereum
- Solana
- Polygon

✅ **On-Chain Verification**
- Cryptographic hash generation
- Smart contract integration
- Etherscan links

✅ **Historical Data Analysis**
- Statistical summaries
- Data visualization
- CSV export

### Running the Dashboard

```bash
# Install dependencies
pip install -r dashboard/requirements.txt

# Run dashboard
streamlit run dashboard/app.py
```

The dashboard will open at `http://localhost:8501`

### Dashboard Sections

#### 1. Live Prediction Tab
- Current price display
- 24h prediction
- Confidence score
- Price trend chart
- Verification hash
- On-chain storage button

#### 2. Historical Data Tab
- Price statistics (max, min, average, std dev)
- Raw data table
- CSV download

#### 3. On-Chain Verification Tab
- Smart contract details
- Transaction verification
- Etherscan integration

#### 4. About Tab
- Project information
- Use cases
- Technology stack
- Community links

### Deployment

**Streamlit Cloud** (Recommended):
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Select `dashboard/app.py` as main file
5. Add secrets (API keys) in settings
6. Deploy!

**Vercel/Railway** (Alternative):
- Use `streamlit run` command in start script
- Configure environment variables

---

## ⛽ Gas Fees Predictor

### Overview

ML-powered gas fee optimization tool that predicts optimal transaction timing and costs.

**Location**: `src/ml/gas_fees_predictor.py`

### Features

✅ **Real-Time Gas Analysis**
- Fetches 24h of gas price history
- Analyzes patterns (hourly, daily)
- Predicts future gas fees

✅ **Multi-Speed Recommendations**
- 🐌 Slow (>10 min)
- ⚡ Standard (~3 min)
- 🚀 Fast (~30 sec)
- ⚡⚡ Instant (<15 sec)

✅ **Optimal Timing**
- Finds cheapest time in next 24h
- Calculates potential savings
- Provides hour-by-hour forecast

### Usage

```python
from src.ml.gas_fees_predictor import GasFeesPredictor
import asyncio

async def main():
    predictor = GasFeesPredictor()
    
    # Fetch historical data
    gas_data = await predictor.fetch_gas_history(hours=24)
    
    # Train model
    predictor.train(gas_data)
    
    # Get current recommendations
    current_fee = gas_data[0]['base_fee']
    predictions = predictor.predict_gas_fee(current_fee)
    
    print(f"Slow: {predictions['slow']:.2f} gwei")
    print(f"Standard: {predictions['standard']:.2f} gwei")
    print(f"Fast: {predictions['fast']:.2f} gwei")
    print(f"Instant: {predictions['instant']:.2f} gwei")
    
    # Find optimal time
    optimal = predictor.get_optimal_time(gas_data, hours_ahead=24)
    print(f"\nOptimal time: {optimal['hours_from_now']} hours from now")
    print(f"Expected fee: {optimal['optimal_fee']:.2f} gwei")
    print(f"Savings: {optimal['potential_savings']:.2f} gwei")

asyncio.run(main())
```

### Run Demo

```bash
python src/ml/gas_fees_predictor.py
```

### Integration with Dashboard

The gas fees predictor can be integrated into the Streamlit dashboard:

```python
# In dashboard/app.py
from src.ml.gas_fees_predictor import GasFeesPredictor

predictor = GasFeesPredictor()
gas_data = await predictor.fetch_gas_history(hours=24)
predictor.train(gas_data)
predictions = predictor.predict_gas_fee(gas_data[0]['base_fee'])

st.metric("Optimal Gas Fee", f"{predictions['standard']:.2f} gwei")
```

---

## 🎯 Accuracy Tracking System

### Overview

On-chain verification system that tracks prediction accuracy and creates public leaderboards.

**Location**: `src/ml/accuracy_tracker.py`

### Features

✅ **Prediction Storage**
- JSON-based persistence
- Cryptographic hashing
- Metadata tracking

✅ **Automatic Verification**
- 24h auto-verification
- Accuracy calculation (MAE, RMSE)
- Direction correctness

✅ **Leaderboard**
- Top predictions ranking
- Predictor statistics
- Asset-wise breakdown

### Usage

```python
from src.ml.accuracy_tracker import AccuracyTracker

tracker = AccuracyTracker()

# Add prediction
pred_id = tracker.add_prediction(
    asset="Bitcoin",
    predicted_price=50000.0,
    confidence=0.85,
    predictor="DecAI Oracle v1.0",
    tx_hash="0x..."  # Optional
)

# Verify later (manual or automatic)
tracker.verify_prediction(pred_id, actual_price=49800.0)

# Get statistics
stats = tracker.get_statistics()
print(f"Average Accuracy: {stats['average_accuracy']:.2f}%")

# Get leaderboard
leaderboard = tracker.get_leaderboard(top_n=10)
for entry in leaderboard:
    print(f"#{entry['rank']}: {entry['accuracy']:.2f}%")
```

### Auto-Verification

```python
from src.ml.data_collector import DataCollector

# Automatically verify pending predictions
collector = DataCollector()
await tracker.auto_verify_pending(collector)
```

### Data Storage

Predictions are stored in `data/predictions.json`:

```json
[
  {
    "id": 1,
    "asset": "Bitcoin",
    "predicted_price": 50000.0,
    "actual_price": 49800.0,
    "confidence": 0.85,
    "timestamp": "2026-02-05T12:00:00",
    "verification_timestamp": "2026-02-06T12:00:00",
    "predictor": "DecAI Oracle v1.0",
    "tx_hash": "0x..."
  }
]
```

---

## 🐦 Twitter Bot

### Overview

Automated social media bot for posting daily predictions and engagement.

**Location**: `src/social/twitter_bot.py`

### Features

✅ **Daily Predictions**
- Automated crypto predictions
- Trend analysis (bullish/bearish)
- Confidence indicators

✅ **Gas Fees Alerts**
- Optimal timing notifications
- Savings calculations

✅ **Accuracy Updates**
- Weekly performance reports
- Leaderboard highlights

### Setup

1. **Get Twitter API Credentials**:
   - Go to [developer.twitter.com](https://developer.twitter.com)
   - Create app
   - Get API keys

2. **Add to `.env`**:
```bash
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
```

3. **Install Dependencies**:
```bash
pip install tweepy
```

### Usage

```python
from src.social.twitter_bot import TwitterBot
import asyncio

async def main():
    bot = TwitterBot()
    
    # Post daily prediction
    tweet_id = await bot.post_daily_prediction("Bitcoin")
    
    # Post gas fees alert
    tweet_id = await bot.post_gas_fees_alert()
    
    # Post accuracy update
    tweet_id = await bot.post_accuracy_update()

asyncio.run(main())
```

### Simulation Mode

Test without posting to Twitter:

```bash
python src/social/twitter_bot.py
```

This will print the tweet content without actually posting.

### Automation

**Schedule with cron** (Linux/Mac):
```bash
# Daily at 9am
0 9 * * * cd /path/to/decai-oracle && python src/social/twitter_bot.py
```

**Schedule with Task Scheduler** (Windows):
- Create new task
- Trigger: Daily at 9am
- Action: Run `python src/social/twitter_bot.py`

**Schedule with GitHub Actions**:
```yaml
# .github/workflows/daily-tweet.yml
name: Daily Tweet
on:
  schedule:
    - cron: '0 9 * * *'  # 9am UTC daily
jobs:
  tweet:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Post tweet
        env:
          TWITTER_API_KEY: ${{ secrets.TWITTER_API_KEY }}
          TWITTER_API_SECRET: ${{ secrets.TWITTER_API_SECRET }}
          TWITTER_ACCESS_TOKEN: ${{ secrets.TWITTER_ACCESS_TOKEN }}
          TWITTER_ACCESS_SECRET: ${{ secrets.TWITTER_ACCESS_SECRET }}
        run: python src/social/twitter_bot.py
```

---

## 📡 API Reference

### Data Collector

**Class**: `DataCollector`  
**Location**: `src/ml/data_collector.py`

**Methods**:
- `fetch_bitcoin_data(days: int) -> np.ndarray`
- `fetch_multi_asset_data(assets: List[str], days: int) -> Dict`
- `fetch_asset_data(asset_id: str, days: int) -> np.ndarray`

### Predictor

**Class**: `Predictor`  
**Location**: `src/ml/predictor.py`

**Methods**:
- `train(prices: np.ndarray, test_size: float = 0.2)`
- `predict_next_day() -> float`
- `get_confidence() -> float`
- `predict_future(days: int) -> np.ndarray`

### Gas Fees Predictor

**Class**: `GasFeesPredictor`  
**Location**: `src/ml/gas_fees_predictor.py`

**Methods**:
- `fetch_gas_history(hours: int = 24) -> List[Dict]`
- `train(gas_data: List[Dict])`
- `predict_gas_fee(current_fee: float, ...) -> Dict`
- `get_optimal_time(gas_data: List[Dict], hours_ahead: int) -> Dict`

### Accuracy Tracker

**Class**: `AccuracyTracker`  
**Location**: `src/ml/accuracy_tracker.py`

**Methods**:
- `add_prediction(asset, predicted_price, confidence, ...) -> int`
- `verify_prediction(prediction_id: int, actual_price: float)`
- `get_leaderboard(top_n: int = 10) -> List[Dict]`
- `get_statistics() -> Dict`
- `auto_verify_pending(data_collector)`

---

## 💡 Usage Examples

### Example 1: Complete Prediction Flow

```python
import asyncio
from src.ml.data_collector import DataCollector
from src.ml.predictor import Predictor
from src.ml.accuracy_tracker import AccuracyTracker
from src.blockchain.contract_manager import ContractManager

async def main():
    # 1. Collect data
    collector = DataCollector()
    data = await collector.fetch_bitcoin_data(days=30)
    
    # 2. Train and predict
    predictor = Predictor()
    predictor.train(data)
    prediction = predictor.predict_next_day()
    confidence = predictor.get_confidence()
    
    # 3. Track accuracy
    tracker = AccuracyTracker()
    pred_id = tracker.add_prediction(
        asset="Bitcoin",
        predicted_price=prediction,
        confidence=confidence
    )
    
    # 4. Store on-chain (if enabled)
    if settings.BLOCKCHAIN_ENABLED:
        contract_manager = ContractManager()
        tx_hash = await contract_manager.store_prediction(
            asset="Bitcoin",
            predicted_price=prediction,
            confidence=confidence
        )
        print(f"Stored on-chain: {tx_hash}")
    
    print(f"Prediction #{pred_id}: ${prediction:.2f} (confidence: {confidence:.2%})")

asyncio.run(main())
```

### Example 2: Gas Optimization

```python
from src.ml.gas_fees_predictor import GasFeesPredictor
import asyncio

async def optimize_transaction():
    predictor = GasFeesPredictor()
    
    # Fetch and train
    gas_data = await predictor.fetch_gas_history(hours=24)
    predictor.train(gas_data)
    
    # Get recommendations
    current_fee = gas_data[0]['base_fee']
    predictions = predictor.predict_gas_fee(current_fee)
    
    # Find optimal time
    optimal = predictor.get_optimal_time(gas_data, hours_ahead=24)
    
    if optimal['potential_savings'] > 5:  # Save >5 gwei
        print(f"⏰ Wait {optimal['hours_from_now']} hours")
        print(f"💰 Save {optimal['potential_savings']:.2f} gwei")
    else:
        print("✅ Send now - fees are optimal")

asyncio.run(optimize_transaction())
```

### Example 3: Social Media Automation

```python
from src.social.twitter_bot import TwitterBot
import asyncio

async def daily_social_update():
    bot = TwitterBot()
    
    # Morning: Daily prediction
    await bot.post_daily_prediction("Bitcoin")
    
    # Afternoon: Gas fees alert
    await bot.post_gas_fees_alert()
    
    # Evening: Accuracy update (weekly)
    from datetime import datetime
    if datetime.now().weekday() == 4:  # Friday
        await bot.post_accuracy_update()

asyncio.run(daily_social_update())
```

---

## 🚀 Quick Start Commands

```bash
# Run main prediction
python src/main.py

# Run Streamlit dashboard
streamlit run dashboard/app.py

# Run gas fees predictor
python src/ml/gas_fees_predictor.py

# Run accuracy tracker demo
python src/ml/accuracy_tracker.py

# Run Twitter bot (simulation)
python src/social/twitter_bot.py

# Run all tests
pytest tests/ -v
```

---

## 📞 Support

- 📖 [Full Documentation](https://docs.decai-oracle.io)
- 💬 [Discord Community](https://discord.gg/decai-oracle)
- 🐛 [Report Issues](https://github.com/decai-oracle/issues)
- 📧 Email: support@decai-oracle.io

---

**Made with ❤️ by the DecAI Oracle community**
