import logging
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from pycoingecko import CoinGeckoAPI
from config import config


class PriceChecker:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cg = CoinGeckoAPI()
        self.price_cache: Dict[str, Dict] = {}
        self.last_update: Optional[datetime] = None

    async def get_prices(self, coin_ids: List[str]) -> Dict[str, float]:
        """Get current prices for multiple coins with caching"""
        try:
            result_prices = {}

            # First try to get prices from cache
            for coin_id in coin_ids:
                if (self.last_update and
                        datetime.now() - self.last_update <= timedelta(seconds=config.PRICE_CACHE_TIME) and
                        coin_id in self.price_cache):
                    result_prices[coin_id] = self.price_cache[coin_id]['usd']

            # If we got all prices from cache, return them
            if len(result_prices) == len(coin_ids):
                return result_prices

            # Otherwise get fresh prices for all requested coins
            prices = self.cg.get_price(
                ids=coin_ids,
                vs_currencies='usd'
            )

            # Update cache
            self.price_cache = prices
            self.last_update = datetime.now()

            # Return all fresh prices
            return {coin: data['usd'] for coin, data in prices.items()}

        except Exception as e:
            self.logger.error(f"Error fetching prices: {e}")
            return {}

    async def get_price(self, coin_id: str) -> Optional[float]:
        """Get current price for a single coin"""
        try:
            prices = await self.get_prices([coin_id])
            return prices.get(coin_id)
        except:
            return None

    @staticmethod
    def format_price(price: float) -> str:
        """Format price with appropriate precision"""
        if price < 0.01:
            return f"${price:.8f}"
        elif price < 1:
            return f"${price:.4f}"
        elif price < 100:
            return f"${price:.2f}"
        else:
            return f"${price:,.2f}"


price_checker = PriceChecker()