"""
- `KLine:` Velas japonesas.
- Objeto contenedor de datos para validar y serializar en tiempo real.
- También se usa para serializar los precios y guardar en MongoDB.

- `body:` Distancia entre el precio de apertura y cierre.
- `shadow:` Distancia entre el precio mas alto y bajo alcanzado en la vela.
- `bullish:` Si el precio de cierre es `mayor` al de apertura `(sube)`.
- `bearish:` Si el precio de cierre es `menor` al de apertura `(baja)`.
"""
from __future__ import annotations
from typing import Self
from datetime import datetime, timedelta
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator
from bson.decimal128 import Decimal128

from cripto_trading.decimals import validate_decimal, serialize_decimal
from cripto_trading.time import timestamp2datetime_utc

__all__ = ["KLine"]


class KLine(BaseModel):
    """ Modelo de datos para las velas del mercado cripto.

    #### Propertys
    - `time_open:   (int)`      Tiempo de apertura de la vela. (UTC)
    - `price_open:  (Decimal)`  Precio de apertura.
    - `price_high:  (Decimal)`  Precio más alto en el intervalo.
    - `price_low:   (Decimal)`  Precio más bajo en el intervalo.
    - `price_close: (Decimal)`  Precio de cierre.
    - `time_close:  (int)`      Tiempo de cierre de la vela. (UTC)
    
    #### Propertys Variables
    - `time_delta:  (int)`      time_close - time_open.
    - `date_delta:  (timedelta)`date_close - date_open.
    - `date_open:   (datetime)` datetime.fromtimestamp(time_open)
    - `date_close:  (datetime)` datetime.fromtimestamp(time_close)
    - `price_body_delta:    (Decimal)` price_close - price_open
    - `price_shadow_delta:  (Decimal)` price_high - price_low
    - `is_bullish:  (bool)` price_close > price_open
    - `is_bearish:  (bool)` price_close < price_open
    
    """
    time_open: int = Field(frozen=True, gt=0)   # (UTC) Tiempo de apertura de la vela.
    price_open: Decimal = Field(frozen=True)    # Precio de apertura.
    price_high: Decimal = Field(frozen=True)    # Precio más alto en el intervalo.
    price_low: Decimal = Field(frozen=True)     # Precio más bajo en el intervalo.
    price_close: Decimal = Field(frozen=True)   # Precio de cierre.
    time_close: int = Field(frozen=True, gt=0)  # (UTC) Tiempo de cierre de la vela.

    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)

    @property
    def time_delta(self) -> int:
        """ `time_close - time_open` [ms]"""
        return self.time_close - self.time_open
    
    @property
    def date_delta(self) -> timedelta:
        """ Retorna la diferencia de tiempo de la vela en `ms`."""
        return self.date_close - self.date_open

    @property
    def date_open(self) -> datetime:
        return timestamp2datetime_utc(self.time_open)
    
    @property
    def date_close(self) -> datetime:
        return timestamp2datetime_utc(self.time_close)

    @property
    def price_body_delta(self) -> Decimal:
        """ `price_close - price_open`"""
        return self.price_close - self.price_open
    
    @property
    def price_shadow_delta(self) -> Decimal:
        """ `price_high - price_low`"""
        return self.price_high - self.price_low
    
    @property
    def is_bullish(self) -> bool:
        """ El precio sube?"""
        return self.price_close > self.price_open
    
    @property
    def is_bearish(self) -> bool:
        """ El precio baja?"""
        return self.price_close < self.price_open

    @classmethod
    def from_binance(cls, kline_binance: list) -> Self:
        """ Ver `UMFutures.mark_price_klines()` para documentación.
        - https://binance-docs.github.io/apidocs/futures/en/#index-price-kline-candlestick-data
        """
        time_open, price_open, price_high, price_low, price_close, _, time_close, _, _, _, _, _ = kline_binance
        return cls(
            time_open = int(time_open),
            price_open = Decimal(price_open),
            price_high = Decimal(price_high),
            price_low = Decimal(price_low),
            price_close = Decimal(price_close),
            time_close = int(time_close)
        )

    @field_validator("price_open", "price_high", "price_low", "price_close", mode="plain")
    def validate_prices(cls, price: str | Decimal | Decimal128) -> Decimal:
        return validate_decimal(price)
    
    @field_serializer("price_open", "price_high", "price_low", "price_close", when_used="always")
    def serialice_prices(price: Decimal) -> Decimal128:
        return serialize_decimal(price)
