import pytest
import numpy as np
import asyncio
from unittest.mock import Mock, patch
from src.ml.predictor import Predictor
from src.ml.data_collector import DataCollector

class TestPredictor:
    @pytest.fixture
    def predictor(self):
        """Fixture providing a fresh Predictor instance"""
        return Predictor()

    def test_predictor_initialization(self, predictor):
        """Test if the predictor initializes with default values"""
        assert predictor.is_trained is False
        assert predictor.train_score is None
        assert predictor.test_score is None
        assert predictor.prices is None

    def test_train_with_valid_data(self, predictor):
        """Test training with a valid set of historical prices"""
        # Create synthetic linear data: y = 2x + 100
        prices = np.array([100, 102, 104, 106, 108, 110, 112, 114, 116, 118])
        predictor.train(prices, test_size=0.2)
        
        assert predictor.is_trained is True
        assert predictor.train_score is not None
        assert predictor.test_score is not None
        assert predictor.train_score > 0.99
        assert predictor.test_score > 0.99

    def test_predict_next_day_untrained_raises_error(self, predictor):
        """Test that calling predict_next_day before training raises ValueError"""
        with pytest.raises(ValueError, match="Model not trained yet"):
            predictor.predict_next_day()

    def test_predict_next_day_accuracy(self, predictor):
        """Test prediction for the next day with linear data"""
        prices = np.array([100, 102, 104, 106, 108, 110, 112, 114, 116, 118])
        predictor.train(prices, test_size=0.2)
        
        # Next day (index 10) should be 120
        prediction = predictor.predict_next_day()
        assert pytest.approx(prediction, rel=1e-5) == 120.0

    def test_get_confidence_untrained(self, predictor):
        """Test that get_confidence returns 0.0 for untrained model"""
        assert predictor.get_confidence() == 0.0

    def test_get_confidence_trained(self, predictor):
        """Test get_confidence for a trained model"""
        prices = np.array([100, 102, 104, 106, 108, 110, 112, 114, 116, 118])
        predictor.train(prices, test_size=0.2)
        
        confidence = predictor.get_confidence()
        assert 0.0 <= confidence <= 1.0
        assert confidence > 0.9

    def test_predict_future(self, predictor):
        """Test predicting multiple future days"""
        prices = np.array([100, 102, 104, 106, 108, 110, 112, 114, 116, 118])
        predictor.train(prices, test_size=0.2)
        
        predictions = predictor.predict_future(days=3)
        assert len(predictions) == 3
        assert pytest.approx(predictions[0], rel=1e-5) == 120.0
        assert pytest.approx(predictions[1], rel=1e-5) == 122.0
        assert pytest.approx(predictions[2], rel=1e-5) == 124.0

    def test_predict_future_untrained_raises_error(self, predictor):
        """Test that calling predict_future before training raises ValueError"""
        with pytest.raises(ValueError, match="Model not trained yet"):
            predictor.predict_future(days=5)

class TestDataCollector:
    @pytest.mark.asyncio
    async def test_fetch_bitcoin_data_success(self):
        """Test successful Bitcoin data fetching with mock API"""
        with patch('src.ml.data_collector.CoinGeckoAPI') as MockCG:
            mock_cg_instance = MockCG.return_value
            mock_cg_instance.get_coin_market_chart_by_id.return_value = {
                'prices': [
                    [1707523200000, 45000.0],
                    [1707609600000, 46000.0],
                    [1707696000000, 47000.0]
                ]
            }
            
            collector = DataCollector()
            prices = await collector.fetch_bitcoin_data(days=3)
            
            assert isinstance(prices, np.ndarray)
            assert len(prices) == 3
            assert prices[0] == 45000.0
            assert prices[2] == 47000.0
            mock_cg_instance.get_coin_market_chart_by_id.assert_called_once_with(
                id='bitcoin', vs_currency='usd', days=3
            )

    @pytest.mark.asyncio
    async def test_fetch_bitcoin_data_failure(self):
        """Test data fetching failure handling"""
        with patch('src.ml.data_collector.CoinGeckoAPI') as MockCG:
            mock_cg_instance = MockCG.return_value
            mock_cg_instance.get_coin_market_chart_by_id.side_effect = Exception("API Link Down")
            
            collector = DataCollector()
            with pytest.raises(Exception, match="API Link Down"):
                await collector.fetch_bitcoin_data(days=3)

    @pytest.mark.asyncio
    async def test_fetch_multi_asset_data(self):
        """Test multi-asset data collection orchestration"""
        with patch('src.ml.data_collector.CoinGeckoAPI') as MockCG:
            mock_cg_instance = MockCG.return_value
            mock_cg_instance.get_coin_market_chart_by_id.side_effect = [
                {'prices': [[1, 10], [2, 11]]},
                {'prices': [[1, 20], [2, 21]]}
            ]
            
            collector = DataCollector()
            assets = ['bitcoin', 'ethereum']
            data = await collector.fetch_multi_asset_data(assets, days=2)
            
            assert len(data) == 2
            assert 'bitcoin' in data
            assert 'ethereum' in data
            assert data['bitcoin'][0] == 10
            assert data['ethereum'][0] == 20
            assert mock_cg_instance.get_coin_market_chart_by_id.call_count == 2
