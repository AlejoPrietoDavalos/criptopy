from typing import Tuple, NewType
from dotenv import load_dotenv
import os
load_dotenv()

from binance.um_futures import UMFutures


BinanceApiKey = NewType("ApiKey", str)
BinanceSecretKey = NewType("SecretKey", str)

def get_credentials() -> Tuple[BinanceApiKey, BinanceSecretKey]:
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
    return BINANCE_API_KEY, BINANCE_SECRET_KEY

def get_um_futures_client(**kwargs) -> UMFutures:
    BINANCE_API_KEY, BINANCE_SECRET_KEY = get_credentials()
    client = UMFutures(key=BINANCE_API_KEY, secret=BINANCE_SECRET_KEY, **kwargs)
    return client