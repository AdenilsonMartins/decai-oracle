"""
ML Predictor - Trains models and makes predictions
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class Predictor:
    """Machine Learning predictor for crypto prices"""
    
    def __init__(self):
        self.model = LinearRegression()
        self.is_trained = False
        self.train_score = None
        self.test_score = None
        self.prices = None
    
    def train(self, prices: np.ndarray, test_size: float = 0.2):
        """
        Train the prediction model
        
        Args:
            prices: Array of historical prices
            test_size: Fraction of data to use for testing
        """
        logger.info("Training ML model...")
        
        # Prepare features (days) and targets (prices)
        self.prices = prices
        dates = np.arange(len(prices)).reshape(-1, 1)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            dates, prices, test_size=test_size, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_pred = self.model.predict(X_train)
        test_pred = self.model.predict(X_test)
        
        self.train_score = r2_score(y_train, train_pred)
        self.test_score = r2_score(y_test, test_pred)
        
        train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
        test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
        
        logger.info(f"✅ Model trained successfully")
        logger.info(f"Train R²: {self.train_score:.4f}, RMSE: ${train_rmse:.2f}")
        logger.info(f"Test R²: {self.test_score:.4f}, RMSE: ${test_rmse:.2f}")
        
        self.is_trained = True
    
    def predict_next_day(self) -> float:
        """
        Predict price for the next day
        
        Returns:
            Predicted price
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet. Call train() first.")
        
        # Predict for day after last data point
        next_day = np.array([[len(self.prices)]])
        prediction = self.model.predict(next_day)[0]
        
        logger.info(f"Predicted next day price: ${prediction:.2f}")
        
        return float(prediction)
    
    def get_confidence(self) -> float:
        """
        Get prediction confidence based on test score
        
        Returns:
            Confidence score (0-1)
        """
        if not self.is_trained:
            return 0.0
        
        # Use R² score as confidence (clamp to 0-1)
        confidence = max(0.0, min(1.0, self.test_score))
        return confidence
    
    def predict_future(self, days: int) -> np.ndarray:
        """
        Predict prices for multiple future days
        
        Args:
            days: Number of days to predict
        
        Returns:
            Array of predicted prices
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet. Call train() first.")
        
        future_days = np.arange(len(self.prices), len(self.prices) + days).reshape(-1, 1)
        predictions = self.model.predict(future_days)
        
        return predictions
