from pydantic import BaseModel
from enum import StrEnum
from typing import Literal
from data_platform_sdk.schema import PriceFilters, TradeFilters, LogsPriceFilters, LogsTradeFilters, LogsOrderFilters


class Mode(StrEnum):
    HISTORICAL = "historical"
    LOGS = "logs"

class HistoricalFilters(BaseModel):
    price_filters: PriceFilters
    trade_filters: TradeFilters


class LogsFilters(BaseModel):
    price_filters: LogsPriceFilters
    trade_filters: LogsTradeFilters
    order_filters: LogsOrderFilters


class Indicators(BaseModel):
    show_mid_price: bool = False
    show_mid_wall: bool = False


class VolumeMode(StrEnum):
    LEVEL = "level"
    NET = "net"


class SidebarState(BaseModel):
    mode: Mode
    logs_uploaded: bool = False
    show_trades: bool = False
    show_orders: bool = False
    indicators: Indicators
    filters: HistoricalFilters | LogsFilters
    volume_mode: VolumeMode
