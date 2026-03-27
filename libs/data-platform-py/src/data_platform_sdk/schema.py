from pydantic import BaseModel
from enum import StrEnum


class Product(StrEnum):
    EMERALDS = "EMERALDS"
    TOMATOES = "TOMATOES"


class Traders(StrEnum):
    pass


class NormaliseOption(StrEnum):
    MID_WALL = "mid_wall"


class FiltersBase(BaseModel):
    round_number: int
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
