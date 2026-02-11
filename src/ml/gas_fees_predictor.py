"""
Gas Fees Predictor - Optimize transaction costs with ML
Predicts optimal gas fees for Ethereum transactions
"""

import asyncio
from typing import Dict, List, Tuple
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from src.utils.logger import setup_logger
from src.utils.config import settings

logger = setup_logger(__name__)


class GasFeesPredictor:
    """Predicts optimal gas fees for Ethereum transactions"""
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.is_trained = False
        self.historical_data = []
    
    async def fetch_gas_history(self, hours: int = 24) -> List[Dict]:
        """
        Fetch historical gas prices from Ethereum
        
        Args:
            hours: Number of hours of historical data
        
        Returns:
            List of gas price data points
        """
        try:
            from web3 import Web3
            
            if not settings.SEPOLIA_RPC_URL:
                logger.warning("No RPC URL configured, using mock data")
                return self._generate_mock_gas_data(hours)
            
            w3 = Web3(Web3.HTTPProvider(settings.SEPOLIA_RPC_URL))
            
            if not w3.is_connected():
                logger.warning("Cannot connect to Ethereum, using mock data")
                return self._generate_mock_gas_data(hours)
            
            logger.info(f"Fetching gas prices for last {hours} hours...")
            
            # Get current block
            current_block = w3.eth.block_number
            
            # Calculate blocks to fetch (assuming ~12s block time)
            blocks_per_hour = 300  # 3600s / 12s
            total_blocks = hours * blocks_per_hour
            
            gas_data = []
            
            # Sample blocks (every 10th block to avoid rate limits)
            for i in range(0, total_blocks, 10):
                block_num = current_block - i
                
                try:
                    block = w3.eth.get_block(block_num)
                    
                    if block and 'baseFeePerGas' in block:
                        gas_price_gwei = w3.from_wei(block['baseFeePerGas'], 'gwei')
                        
                        gas_data.append({
                            'block': block_num,
                            'timestamp': block['timestamp'],
                            'base_fee': float(gas_price_gwei),
                            'transactions': len(block.get('transactions', []))
                        })
                except Exception as e:
                    logger.debug(f"Error fetching block {block_num}: {e}")
                    continue
            
            logger.info(f"✅ Fetched {len(gas_data)} gas price data points")
            self.historical_data = gas_data
            
            return gas_data
            
        except Exception as e:
            logger.error(f"Error fetching gas history: {e}")
            return self._generate_mock_gas_data(hours)
    
    def _generate_mock_gas_data(self, hours: int) -> List[Dict]:
        """Generate mock gas data for testing"""
        logger.info("Generating mock gas data for demonstration")
        
        data = []
        base_fee = 20.0  # Base fee in gwei
        
        for i in range(hours * 6):  # 6 data points per hour
            # Simulate daily pattern (higher fees during business hours)
            hour_of_day = (datetime.now() - timedelta(minutes=i*10)).hour
            
            # Higher fees during 9am-5pm UTC
            if 9 <= hour_of_day <= 17:
                multiplier = 1.5 + np.random.normal(0, 0.2)
            else:
                multiplier = 0.8 + np.random.normal(0, 0.15)
            
            gas_fee = base_fee * multiplier
            
            data.append({
                'block': 1000000 - i,
                'timestamp': int((datetime.now() - timedelta(minutes=i*10)).timestamp()),
                'base_fee': max(5.0, gas_fee),  # Minimum 5 gwei
                'transactions': int(100 + np.random.normal(0, 30))
            })
        
        return data
    
    def train(self, gas_data: List[Dict]):
        """
        Train gas fee prediction model
        
        Args:
            gas_data: Historical gas price data
        """
        if len(gas_data) < 10:
            raise ValueError("Need at least 10 data points to train")
        
        logger.info("Training gas fee prediction model...")
        
        # Extract features
        features = []
        targets = []
        
        for i in range(len(gas_data) - 1):
            current = gas_data[i]
            next_point = gas_data[i + 1]
            
            # Features: current fee, hour of day, tx count
            dt = datetime.fromtimestamp(current['timestamp'])
            
            features.append([
                current['base_fee'],
                dt.hour,
                dt.weekday(),
                current['transactions']
            ])
            
            # Target: next gas fee
            targets.append(next_point['base_fee'])
        
        X = np.array(features)
        y = np.array(targets)
        
        # Train model
        self.model.fit(X, y)
        
        # Evaluate
        score = self.model.score(X, y)
        
        logger.info(f"✅ Model trained with R² score: {score:.4f}")
        self.is_trained = True
    
    def predict_gas_fee(
        self,
        current_fee: float,
        hour: int = None,
        weekday: int = None,
        tx_count: int = 100
    ) -> Dict[str, float]:
        """
        Predict gas fees for different urgency levels
        
        Args:
            current_fee: Current base fee in gwei
            hour: Hour of day (0-23), defaults to current
            weekday: Day of week (0-6), defaults to current
            tx_count: Number of transactions in block
        
        Returns:
            Dictionary with predictions for slow/standard/fast
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet. Call train() first.")
        
        now = datetime.now()
        hour = hour if hour is not None else now.hour
        weekday = weekday if weekday is not None else now.weekday()
        
        # Predict next fee
        features = np.array([[current_fee, hour, weekday, tx_count]])
        predicted_base = self.model.predict(features)[0]
        
        # Calculate recommendations for different speeds
        # Slow: base fee
        # Standard: base + 10%
        # Fast: base + 25%
        # Instant: base + 50%
        
        recommendations = {
            'slow': max(5.0, predicted_base * 0.9),
            'standard': predicted_base,
            'fast': predicted_base * 1.15,
            'instant': predicted_base * 1.3,
            'predicted_base': predicted_base,
            'current_base': current_fee,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Gas fee predictions: {recommendations}")
        
        return recommendations
    
    def get_optimal_time(self, gas_data: List[Dict], hours_ahead: int = 24) -> Dict:
        """
        Find optimal time to send transaction in next N hours
        
        Args:
            gas_data: Historical gas data
            hours_ahead: Hours to look ahead
        
        Returns:
            Dictionary with optimal time and expected fee
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet")
        
        predictions = []
        
        for hour_offset in range(hours_ahead):
            future_time = datetime.now() + timedelta(hours=hour_offset)
            
            # Use average current fee
            avg_current_fee = np.mean([d['base_fee'] for d in gas_data[-10:]])
            
            pred = self.predict_gas_fee(
                current_fee=avg_current_fee,
                hour=future_time.hour,
                weekday=future_time.weekday()
            )
            
            predictions.append({
                'time': future_time,
                'predicted_fee': pred['standard'],
                'hour_offset': hour_offset
            })
        
        # Find minimum
        optimal = min(predictions, key=lambda x: x['predicted_fee'])
        
        logger.info(f"Optimal time: {optimal['time']} with fee {optimal['predicted_fee']:.2f} gwei")
        
        return {
            'optimal_time': optimal['time'].isoformat(),
            'optimal_fee': optimal['predicted_fee'],
            'hours_from_now': optimal['hour_offset'],
            'current_average': np.mean([d['base_fee'] for d in gas_data[-10:]]),
            'potential_savings': np.mean([d['base_fee'] for d in gas_data[-10:]]) - optimal['predicted_fee']
        }


