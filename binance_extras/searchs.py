""" Búsqueda de KLines en la API de Binance."""
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, field_validator

from binance_extras.intervals import IntervalEnum
from binance_extras.coins import SymbolPairsEnum
from cripto_trading.time import validate_time_ms

__all__ = ["SearchKLines"]


class SearchKLines(BaseModel):
    symbol: SymbolPairsEnum
    interval: IntervalEnum
    limit: int = Field(default=1000, gt=0, le=1000)
    start_time: Optional[int] = Field(default=None, gt=0, alias="startTime")
    end_time: Optional[int] = Field(default=None, gt=0, alias="endTime")

    model_config = ConfigDict(use_enum_values=True)

    def model_dump(self) -> dict:
        return super().model_dump(by_alias=True, exclude_none=True)

    @field_validator("start_time", "end_time", mode="before")
    def validate_time(cls, t: int | datetime) -> int:
        return validate_time_ms(t)
