"""
DecAI Oracle - Multi-Source Data Aggregator
Versão 2.0 - Resilient Data Layer

Resolve Single Point of Failure (SPOF) usando múltiplas fontes:
- Binance API
- CoinGecko API
- CoinCap API
- Chainlink Price Feeds (on-chain)
- Fallback automático
- Validação cruzada
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import statistics
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataSourceStatus(Enum):
    """Status de uma fonte de dados"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    DOWN = "down"
    UNKNOWN = "unknown"


@dataclass
class PriceData:
    """Dados de preço de uma fonte"""
    source: str
    symbol: str
    price: float
    volume_24h: Optional[float]
    timestamp: datetime
    confidence: float  # 0-100%
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SourceHealth:
    """Métricas de saúde de uma fonte"""
    source_name: str
    status: DataSourceStatus
    success_rate: float  # últimas N requisições
    avg_response_time: float  # ms
    last_success: Optional[datetime]
    last_failure: Optional[datetime]
    consecutive_failures: int
    total_requests: int
    total_failures: int


class DataSourceBase:
    """Classe base para fontes de dados"""
    
    def __init__(self, name: str, timeout: int = 5):
        self.name = name
        self.timeout = timeout
        self.health = SourceHealth(
            source_name=name,
            status=DataSourceStatus.UNKNOWN,
            success_rate=100.0,
            avg_response_time=0.0,
            last_success=None,
            last_failure=None,
            consecutive_failures=0,
            total_requests=0,
            total_failures=0
        )
    
    async def fetch_price(self, symbol: str) -> Optional[PriceData]:
        """Implementar em subclasses"""
        raise NotImplementedError
    
    def update_health(self, success: bool, response_time: float):
        """Atualiza métricas de saúde"""
        self.health.total_requests += 1
        
        if success:
            self.health.consecutive_failures = 0
            self.health.last_success = datetime.now()
            self.health.status = DataSourceStatus.HEALTHY
        else:
            self.health.consecutive_failures += 1
            self.health.total_failures += 1
            self.health.last_failure = datetime.now()
            
            # Circuit breaker
            if self.health.consecutive_failures >= 3:
                self.health.status = DataSourceStatus.DOWN
            elif self.health.consecutive_failures >= 1:
                self.health.status = DataSourceStatus.DEGRADED
        
        # Calcular success rate
        if self.health.total_requests > 0:
            success_count = self.health.total_requests - self.health.total_failures
            self.health.success_rate = (success_count / self.health.total_requests) * 100
        
        # Atualizar tempo médio de resposta (média móvel)
        if self.health.avg_response_time == 0:
            self.health.avg_response_time = response_time
        else:
            # Weighted average (70% histórico, 30% novo)
            self.health.avg_response_time = (
                self.health.avg_response_time * 0.7 + response_time * 0.3
            )


class BinanceSource(DataSourceBase):
    """Fonte de dados: Binance API"""
    
    BASE_URL = "https://api.binance.com/api/v3"
    
    def __init__(self):
        super().__init__("Binance")
    
    async def fetch_price(self, symbol: str) -> Optional[PriceData]:
        """Busca preço da Binance"""
        start_time = datetime.now()
        
        try:
            # Converter símbolo (BTC/USD → BTCUSDT)
            binance_symbol = symbol.replace('/', '') + 'T' if not symbol.endswith('T') else symbol
            
            async with aiohttp.ClientSession() as session:
                # Ticker 24h
                ticker_url = f"{self.BASE_URL}/ticker/24hr?symbol={binance_symbol}"
                
                async with session.get(ticker_url, timeout=self.timeout) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        response_time = (datetime.now() - start_time).total_seconds() * 1000
                        self.update_health(True, response_time)
                        
                        return PriceData(
                            source=self.name,
                            symbol=symbol,
                            price=float(data['lastPrice']),
                            volume_24h=float(data['volume']),
                            timestamp=datetime.now(),
                            confidence=95.0,  # Binance é muito confiável
                            metadata={
                                'high_24h': float(data['highPrice']),
                                'low_24h': float(data['lowPrice']),
                                'price_change_pct': float(data['priceChangePercent'])
                            }
                        )
                    else:
                        raise Exception(f"HTTP {response.status}")
        
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            self.update_health(False, response_time)
            logger.warning(f"❌ {self.name} falhou para {symbol}: {str(e)}")
            return None