async def main():
    """Demo gas fees predictor"""
    logger.info("🚀 Starting Gas Fees Predictor Demo...")
    
    predictor = GasFeesPredictor()
    
    # Fetch historical data
    gas_data = await predictor.fetch_gas_history(hours=24)
    
    # Train model
    predictor.train(gas_data)
    
    # Current gas fee (use latest from data)
    current_fee = gas_data[0]['base_fee']
    
    # Predict
    predictions = predictor.predict_gas_fee(current_fee)
    
    print("\n" + "="*60)
    print("⛽ GAS FEE PREDICTIONS")
    print("="*60)
    print(f"Current Base Fee: {current_fee:.2f} gwei")
    print(f"\nRecommended Gas Prices:")
    print(f"  🐌 Slow (>10 min):     {predictions['slow']:.2f} gwei")
    print(f"  ⚡ Standard (~3 min):  {predictions['standard']:.2f} gwei")
    print(f"  🚀 Fast (~30 sec):     {predictions['fast']:.2f} gwei")
    print(f"  ⚡⚡ Instant (<15 sec): {predictions['instant']:.2f} gwei")
    print("="*60)
    
    # Find optimal time
    optimal = predictor.get_optimal_time(gas_data, hours_ahead=24)
    
    print("\n" + "="*60)
    print("⏰ OPTIMAL TRANSACTION TIME")
    print("="*60)
    print(f"Best time: {optimal['hours_from_now']} hours from now")
    print(f"Expected fee: {optimal['optimal_fee']:.2f} gwei")
    print(f"Potential savings: {optimal['potential_savings']:.2f} gwei ({optimal['potential_savings']/current_fee*100:.1f}%)")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
