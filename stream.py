from typing import Literal

import json

import matplotlib.pyplot as plt
from pydantic import BaseModel, Field, ConfigDict

from binance.websocket.binance_socket_manager import BinanceSocketManager
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
from general_utils.coins import SymbolPairsEnum

import logging
#from binance.lib.utils import config_logging
#config_logging(logging, logging.NOTSET)


class Message(BaseModel):
    e: Literal["markPriceUpdate"]
    E: int  # Tiempo actual en timestamp.
    s: SymbolPairsEnum
    p: float
    P: float
    i: float
    r: float
    T: int

    model_config = ConfigDict(use_enum_values=True)

    @property
    def timestamp(self) -> int:
        return self.E
    
    @property
    def price(self) -> float:
        return self.i

    def printear(self) -> None:
        print(f"MarkPrice={self.p} | IndexPrice={self.P} | EstimatedSettlerPrice={self.i}")

i = 0
i_last_update = 0
t, p = [], []

def message_handler(bsm: BinanceSocketManager, msg_str: str):
    """ - `message_str`: Retorna primero un string con: `result` y `id`."""
    global t, p, i
    try:
        msg_dict = json.loads(msg_str)
        msg = Message(**msg_dict)
        t.append(i)
        p.append(msg.price)
        i += 1
        #print(msg.model_dump())
        #print("-"*40)
        print(t)
        print(p)
        print("-"*20)
    except Exception as e:
        print(e)








if __name__ == '__main__':
    my_client = UMFuturesWebsocketClient(on_message=message_handler)
    my_client.mark_price(
        symbol = SymbolPairsEnum.AXSUSDT.value,
        id = 13,
        speed = 1,
    )
    
    while True:
        pass


#logging.debug("closing ws connection")
#my_client.stop()

