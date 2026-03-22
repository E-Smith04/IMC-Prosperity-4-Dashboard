from pydantic import BaseModel
from enum import Enum


class Product(str, Enum):
    EMERALDS = "EMERALDS"
    TOMATOES = "TOMATOES"


class Traders(str, Enum):
    pass


class NormaliseOption(str, Enum):
    MID_WALL = "mid_wall"


class FiltersBase(BaseModel):
    day: int | None = None
    timestamp_min: int | None = None
    timestamp_max: int | None = None
    normalise_option: NormaliseOption | None = None


class PriceFilters(FiltersBase):
    product: Product | None = None


class TradeFilters(FiltersBase):
    symbol: Product | None = None
    quantity_min: int | None = None
    quantity_max: int | None = None
    buyers: list[Traders] | None = None
    sellers: list[Traders] | None = None
