""" Abstract Base Classes"""
from abc import ABC

from pydantic import BaseModel, ConfigDict

__all__ = ["BasePricesModel"]

class BasePricesModel(BaseModel, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)