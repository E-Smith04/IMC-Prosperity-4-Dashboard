from pydantic import BaseModel
from enum import Enum


class Product(str, Enum):
    EMERALDS = "EMERALDS"
    TOMATOES = "TOMATOES"


class FiltersBase(BaseModel):
    day: int | None = None
    timestamp_min: int | None = None
    timestamp_max: int | None = None