from enum import Enum

__all__ = ["IntervalEnum"]

class IntervalEnum(Enum):
    interval_1m = "1m"
    interval_5m = "5m"
    interval_1h = "1h"
    interval_1d = "1d"