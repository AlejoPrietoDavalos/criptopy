""" Utilidades para manejar tiempo en UTC."""
from typing import Optional, SupportsIndex
from datetime import datetime, UTC

__all__ = [
    "get_datetime_now", "get_datetime",
    "timestamp2datetime", "is_datetime_utc",
    "datetime2timestamp", "validate_time_ms"
]


def get_datetime_now() -> datetime:
    """ Retorna el tiempo actual en UTC."""
    return datetime.now(tz=UTC)

def get_timestamp_now(in_ms: bool = True) -> int:
    date_now = get_datetime_now()
    return datetime2timestamp(date_now, in_ms)

def get_datetime(
        year: SupportsIndex,
        month: SupportsIndex,
        day: SupportsIndex,
        hour: SupportsIndex = 0,
        minute: SupportsIndex = 0,
        second: SupportsIndex = 0,
        microsecond: SupportsIndex = 0,
    ) -> datetime:
    return datetime(year, month, day, hour, minute, second, microsecond, tzinfo=UTC)

def timestamp2datetime(t: int, is_ms: bool = True) -> datetime:
    """ Recibe un timestamp en `ms`, retorna el datetime en UTC."""
    if is_ms:
        t /= 1000
    return datetime.fromtimestamp(t, tz=UTC)

def datetime2timestamp(date: datetime, in_ms: bool = True) -> int:
    """ Nota: Se queda con 3 decimales después de la comma del segundo, después redondea."""
    if not is_datetime_utc(date):
        raise ValueError("El datetime debe estar en UTC.")
    t = date.timestamp()
    if in_ms:   # Se convierte a ms.
        t *= 1000
    return int(t)

def is_datetime_utc(date: datetime) -> bool:
    """ Retorna True si el datetime está en UTC."""
    if date.tzinfo is not None:
        if date.tzinfo.utcoffset(date) == UTC.utcoffset(date):
            return True
    return False

def validate_time_ms(t: int | datetime) -> int:
    """ Retorna el tiempo en timestamp [ms], tz=UTC."""
    if isinstance(t, int):
        return t
    elif isinstance(t, datetime):
        return datetime2timestamp(t, in_ms=True)
    else:
        raise ValueError("Tiempo incorrecto.")
