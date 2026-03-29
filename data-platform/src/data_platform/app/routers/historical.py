from fastapi import APIRouter, Depends, Query
from typing import Annotated, Any
from data_platform.app.services import HistoricalService
from data_platform.app.schemas.historical import PriceFilters, TradeFilters

router = APIRouter(
    prefix="/historical",
    tags=["historical"]
)


@router.get("/prices")
def get_prices(
    price_filters: Annotated[PriceFilters, Query()],
    service: Annotated[HistoricalService, Depends()]
) -> list[dict[str, Any]]:
    return service.get_prices(price_filters)


@router.get("/trades")
def get_trades(
    trade_filters: Annotated[TradeFilters, Query()],
    service: Annotated[HistoricalService, Depends()]
) -> list[dict[str, Any]]:
    return service.get_trades(trade_filters)
