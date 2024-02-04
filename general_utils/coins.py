""" Este módulo contiene todas las monedas de interés."""
from typing import Generator, Tuple, Dict
from enum import Enum

__all__ = [
    "USDT", "BTC", "ETH", "BNB", "AXS",
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "AXSUSDT",
    "IntervalKLineEnum", "SymbolEnum", "SymbolPairsEnum", "iter_all_symbol_interval",
]


# Símbolos de las cripto.
USDT = "USDT"
BTC = "BTC"
ETH = "ETH"
BNB = "BNB"
AXS = "AXS"


# Pares de símbolos de cripto con USDT.
BTCUSDT = BTC + USDT
ETHUSDT = ETH + USDT
BNBUSDT = BNB + USDT
AXSUSDT = AXS + USDT


class SymbolEnum(Enum):
    """ Símbolos de las cripto."""
    USDT = USDT
    BTC = BTC
    ETH = ETH
    BNB = BNB
    AXS = AXS


class SymbolPairsEnum(Enum):
    """ Pares de símbolos de cripto con USDT."""
    BTCUSDT = BTCUSDT
    ETHUSDT = ETHUSDT
    BNBUSDT = BNBUSDT
    AXSUSDT = AXSUSDT




INTERVAL_1M = "1m"
INTERVAL_5M = "5m"
INTERVAL_1H = "1h"
INTERVAL_1D = "1d"

class IntervalKLineEnum(Enum):
    """ Intervalos existentes de KLines."""
    interval_1m = INTERVAL_1M
    interval_5m = INTERVAL_5M
    interval_1h = INTERVAL_1H
    interval_1d = INTERVAL_1D

    @property
    def unit2minutes(self) -> Dict[str, int]:
        return {'m': 1, 'h': 60, 'd': 1440}

    @property
    def minutes(self) -> int:
        value, unit = int(self.value[:-1]), self.value[-1]
        return value * self.unit2minutes[unit]
    
    @property
    def seconds(self) -> int:
        return self.minutes * 60
    
    @property
    def microseconds(self) -> int:
        return self.seconds * 1000


def iter_all_symbol_interval() -> Generator[Tuple[SymbolPairsEnum, IntervalKLineEnum], None, None]:
    """ Itera por todas las convinaciones de `symbols e intervals`."""
    return ((symbol, interval) for symbol in SymbolPairsEnum for interval in IntervalKLineEnum)
