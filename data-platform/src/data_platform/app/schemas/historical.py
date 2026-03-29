from enum import StrEnum

from data_platform.app.schemas.shared import Product, Filters, Traders


class NormaliseOption(StrEnum):
    MID_WALL = "mid_wall"


class PriceFilters(Filters):
    round_number: int
    day: int
    product: Product | None = None
    normalise_option: NormaliseOption | None = None


class TradeFilters(Filters):
    round_number: int
    day: int
    symbol: Product | None = None
    quantity_min: int | None = None
    quantity_max: int | None = None
    buyers: list[Traders] | None = None
    sellers: list[Traders] | None = None
    normalise_option: NormaliseOption | None = None
