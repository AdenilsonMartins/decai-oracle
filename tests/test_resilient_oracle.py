
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from src.resilient_oracle import ResilientOracleSystem
from src.data.data_aggregator import PriceData

@pytest.fixture
def mock_price_data():
    return PriceData(
        source="MultiSource-Aggregator",
        symbol="BTC/USD",
        price=50000.0,
        volume_24h=1000000.0,
        timestamp=datetime.now(),
        confidence=95.0,
        metadata={
            'sources_used': ['Binance', 'CoinGecko'],
            'num_sources': 2,
            'price_deviation_pct': 0.1,
            'individual_prices': {'Binance': 50000.0, 'CoinGecko': 50000.0}
        }
    )

@pytest.mark.asyncio
class TestResilientOracle:

    @patch('src.resilient_oracle.MultiSourceAggregator')
    @patch('src.resilient_oracle.ContractManager')
    async def test_initialization(self, mock_contract_mgr, mock_aggregator):
        """Testa se o sistema inicializa corretamente os subsistemas"""
        oracle = ResilientOracleSystem()
        assert oracle.aggregator is not None
        assert oracle.contract_manager is not None
        assert oracle.predictions_count == 0

    @patch('src.resilient_oracle.MultiSourceAggregator')
    @patch('src.resilient_oracle.ContractManager')
    async def test_generate_prediction_success(self, mock_contract_mgr, mock_aggregator, mock_price_data):
        """Testa a geração de previsão quando o agregador retorna dados válidos"""
        # Setup mocks
        aggregator_instance = mock_aggregator.return_value
        aggregator_instance.get_price = AsyncMock(return_value=mock_price_data)
        
        oracle = ResilientOracleSystem()
        
        # Execute
        prediction = await oracle.generate_prediction("BTC/USD")
        
        # Verify
        assert prediction is not None
        assert prediction['symbol'] == "BTC/USD"
        assert prediction['current_price'] == 50000.0
        # Check simulated logic (+2%)
        assert prediction['predicted_price'] == 51000.0 
        assert prediction['data_quality']['num_sources'] == 2

    @patch('src.resilient_oracle.MultiSourceAggregator')
    @patch('src.resilient_oracle.ContractManager')
    async def test_generate_prediction_failure(self, mock_contract_mgr, mock_aggregator):
        """Testa comportamento quando o agregador falha (retorna None)"""
        # Setup mocks
        aggregator_instance = mock_aggregator.return_value
        aggregator_instance.get_price = AsyncMock(return_value=None)
        
        oracle = ResilientOracleSystem()
        
        # Execute
        prediction = await oracle.generate_prediction("BTC/USD")
        
        # Verify
        assert prediction is None

    @patch('src.resilient_oracle.MultiSourceAggregator')
    @patch('src.resilient_oracle.ContractManager')
    async def test_store_prediction_on_chain(self, mock_contract_mgr, mock_aggregator):
        """Testa o envio da previsão para o blockchain"""
        # Setup mocks
        contract_instance = mock_contract_mgr.return_value
        contract_instance.store_prediction.return_value = {
            'success': True,
            'tx_hash': '0x123...',
            'block_number': 100
        }
        
        oracle = ResilientOracleSystem()
        prediction_data = {
            'symbol': 'BTC/USD',
            'predicted_price': 50000.0,
            'model_version': 'v1',
            'prediction_confidence': 90.0
        }
        
        # Execute
        result = await oracle.store_prediction_on_chain(prediction_data)
        
        # Verify
        assert result['success'] is True
        assert result['tx_hash'] == '0x123...'
        assert 'blockchain' in prediction_data
        assert prediction_data['blockchain']['tx_hash'] == '0x123...'
        assert oracle.predictions_count == 1

    @patch('src.resilient_oracle.MultiSourceAggregator')
    @patch('src.resilient_oracle.ContractManager')
    async def test_run_prediction_cycle(self, mock_contract_mgr, mock_aggregator):
        """Testa o ciclo de previsão isolado"""
        oracle = ResilientOracleSystem()
        
        # Mocking methods on the instance
        oracle.generate_prediction = AsyncMock(side_effect=[
            {'symbol': 'BTC/USD', 'predicted_price': 50000.0, 'prediction_confidence': 95.0},
            {'symbol': 'ETH/USD', 'predicted_price': 3000.0, 'prediction_confidence': 90.0}
        ])
        
        oracle.store_prediction_on_chain = AsyncMock(return_value={'success': True, 'tx_hash': '0xabc'})
        oracle.print_cycle_summary = MagicMock() # Silenciar print
        
        # Execute
        results = await oracle.run_prediction_cycle(['BTC/USD', 'ETH/USD'])
        
        # Verify
        assert len(results) == 2
        assert results[0]['success'] is True
        assert results[1]['success'] is True
        assert results[0]['symbol'] == 'BTC/USD'
        assert results[1]['symbol'] == 'ETH/USD'
