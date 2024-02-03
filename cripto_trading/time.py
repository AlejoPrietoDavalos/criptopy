""" Utilidades para manejar tiempo.
- TODO: Mover a un módulo fuera de `cripto_trading`.
"""
from datetime import datetime, timezone

def time_ms_to_datetime_utc(timestamp_ms: int) -> datetime:
    """ Recibe un timestamp en `ms`, retorna el datetime en UTC."""
    return datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)