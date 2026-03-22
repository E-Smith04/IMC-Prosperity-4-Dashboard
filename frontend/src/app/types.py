from pydantic import BaseModel
from data_platform_sdk.schema import PriceFilters, TradeFilters


class Indicators(BaseModel):
    show_mid_price: bool = False
    show_mid_wall: bool = False

class SidebarState(BaseModel):
    round: int
    show_trades: bool = False
    indicators: Indicators
    price_filters: PriceFilters
    trade_filters: TradeFilters
