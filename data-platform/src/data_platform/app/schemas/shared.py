from pydantic import BaseModel
from enum import StrEnum


class Product(StrEnum):
    EMERALDS = "EMERALDS"
    TOMATOES = "TOMATOES"


class NormaliseOption(StrEnum):
    MID_WALL = "mid_wall"


class FiltersBase(BaseModel):
    round_number: int
    day: int | None = None
    timestamp_min: int | None = None
    timestamp_max: int | None = None
    normalise_option: NormaliseOption | None = None
