import pytest
import asyncio
import statistics
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime
from src.data.data_aggregator import MultiSourceAggregator, PriceData, DataSourceStatus

class TestResilience:
    @pytest.fixture
    def aggregator(self):
        return MultiSourceAggregator()

    @pytest.mark.asyncio
    async def test_scenario_primary_source_down(self, aggregator):
        """
        Cenário 1: Fonte Principal (Binance) Cai
        O sistema deve continuar operando usando CoinGecko e CoinCap.
        """
        # Mock Binance para falhar
        with patch('src.data.data_aggregator.BinanceSource.fetch_price', new_callable=AsyncMock) as mock_binance:
            mock_binance.return_value = None
            
            # Mock CoinGecko e CoinCap para sucesso
            with patch('src.data.data_aggregator.CoinGeckoSource.fetch_price', new_callable=AsyncMock) as mock_gecko, \
                 patch('src.data.data_aggregator.CoinCapSource.fetch_price', new_callable=AsyncMock) as mock_cap:
                
                mock_gecko.return_value = PriceData(
                    source="CoinGecko", symbol="BTC/USD", price=50000.0, 
                    volume_24h=1000, timestamp=datetime.now(), confidence=90.0
                )
                mock_cap.return_value = PriceData(
                    source="CoinCap", symbol="BTC/USD", price=50010.0, 
                    volume_24h=1000, timestamp=datetime.now(), confidence=85.0
                )
                
                result = await aggregator.get_price("BTC/USD", min_sources=2)
                
                assert result is not None
                assert result.source == "MultiSource-Aggregator"
                assert "Binance" not in result.metadata['sources_used']
                assert "CoinGecko" in result.metadata['sources_used']
                assert "CoinCap" in result.metadata['sources_used']
                assert result.metadata['num_sources'] == 2

    @pytest.mark.asyncio
    async def test_scenario_divergent_data_outlier(self, aggregator):
        """
        Cenário 2: Dados Divergentes (Anomalia/Outlier)
        Uma fonte retorna um valor absurdo (ex: $60k enquanto outras estão em $50k).
        O sistema deve descartar o outlier.
        """
        with patch('src.data.data_aggregator.BinanceSource.fetch_price', new_callable=AsyncMock) as mock_binance, \
             patch('src.data.data_aggregator.CoinGeckoSource.fetch_price', new_callable=AsyncMock) as mock_gecko, \
             patch('src.data.data_aggregator.CoinCapSource.fetch_price', new_callable=AsyncMock) as mock_cap:
            
            mock_binance.return_value = PriceData(
                source="Binance", symbol="BTC/USD", price=50000.0, 
                volume_24h=1000, timestamp=datetime.now(), confidence=95.0
            )
            mock_gecko.return_value = PriceData(
                source="CoinGecko", symbol="BTC/USD", price=50100.0, 
                volume_24h=1000, timestamp=datetime.now(), confidence=90.0
            )
            mock_cap.return_value = PriceData(
                source="CoinCap", symbol="BTC/USD", price=80000.0, # OUTLIER!
                volume_24h=1000, timestamp=datetime.now(), confidence=85.0
            )
            
            # Usamos um max_deviation baixo para forçar a detecção de anomalia
            result = await aggregator.get_price("BTC/USD", min_sources=2, max_deviation=5.0)
            
            assert result is not None
            # O preço final não deve ser influenciado pelo de 80.000
            assert result.price < 55000.0
            assert "CoinCap" not in result.metadata['sources_used']
            assert result.metadata['num_sources'] == 2

    @pytest.mark.asyncio
    async def test_circuit_breaker_activation(self, aggregator):
        """
        Testa o Circuit Breaker: após 3 falhas consecutivas, a fonte deve ser marcada como DOWN.
        """
        binance = aggregator.sources[0] # Assumindo que Binance é a primeira
        
        # Simular 3 falhas
        with patch('src.data.data_aggregator.aiohttp.ClientSession.get') as mock_get:
            mock_get.side_effect = Exception("Connection Timeout")
            
            for _ in range(3):
                await binance.fetch_price("BTC/USD")
            
            assert binance.health.consecutive_failures == 3
            assert binance.health.status == DataSourceStatus.DOWN

    @pytest.mark.asyncio
    async def test_cache_resilience(self, aggregator):
        """
        Testa se o cache evita chamadas desnecessárias e provê dados se as fontes falharem temporariamente.
        """
        # 1. Popula cache
        with patch('src.data.data_aggregator.BinanceSource.fetch_price', new_callable=AsyncMock) as mock_binance, \
             patch('src.data.data_aggregator.CoinGeckoSource.fetch_price', new_callable=AsyncMock) as mock_gecko:
            
            mock_binance.return_value = PriceData(
                source="Binance", symbol="BTC/USD", price=50000.0, 
                volume_24h=1000, timestamp=datetime.now(), confidence=95.0
            )
            mock_gecko.return_value = PriceData(
                source="CoinGecko", symbol="BTC/USD", price=50000.0, 
                volume_24h=1000, timestamp=datetime.now(), confidence=90.0
            )
            
            first_result = await aggregator.get_price("BTC/USD")
            assert first_result.price == 50000.0
            
            # 2. Mock falhas totais logo em seguida
            mock_binance.return_value = None
            mock_gecko.return_value = None
            
            # Deve retornar do cache sem erros
            second_result = await aggregator.get_price("BTC/USD")
            assert second_result.price == 50000.0
            assert second_result.timestamp == first_result.timestamp
