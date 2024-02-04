""" Utilidades para manejar tiempo.
- TODO: Mover a un módulo fuera de `cripto_trading`.
"""
from datetime import datetime, timezone


def timestamp2datetime_utc(timestamp_ms: int) -> datetime:
    """ Recibe un timestamp en `ms`, retorna el datetime en UTC."""
    return datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)


def datetime2timestamp_utc(date: datetime) -> bool:
    if not is_datetime_utc(date):
        raise ValueError("El datetime debe estar en UTC.")
    return int(date.timestamp() * 1000)   # Se convierte a ms.


def is_datetime_utc(date: datetime) -> bool:
    """ Retorna True si el datetime está en UTC."""
    if date.tzinfo is not None:
        if date.tzinfo.utcoffset(date) == timezone.utc.utcoffset(date):
            return True
    return False