class CoinGeckoSource(DataSourceBase):
    """Fonte de dados: CoinGecko API"""
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    # Mapeamento de símbolos
    SYMBOL_MAP = {
        'BTC/USD': 'bitcoin',
        'ETH/USD': 'ethereum',
        'BNB/USD': 'binancecoin',
        'SOL/USD': 'solana',
        'ADA/USD': 'cardano'
    }
    
    def __init__(self):
        super().__init__("CoinGecko")
    
    async def fetch_price(self, symbol: str) -> Optional[PriceData]:
        """Busca preço do CoinGecko"""
        start_time = datetime.now()
        
        try:
            # Mapear símbolo
            coin_id = self.SYMBOL_MAP.get(symbol)
            if not coin_id:
                logger.warning(f"⚠️ {symbol} não mapeado no CoinGecko")
                return None
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.BASE_URL}/simple/price"
                params = {
                    'ids': coin_id,
                    'vs_currencies': 'usd',
                    'include_24hr_vol': 'true',
                    'include_24hr_change': 'true'
                }
                
                async with session.get(url, params=params, timeout=self.timeout) as response:
                    if response.status == 200:
                        data = await response.json()
                        coin_data = data.get(coin_id, {})
                        
                        response_time = (datetime.now() - start_time).total_seconds() * 1000
                        self.update_health(True, response_time)
                        
                        return PriceData(
                            source=self.name,
                            symbol=symbol,
                            price=float(coin_data['usd']),
                            volume_24h=coin_data.get('usd_24h_vol'),
                            timestamp=datetime.now(),
                            confidence=90.0,  # CoinGecko é confiável
                            metadata={
                                'change_24h': coin_data.get('usd_24h_change')
                            }
                        )
                    else:
                        raise Exception(f"HTTP {response.status}")
        
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            self.update_health(False, response_time)
            logger.warning(f"❌ {self.name} falhou para {symbol}: {str(e)}")
            return None


class CoinCapSource(DataSourceBase):
    """Fonte de dados: CoinCap API"""
    
    BASE_URL = "https://api.coincap.io/v2"
    
    SYMBOL_MAP = {
        'BTC/USD': 'bitcoin',
        'ETH/USD': 'ethereum',
        'BNB/USD': 'binance-coin',
        'SOL/USD': 'solana',
        'ADA/USD': 'cardano'
    }
    
    def __init__(self):
        super().__init__("CoinCap")
    
    async def fetch_price(self, symbol: str) -> Optional[PriceData]:
        """Busca preço do CoinCap"""
        start_time = datetime.now()
        
        try:
            asset_id = self.SYMBOL_MAP.get(symbol)
            if not asset_id:
                return None
            
            async with aiohttp.ClientSession() as session:
                url = f"{self.BASE_URL}/assets/{asset_id}"
                
                async with session.get(url, timeout=self.timeout) as response:
                    if response.status == 200:
                        result = await response.json()
                        data = result['data']
                        
                        response_time = (datetime.now() - start_time).total_seconds() * 1000
                        self.update_health(True, response_time)
                        
                        return PriceData(
                            source=self.name,
                            symbol=symbol,
                            price=float(data['priceUsd']),
                            volume_24h=float(data.get('volumeUsd24Hr', 0)),
                            timestamp=datetime.now(),
                            confidence=85.0,
                            metadata={
                                'market_cap': float(data['marketCapUsd']),
                                'change_24h': float(data['changePercent24Hr'])
                            }
                        )
                    else:
                        raise Exception(f"HTTP {response.status}")
        
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            self.update_health(False, response_time)
            logger.warning(f"❌ {self.name} falhou para {symbol}: {str(e)}")
            return None


