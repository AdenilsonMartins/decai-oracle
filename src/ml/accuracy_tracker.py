"""
Accuracy Tracker - On-chain verification system
Tracks prediction accuracy and creates leaderboard
"""

import asyncio
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import json
from pathlib import Path
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class PredictionRecord:
    """Record of a single prediction"""
    id: int
    asset: str
    predicted_price: float
    actual_price: Optional[float]
    confidence: float
    timestamp: datetime
    verification_timestamp: Optional[datetime]
    predictor: str
    tx_hash: Optional[str]
    
    def calculate_accuracy(self) -> Optional[float]:
        """Calculate prediction accuracy (0-100%)"""
        if self.actual_price is None:
            return None
        
        error = abs(self.predicted_price - self.actual_price)
        accuracy = max(0, 100 - (error / self.actual_price * 100))
        return accuracy
    
    def calculate_mae(self) -> Optional[float]:
        """Calculate Mean Absolute Error"""
        if self.actual_price is None:
            return None
        return abs(self.predicted_price - self.actual_price)
    
    def is_direction_correct(self) -> Optional[bool]:
        """Check if prediction direction was correct"""
        if self.actual_price is None:
            return None
        
        # Compare with previous price (simplified)
        return True  # Placeholder


class AccuracyTracker:
    """Tracks and verifies prediction accuracy"""
    
    def __init__(self, storage_path: str = "data/predictions.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.predictions: List[PredictionRecord] = []
        self.load_predictions()
    
    def load_predictions(self):
        """Load predictions from storage"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    
                self.predictions = [
                    PredictionRecord(
                        id=p['id'],
                        asset=p['asset'],
                        predicted_price=p['predicted_price'],
                        actual_price=p.get('actual_price'),
                        confidence=p['confidence'],
                        timestamp=datetime.fromisoformat(p['timestamp']),
                        verification_timestamp=datetime.fromisoformat(p['verification_timestamp']) if p.get('verification_timestamp') else None,
                        predictor=p['predictor'],
                        tx_hash=p.get('tx_hash')
                    )
                    for p in data
                ]
                
                logger.info(f"✅ Loaded {len(self.predictions)} predictions")
            except Exception as e:
                logger.error(f"Error loading predictions: {e}")
                self.predictions = []
    
    def save_predictions(self):
        """Save predictions to storage"""
        try:
            data = [
                {
                    'id': p.id,
                    'asset': p.asset,
                    'predicted_price': p.predicted_price,
                    'actual_price': p.actual_price,
                    'confidence': p.confidence,
                    'timestamp': p.timestamp.isoformat(),
                    'verification_timestamp': p.verification_timestamp.isoformat() if p.verification_timestamp else None,
                    'predictor': p.predictor,
                    'tx_hash': p.tx_hash
                }
                for p in self.predictions
            ]
            
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"✅ Saved {len(self.predictions)} predictions")
        except Exception as e:
            logger.error(f"Error saving predictions: {e}")
    
    def add_prediction(
        self,
        asset: str,
        predicted_price: float,
        confidence: float,
        predictor: str = "DecAI Oracle",
        tx_hash: Optional[str] = None
    ) -> int:
        """
        Add a new prediction
        
        Returns:
            Prediction ID
        """
        prediction_id = len(self.predictions) + 1
        
        prediction = PredictionRecord(
            id=prediction_id,
            asset=asset,
            predicted_price=predicted_price,
            actual_price=None,
            confidence=confidence,
            timestamp=datetime.now(),
            verification_timestamp=None,
            predictor=predictor,
            tx_hash=tx_hash
        )
        
        self.predictions.append(prediction)
        self.save_predictions()
        
        logger.info(f"✅ Added prediction #{prediction_id}: {asset} @ ${predicted_price:.2f}")
        
        return prediction_id
    
    def verify_prediction(self, prediction_id: int, actual_price: float):
        """
        Verify a prediction with actual price
        
        Args:
            prediction_id: ID of prediction to verify
            actual_price: Actual price observed
        """
        prediction = next((p for p in self.predictions if p.id == prediction_id), None)
        
        if not prediction:
            raise ValueError(f"Prediction {prediction_id} not found")
        
        if prediction.actual_price is not None:
            logger.warning(f"Prediction {prediction_id} already verified")
            return
        
        prediction.actual_price = actual_price
        prediction.verification_timestamp = datetime.now()
        
        accuracy = prediction.calculate_accuracy()
        mae = prediction.calculate_mae()
        
        self.save_predictions()
        
        logger.info(f"✅ Verified prediction #{prediction_id}")
        logger.info(f"   Predicted: ${prediction.predicted_price:.2f}")
        logger.info(f"   Actual: ${actual_price:.2f}")
        logger.info(f"   Accuracy: {accuracy:.2f}%")
        logger.info(f"   MAE: ${mae:.2f}")
    
    def get_leaderboard(self, top_n: int = 10) -> List[Dict]:
        """
        Get leaderboard of best predictions
        
        Args:
            top_n: Number of top predictions to return
        
        Returns:
            List of top predictions sorted by accuracy
        """
        verified = [p for p in self.predictions if p.actual_price is not None]
        
        if not verified:
            return []
        
        # Sort by accuracy
        sorted_predictions = sorted(
            verified,
            key=lambda p: p.calculate_accuracy() or 0,
            reverse=True
        )
        
        leaderboard = []
        for i, pred in enumerate(sorted_predictions[:top_n], 1):
            leaderboard.append({
                'rank': i,
                'id': pred.id,
                'asset': pred.asset,
                'predicted': pred.predicted_price,
                'actual': pred.actual_price,
                'accuracy': pred.calculate_accuracy(),
                'mae': pred.calculate_mae(),
                'confidence': pred.confidence,
                'predictor': pred.predictor,
                'timestamp': pred.timestamp.isoformat()
            })
        
        return leaderboard
    
    def get_statistics(self) -> Dict:
        """Get overall statistics"""
        verified = [p for p in self.predictions if p.actual_price is not None]
        
        if not verified:
            return {
                'total_predictions': len(self.predictions),
                'verified_predictions': 0,
                'average_accuracy': 0,
                'average_mae': 0,
                'best_accuracy': 0,
                'worst_accuracy': 0
            }
        
        accuracies = [p.calculate_accuracy() for p in verified]
        maes = [p.calculate_mae() for p in verified]
        
        return {
            'total_predictions': len(self.predictions),
            'verified_predictions': len(verified),
            'pending_verification': len(self.predictions) - len(verified),
            'average_accuracy': sum(accuracies) / len(accuracies),
            'average_mae': sum(maes) / len(maes),
            'best_accuracy': max(accuracies),
            'worst_accuracy': min(accuracies),
            'median_accuracy': sorted(accuracies)[len(accuracies)//2],
            'predictions_by_asset': self._count_by_asset()
        }
    
    def _count_by_asset(self) -> Dict[str, int]:
        """Count predictions by asset"""
        counts = {}
        for pred in self.predictions:
            counts[pred.asset] = counts.get(pred.asset, 0) + 1
        return counts
    
    async def auto_verify_pending(self, data_collector):
        """
        Automatically verify pending predictions
        
        Args:
            data_collector: DataCollector instance to fetch current prices
        """
        pending = [
            p for p in self.predictions
            if p.actual_price is None
            and (datetime.now() - p.timestamp) > timedelta(hours=24)
        ]
        
        if not pending:
            logger.info("No pending predictions to verify")
            return
        
        logger.info(f"Verifying {len(pending)} pending predictions...")
        
        for pred in pending:
            try:
                # Fetch current price
                asset_map = {
                    'Bitcoin': 'bitcoin',
                    'Ethereum': 'ethereum',
                    'Solana': 'solana',
                    'Polygon': 'matic-network'
                }
                
                asset_id = asset_map.get(pred.asset, 'bitcoin')
                data = await data_collector.fetch_asset_data(asset_id, days=1)
                
                if len(data) > 0:
                    actual_price = data[-1]
                    self.verify_prediction(pred.id, actual_price)
                
            except Exception as e:
                logger.error(f"Error verifying prediction {pred.id}: {e}")


async def main():
    """Demo accuracy tracker"""
    logger.info("🎯 Starting Accuracy Tracker Demo...")
    
    tracker = AccuracyTracker()
    
    # Add some predictions
    pred_id = tracker.add_prediction(
        asset="Bitcoin",
        predicted_price=50000.0,
        confidence=0.85,
        predictor="DecAI Oracle v1.0"
    )
    
    # Simulate verification
    tracker.verify_prediction(pred_id, actual_price=49800.0)
    
    # Get statistics
    stats = tracker.get_statistics()
    
    print("\n" + "="*60)
    print("📊 ACCURACY STATISTICS")
    print("="*60)
    print(f"Total Predictions: {stats['total_predictions']}")
    print(f"Verified: {stats['verified_predictions']}")
    print(f"Pending: {stats['pending_verification']}")
    print(f"Average Accuracy: {stats['average_accuracy']:.2f}%")
    print(f"Average MAE: ${stats['average_mae']:.2f}")
    print(f"Best Accuracy: {stats['best_accuracy']:.2f}%")
    print("="*60)
    
    # Get leaderboard
    leaderboard = tracker.get_leaderboard(top_n=5)
    
    if leaderboard:
        print("\n" + "="*60)
        print("🏆 LEADERBOARD (Top 5)")
        print("="*60)
        for entry in leaderboard:
            print(f"#{entry['rank']} - {entry['asset']}")
            print(f"   Predicted: ${entry['predicted']:.2f} | Actual: ${entry['actual']:.2f}")
            print(f"   Accuracy: {entry['accuracy']:.2f}% | MAE: ${entry['mae']:.2f}")
            print(f"   Predictor: {entry['predictor']}")
            print()
        print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
