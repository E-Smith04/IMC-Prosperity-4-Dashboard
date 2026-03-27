from data_platform.app.schemas.shared import FiltersBase, Product
from enum import StrEnum


class Traders(StrEnum):
    pass


class TradeFilters(FiltersBase):
    symbol: Product | None = None
    quantity_min: int | None = None
    quantity_max: int | None = None
    buyers: list[Traders] | None = None
    sellers: list[Traders] | None = None