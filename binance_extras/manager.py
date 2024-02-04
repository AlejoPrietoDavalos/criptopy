""" Abstracción de la API de Binance."""
from typing import List

from binance.um_futures import UMFutures

from binance_extras.searchs import SearchKLines
from cripto_trading.kline import KLine

class BinanceManager:
    def __init__(self, key=None, secret=None, **kwargs):
        self._um = UMFutures(key, secret, **kwargs)

    @property
    def um(self) -> UMFutures:
        return self._um
    
    def mark_price_klines(self, search_klines: SearchKLines) -> List[KLine]:
        return [KLine.from_binance(kline) for kline in self.um.mark_price_klines(**search_klines.model_dump())]
