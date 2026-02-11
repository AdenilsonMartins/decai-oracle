"""
Unit tests for Gas Fees Predictor
"""

import pytest
import numpy as np
from src.ml.gas_fees_predictor import GasFeesPredictor

@pytest.fixture
def predictor():
    return GasFeesPredictor()

@pytest.fixture
def mock_gas_data(predictor):
    # Use internal mock data generator
    return predictor._generate_mock_gas_data(hours=5)

def test_gas_history_fetch(predictor):
    # This should return mock data when no RPC configured
    import asyncio
    data = asyncio.run(predictor.fetch_gas_history(hours=1))
    assert len(data) > 0
    assert 'base_fee' in data[0]

def test_training(predictor, mock_gas_data):
    predictor.train(mock_gas_data)
    assert predictor.is_trained

def test_recommendations(predictor, mock_gas_data):
    predictor.train(mock_gas_data)
    current_fee = 20.0
    preds = predictor.predict_gas_fee(current_fee)
    
    assert preds['slow'] < preds['fast']
    assert preds['instant'] > preds['standard']
    assert 'timestamp' in preds

def test_optimal_time(predictor, mock_gas_data):
    predictor.train(mock_gas_data)
    optimal = predictor.get_optimal_time(mock_gas_data, hours_ahead=12)
    
    assert 'optimal_fee' in optimal
    assert 'hours_from_now' in optimal
    assert optimal['hours_from_now'] >= 0
