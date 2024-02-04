from decimal import Decimal
from bson.decimal128 import Decimal128

__all__ = ["serialize_decimal", "validate_decimal"]

def serialize_decimal(decimal: Decimal) -> Decimal128:
    if not isinstance(decimal, Decimal):
        raise ValueError("Se espera una instancia de Decimal.")
    return Decimal128(decimal)

def validate_decimal(decimal: str | Decimal | Decimal128) -> Decimal:
    """ TODO: Ver caso `float`. Mete como 80 decimales."""
    if isinstance(decimal, Decimal):
        return decimal
    elif isinstance(decimal, str):
        return Decimal(decimal)
    elif isinstance(decimal, Decimal128):
        return decimal.to_decimal()
    else:
        raise Exception("Precio incorrecto.")