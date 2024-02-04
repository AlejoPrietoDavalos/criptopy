from typing import Dict
from enum import Enum

__all__ = ["IntervalEnum"]

class IntervalEnum(Enum):
    interval_1m = "1m"
    interval_5m = "5m"
    interval_1h = "1h"
    interval_1d = "1d"

    @property
    def unit2minutes(self) -> Dict[str, int]:
        return {'m': 1, 'h': 60, 'd': 1440}

    @property
    def minutes(self) -> int:
        value, unit = int(self.value[:-1]), self.value[-1]
        return value * self.unit2minutes[unit]
    
    @property
    def seconds(self) -> int:
        return self.minutes * 60
    
    @property
    def microseconds(self) -> int:
        return self.seconds * 1000
