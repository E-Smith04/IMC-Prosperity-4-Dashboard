from __future__ import annotations

from pydantic import BaseModel, computed_field
from typing import Any
from data_platform.app.schemas.shared import Filters, Product, Traders


class LogsPriceFilters(Filters):
    product: Product | None = None


class LogsTradeFilters(Filters):
    symbol: Product | None = None
    quantity_min: int | None = None
    quantity_max: int | None = None
    buyers: list[Traders] | None = None
    sellers: list[Traders] | None = None


class LogsOrderFilters(Filters):
    symbol: Product | None = None


class LogsUpload(BaseModel):
    submissionId: str
    activitiesLog: str
    logs: list[Log]
    tradeHistory: list[TradeHistory]

    @computed_field
    def flattened_orders(self) -> list[dict[str, Any]]:
        return [
            {"timestamp": log.timestamp} | order.model_dump()
            for log in self.logs
            for order in log.lambdaLog.orders
        ]


class Log(BaseModel):
    sandboxLog: str
    lambdaLog: LambdaLog
    timestamp: int


class LambdaLog(BaseModel):
    state: State
    orders: list[Order]
    conversions: int
    traderData: str
    logs: str


class Listing(BaseModel):
    symbol: str
    product: str
    denomination: int


class OrderDepth(BaseModel):
    buy_orders: dict[int, int]
    sell_orders: dict[int, int]


class Trade(BaseModel):
    symbol: str
    price: float
    quantity: int
    buyer: str | None = None
    seller: str | None = None
    timestamp: int


class ConversionObservation(BaseModel):
    bidPrice: float
    askPrice: float
    transportFees: float
    exportTariff: float
    importTariff: float
    sugarPrice: float
    sunlightIndex: float


class Observations(BaseModel):
    plainValueObservations: dict[str, Any]
    conversionObservations: dict[str, ConversionObservation]


class State(BaseModel):
    timestamp: int
    traderData: str
    listings: list[Listing]
    order_depths: dict[str, OrderDepth]
    own_trades: list[Trade]
    market_trades: list[Trade]
    position: dict[str, int]
    observations: Observations


class Order(BaseModel):
    symbol: str
    price: int
    quantity: int


class TradeHistory(BaseModel):
    timestamp: int
    buyer: str | None = None
    seller: str | None = None
    symbol: str
    currency: str
    price: float
    quantity: int
