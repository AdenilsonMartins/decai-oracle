"""
Data collection from crypto APIs
"""

import asyncio
from typing import List, Dict
from datetime import datetime
import numpy as np
from pycoingecko import CoinGeckoAPI
from src.utils.logger import setup_logger
from src.utils.config import settings

logger = setup_logger(__name__)


class DataCollector:
    """Collects cryptocurrency data from various sources"""
    
    def __init__(self):
        self.cg = CoinGeckoAPI()
        if settings.COINGECKO_API_KEY:
            self.cg = CoinGeckoAPI(api_key=settings.COINGECKO_API_KEY)
    
    async def fetch_bitcoin_data(self, days: int = 30) -> np.ndarray:
        """
        Fetch Bitcoin price data for the last N days
        
        Args:
            days: Number of days of historical data
        
        Returns:
            NumPy array of prices
        """
        try:
            logger.info(f"Fetching Bitcoin data for last {days} days...")
            
            # CoinGecko API is synchronous, run in executor
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(
                None,
                lambda: self.cg.get_coin_market_chart_by_id(
                    id='bitcoin',
                    vs_currency='usd',
                    days=days
                )
            )
            
            # Extract prices
            prices = np.array([p[1] for p in data['prices']])
            
            logger.info(f"✅ Fetched {len(prices)} price points")
            logger.info(f"Price range: ${prices.min():.2f} - ${prices.max():.2f}")
            
            return prices
            
        except Exception as e:
            logger.error(f"Error fetching Bitcoin data: {e}")
            raise
    
    async def fetch_multi_asset_data(self, assets: List[str], days: int = 30) -> Dict[str, np.ndarray]:
        """
        Fetch data for multiple assets
        
        Args:
            assets: List of asset IDs (e.g., ['bitcoin', 'ethereum'])
            days: Number of days of historical data
        
        Returns:
            Dictionary mapping asset names to price arrays
        """
        tasks = []
        for asset in assets:
            task = self.fetch_asset_data(asset, days)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        data = {}
        for asset, result in zip(assets, results):
            if isinstance(result, Exception):
                logger.error(f"Failed to fetch {asset}: {result}")
            else:
                data[asset] = result
        
        return data
    
    async def fetch_asset_data(self, asset_id: str, days: int = 30) -> np.ndarray:
        """Fetch data for a single asset"""
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None,
            lambda: self.cg.get_coin_market_chart_by_id(
                id=asset_id,
                vs_currency='usd',
                days=days
            )
        )
        return np.array([p[1] for p in data['prices']])