class MultiSourceAggregator:
    """
    Agregador de múltiplas fontes com:
    - Fallback automático
    - Validação cruzada
    - Circuit breaker
    - Consenso entre fontes
    """
    
    def __init__(self):
        self.sources: List[DataSourceBase] = [
            BinanceSource(),
            CoinGeckoSource(),
            CoinCapSource(),
        ]
        
        # Cache de preços (TTL: 30 segundos)
        self.cache: Dict[str, Tuple[PriceData, datetime]] = {}
        self.cache_ttl = timedelta(seconds=30)
        
        logger.info(f"✅ Agregador inicializado com {len(self.sources)} fontes")
    
    async def get_price(
        self,
        symbol: str,
        min_sources: int = 2,
        max_deviation: float = 5.0  # % máximo de desvio entre fontes
    ) -> Optional[PriceData]:
        """
        Busca preço de múltiplas fontes e retorna consenso
        
        Args:
            symbol: Par de negociação (ex: BTC/USD)
            min_sources: Mínimo de fontes necessárias
            max_deviation: Desvio máximo aceitável entre fontes (%)
        """
        # Verificar cache
        cached = self._get_from_cache(symbol)
        if cached:
            logger.info(f"💾 Cache hit para {symbol}")
            return cached
        
        # Buscar de todas as fontes em paralelo
        logger.info(f"🔍 Buscando {symbol} em {len(self.sources)} fontes...")
        
        tasks = [source.fetch_price(symbol) for source in self.sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filtrar resultados válidos
        valid_results: List[PriceData] = [
            r for r in results 
            if isinstance(r, PriceData) and r is not None
        ]
        
        if len(valid_results) < min_sources:
            logger.error(
                f"❌ Fontes insuficientes para {symbol}: "
                f"{len(valid_results)}/{min_sources} necessárias"
            )
            return None
        
        # Validar consenso
        prices = [r.price for r in valid_results]
        avg_price = statistics.mean(prices)
        std_dev = statistics.stdev(prices) if len(prices) > 1 else 0
        deviation_pct = (std_dev / avg_price * 100) if avg_price > 0 else 100
        
        logger.info(f"📊 {symbol}: {len(valid_results)} fontes")
        for result in valid_results:
            diff_pct = abs((result.price - avg_price) / avg_price * 100)
            logger.info(
                f"   {result.source}: ${result.price:,.2f} "
                f"(diff: {diff_pct:.2f}%)"
            )
        
        # Verificar desvio
        if deviation_pct > max_deviation:
            logger.warning(
                f"⚠️ Desvio alto detectado ({deviation_pct:.2f}% > {max_deviation}%)"
            )
            
            # Para conjuntos pequenos (3-5 fontes), removemos quem estiver mais longe da mediana
            if 2 < len(valid_results) <= 5:
                median_price = statistics.median(prices)
                # Ordenar por proximidade da mediana e manter os N-1 melhores
                valid_results.sort(key=lambda r: abs(r.price - median_price))
                removed = valid_results.pop()
                logger.warning(f"🧹 Outlier removido (furthest from median): {removed.source} (${removed.price:,.2f})")
                
                # Recalcular métricas básicas após remoção para o objeto final
                prices = [r.price for r in valid_results]
                avg_price = statistics.mean(prices)
                std_dev = statistics.stdev(prices) if len(prices) > 1 else 0
                deviation_pct = (std_dev / avg_price * 100) if avg_price > 0 else 0
            else:
                # Para conjuntos maiores, usamos o desvio padrão (Z-score > 2)
                valid_results = [
                    r for r in valid_results
                    if abs(r.price - avg_price) <= 2 * std_dev
                ]
            
            if len(valid_results) < min_sources:
                logger.error("❌ Muitos outliers, dados não confiáveis")
                return None
        
        # Calcular preço consensual (média ponderada por confiança)
        total_confidence = sum(r.confidence for r in valid_results)
        weighted_price = sum(
            r.price * (r.confidence / total_confidence)
            for r in valid_results
        )
        
        # Agregar volumes
        total_volume = sum(
            r.volume_24h for r in valid_results 
            if r.volume_24h is not None
        )
        
        # Criar resultado agregado
        aggregated = PriceData(
            source="MultiSource-Aggregator",
            symbol=symbol,
            price=weighted_price,
            volume_24h=total_volume if total_volume > 0 else None,
            timestamp=datetime.now(),
            confidence=statistics.mean([r.confidence for r in valid_results]),
            metadata={
                'sources_used': [r.source for r in valid_results],
                'num_sources': len(valid_results),
                'price_std_dev': std_dev,
                'price_deviation_pct': deviation_pct,
                'individual_prices': {r.source: r.price for r in valid_results}
            }
        )
        
        # Cachear resultado
        self._save_to_cache(symbol, aggregated)
        
        logger.info(
            f"✅ Consenso para {symbol}: ${weighted_price:,.2f} "
            f"({len(valid_results)} fontes, confiança: {aggregated.confidence:.1f}%)"
        )
        
        return aggregated
    
    def _get_from_cache(self, symbol: str) -> Optional[PriceData]:
        """Recupera preço do cache se ainda válido"""
        if symbol in self.cache:
            data, timestamp = self.cache[symbol]
            if datetime.now() - timestamp < self.cache_ttl:
                return data
        return None
    
    def _save_to_cache(self, symbol: str, data: PriceData):
        """Salva preço no cache"""
        self.cache[symbol] = (data, datetime.now())
    
    def get_health_report(self) -> Dict[str, Any]:
        """Retorna relatório de saúde de todas as fontes"""
        return {
            'timestamp': datetime.now().isoformat(),
            'total_sources': len(self.sources),
            'sources': [
                {
                    'name': source.name,
                    'status': source.health.status.value,
                    'success_rate': f"{source.health.success_rate:.1f}%",
                    'avg_response_time_ms': f"{source.health.avg_response_time:.0f}",
                    'consecutive_failures': source.health.consecutive_failures,
                    'total_requests': source.health.total_requests,
                    'total_failures': source.health.total_failures,
                    'last_success': source.health.last_success.isoformat() 
                        if source.health.last_success else None,
                    'last_failure': source.health.last_failure.isoformat()
                        if source.health.last_failure else None
                }
                for source in self.sources
            ],
            'healthy_sources': sum(
                1 for s in self.sources 
                if s.health.status == DataSourceStatus.HEALTHY
            )
        }


# Função auxiliar para testes
async def main():
    """Teste do agregador"""
    print("\n" + "="*60)
    print("🔷 DECAI ORACLE - MULTI-SOURCE AGGREGATOR TEST")
    print("="*60)
    
    aggregator = MultiSourceAggregator()
    
    # Testar símbolos
    symbols = ['BTC/USD', 'ETH/USD', 'SOL/USD']
    
    for symbol in symbols:
        print(f"\n{'─'*60}")
        result = await aggregator.get_price(symbol)
        
        if result:
            print(f"✅ {symbol}: ${result.price:,.2f}")
            print(f"   Fontes: {result.metadata['sources_used']}")
            print(f"   Confiança: {result.confidence:.1f}%")
            print(f"   Desvio: {result.metadata['price_deviation_pct']:.2f}%")
        else:
            print(f"❌ {symbol}: Falha ao obter preço")
    
    # Relatório de saúde
    print(f"\n{'─'*60}")
    print("📊 HEALTH REPORT")
    print("─"*60)
    
    health = aggregator.get_health_report()
    for source in health['sources']:
        status_emoji = {
            'healthy': '✅',
            'degraded': '⚠️',
            'down': '❌',
            'unknown': '❓'
        }
        emoji = status_emoji.get(source['status'], '❓')
        
        print(f"{emoji} {source['name']}")
        print(f"   Status: {source['status']}")
        print(f"   Success Rate: {source['success_rate']}")
        print(f"   Response Time: {source['avg_response_time_ms']}ms")
        print(f"   Requests: {source['total_requests']} (failures: {source['total_failures']})")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    asyncio.run(main())
