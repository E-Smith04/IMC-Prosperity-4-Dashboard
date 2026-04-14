from __future__ import annotations

import json
from pydantic import BaseModel, field_validator
from enum import StrEnum
from typing import Any


class Product(StrEnum):
    EMERALDS = "EMERALDS"
    TOMATOES = "TOMATOES"
    ASH_COATED_OSMIUM = "ASH_COATED_OSMIUM"
    INTARIAN_PEPPER_ROOT = "INTARIAN_PEPPER_ROOT"


class Traders(StrEnum):
    SUBMISSION = "SUBMISSION"


class NormaliseOption(StrEnum):
    MID_WALL = "mid_wall"


class Filters(BaseModel):
    timestamp_min: int | None = None
    timestamp_max: int | None = None


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


class Log(BaseModel):
    sandboxLog: str
    lambdaLog: LambdaLog
    timestamp: int

    @field_validator("lambdaLog", mode="before")
    def parse_lambda(cls, v):
        return LambdaLog.from_raw(v)


class LambdaLog(BaseModel):
    state: State
    orders: list[Order]
    conversions: int
    traderData: str
    logs: str

    @classmethod
    def from_raw(cls, raw: str):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            raise ValueError("Invalid or truncated lambdaLog JSON")

        state_raw = data[0]

        listings = [
            Listing(symbol=l[0], product=l[1], denomination=l[2])
            for l in state_raw[2]
        ]

        order_depths = {}
        for symbol, depth in state_raw[3].items():
            order_depths[symbol] = OrderDepth(
                buy_orders={k: v for k, v in depth[0].items()},
                sell_orders={k: v for k, v in depth[1].items()},
            )

        def parse_trades(trades):
            return [
                Trade(
                    symbol=t[0],
                    price=t[1],
                    quantity=t[2],
                    buyer=t[3],
                    seller=t[4],
                    timestamp=t[5],
                )
                for t in trades
            ]

        obs_raw = state_raw[7]

        conversion_obs = {
            product: ConversionObservation(
                bidPrice=v[0],
                askPrice=v[1],
                transportFees=v[2],
                exportTariff=v[3],
                importTariff=v[4],
                sugarPrice=v[5],
                sunlightIndex=v[6],
            )
            for product, v in obs_raw[1].items()
        }

        observations = Observations(
            plainValueObservations=obs_raw[0],
            conversionObservations=conversion_obs,
        )

        state = State(
            timestamp=state_raw[0],
            traderData=state_raw[1],
            listings=listings,
            order_depths=order_depths,
            own_trades=parse_trades(state_raw[4]),
            market_trades=parse_trades(state_raw[5]),
            position=state_raw[6],
            observations=observations,
        )

        orders = [
            Order(symbol=o[0], price=o[1], quantity=o[2])
            for o in data[1]
        ]

        return cls(
            state=state,
            orders=orders,
            conversions=data[2],
            traderData=data[3],
            logs=data[4],
        )


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
    buyer: str
    seller: str
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
    buyer: str
    seller: str
    symbol: str
    currency: str
    price: float
    quantity: int
