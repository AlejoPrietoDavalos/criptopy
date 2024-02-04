""" Abstracción de la API de Binance."""
from binance.um_futures import UMFutures

from binance_extras.searchs import SearchKLines
from cripto_trading.klines import KLineList


class BinanceManager:
    def __init__(self, key=None, secret=None, **kwargs):
        self._um = UMFutures(key, secret, **kwargs)

    @property
    def um(self) -> UMFutures:
        return self._um
    
    def mark_price_klines(self, search_klines: SearchKLines) -> KLineList:
        klines_binance = self.um.mark_price_klines(**search_klines.model_dump())
        return KLineList.from_binance(klines_binance)
