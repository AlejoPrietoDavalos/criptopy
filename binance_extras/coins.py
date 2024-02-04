""" Este módulo contiene todas las monedas de interés."""
from enum import Enum

__all__ = [
    "USDT", "BTC", "ETH", "BNB", "AXS",
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "AXSUSDT",
    "SymbolEnum", "SymbolPairsEnum",
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
