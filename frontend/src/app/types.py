from pydantic import BaseModel
from data_platform_sdk.schema import PriceFilters, TradeFilters


class SidebarState(BaseModel):
    round: int
    show_trades: bool = False
    price_filters: PriceFilters
    trade_filters: TradeFilters
