import logging
from typing import Dict, List, Optional
from pycoingecko import CoinGeckoAPI
from config import Config
from datetime import datetime


class CoinManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.init_date = datetime.now()
        self.cg = CoinGeckoAPI()
        self.symbol_to_id: Dict[str, str] = {}
        self.name_to_id: Dict[str, str] = {}
        self.display_names: Dict[str, str] = {}
        self.initialize_coins()

    def __add_to(self, items: List[Dict]) -> None:
        """Add coins to mapping dictionaries"""
        for coin in items:
            symbol = coin['symbol'].lower()
            coin_id = coin['id']
            name = coin['name'].lower()

            # Don't override existing mappings (preserves priority)
            if symbol not in self.symbol_to_id:
                self.symbol_to_id[symbol] = coin_id
            if name not in self.name_to_id:
                self.name_to_id[name] = coin_id
            if coin_id not in self.display_names:
                self.display_names[coin_id] = coin['name']

    def initialize_coins(self) -> None:
        """Initialize coin mappings from multiple sources"""
        try:
            self.logger.info("Fetching coins list from CoinGecko...")

            # Reset mappings
            self.symbol_to_id.clear()
            self.name_to_id.clear()
            self.display_names.clear()  # Added this

            all_coins = self.cg.get_coins_list()
            self.__add_to(all_coins)

            self.logger.info(f"Initialized {len(self.symbol_to_id)} coins by symbol")
            self.logger.info(f"Initialized {len(self.name_to_id)} coins by name")
            self.logger.info(f"Initialized {len(self.display_names)} display names")  # Added this

        except Exception as e:
            self.logger.error(f"Error initializing coins: {e}")
            raise

    def get_coin_name(self, coin_id: str) -> Optional[str]:
        """Get original case-sensitive name for a coin ID"""
        return self.display_names.get(coin_id)

    def get_coin_id(self, user_input: str) -> Optional[str]:
        """Get coin ID from symbol or name"""
        user_input = user_input.lower()
        return Config.SYMBOL_PRIORITY_MAP.get(user_input) or self.name_to_id.get(user_input) or self.symbol_to_id.get(user_input)

    def get_coin_id_by_symbol(self, symbol: str) -> Optional[str]:
        """Get coin ID by symbol only"""
        return self.symbol_to_id.get(symbol.lower())

    def get_coin_id_by_name(self, name: str) -> Optional[str]:
        """Get coin ID by name only"""
        return self.name_to_id.get(name.lower())


# Create singleton instance
coin_manager = CoinManager()