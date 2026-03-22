from pydantic import BaseModel
from enum import Enum


class Product(str, Enum):
    EMERALDS = "EMERALDS"
    TOMATOES = "TOMATOES"


class NormaliseOption(str, Enum):
    MID_WALL = "mid_wall"


class FiltersBase(BaseModel):
    day: int | None = None
    timestamp_min: int | None = None
    timestamp_max: int | None = None
    normalise_option: NormaliseOption | None = None
