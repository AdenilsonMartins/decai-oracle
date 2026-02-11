"""
Unit tests for ML Predictor
"""

import pytest
import numpy as np
from src.ml.predictor import Predictor

@pytest.fixture
def mock_price_data():
    return np.array([40000.0, 41000.0, 40500.0, 42000.0, 43000.0])

def test_predictor_training(mock_price_data):
    predictor = Predictor()
    predictor.train(mock_price_data)
    
    assert predictor.is_trained
    assert predictor.train_score is not None
    assert predictor.model is not None

def test_prediction_output(mock_price_data):
    predictor = Predictor()
    predictor.train(mock_price_data)
    
    prediction = predictor.predict_next_day()
    assert isinstance(prediction, float)
    assert prediction > 0

def test_confidence_score(mock_price_data):
    predictor = Predictor()
    predictor.train(mock_price_data)
    
    confidence = predictor.get_confidence()
    assert 0.0 <= confidence <= 1.0

def test_not_trained_error():
    predictor = Predictor()
    with pytest.raises(ValueError):
        predictor.predict_next_day()
