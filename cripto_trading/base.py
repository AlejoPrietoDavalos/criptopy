""" Abstract Base Classes"""
from abc import ABC

from pydantic import BaseModel, ConfigDict

class BasePricesModel(BaseModel, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)