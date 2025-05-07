from typing import Tuple, NewType
import os

from dotenv import load_dotenv
from binance.um_futures import UMFutures

load_dotenv()

type T_BinanceApiKey = str
type T_BinanceSecretKey = str

def get_credentials() -> Tuple[T_BinanceApiKey, T_BinanceSecretKey]:
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
    return BINANCE_API_KEY, BINANCE_SECRET_KEY

def get_um_futures_client(**kwargs) -> UMFutures:
    BINANCE_API_KEY, BINANCE_SECRET_KEY = get_credentials()
    client = UMFutures(key=BINANCE_API_KEY, secret=BINANCE_SECRET_KEY, **kwargs)
    return client