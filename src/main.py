"""
DecAI Oracle - Main Entry Point
Runs the ML prediction engine and blockchain integration
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config import settings
from src.utils.logger import setup_logger
from src.ml.data_collector import DataCollector
from src.ml.predictor import Predictor
from src.blockchain.contract_manager import ContractManager

logger = setup_logger(__name__)


async def main():
    """Main execution flow"""
    logger.info("🚀 Starting DecAI Oracle...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    try:
        # Step 1: Collect data
        logger.info("📊 Collecting crypto data...")
        collector = DataCollector()
        data = await collector.fetch_bitcoin_data(days=30)
        logger.info(f"✅ Collected {len(data)} data points")
        
        # Step 2: Train model and predict
        logger.info("🧠 Training ML model...")
        predictor = Predictor()
        predictor.train(data)
        prediction = predictor.predict_next_day()
        confidence = predictor.get_confidence()
        
        logger.info(f"💰 Prediction: ${prediction:.2f}")
        logger.info(f"📈 Confidence: {confidence:.2%}")
        
        # Step 3: Store on blockchain (if enabled)
        if settings.BLOCKCHAIN_ENABLED:
            logger.info("⛓️  Storing prediction on blockchain...")
            contract_manager = ContractManager()
            tx_hash = await contract_manager.store_prediction(
                asset="Bitcoin",
                predicted_price=prediction,
                confidence=confidence
            )
            logger.info(f"✅ Transaction: {tx_hash}")
        else:
            logger.warning("⚠️  Blockchain disabled - prediction not stored on-chain")
        
        # Step 4: Generate verification hash
        from hashlib import sha256
        from datetime import datetime, timedelta
        
        prediction_data = f"Bitcoin prediction: ${prediction:.2f} on {datetime.now() + timedelta(days=1)}"
        prediction_hash = sha256(prediction_data.encode()).hexdigest()
        logger.info(f"🔒 Verification Hash: {prediction_hash}")
        
        logger.info("✨ DecAI Oracle completed successfully!")
        
        return {
            "prediction": prediction,
            "confidence": confidence,
            "hash": prediction_hash,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    result = asyncio.run(main())
    print("\n" + "="*50)
    print("📊 PREDICTION RESULT")
    print("="*50)
    print(f"Asset: Bitcoin")
    print(f"Predicted Price: ${result['prediction']:.2f}")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"Hash: {result['hash'][:16]}...")
    print(f"Timestamp: {result['timestamp']}")
    print("="*50)
