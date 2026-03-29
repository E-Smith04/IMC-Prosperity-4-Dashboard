from fastapi import APIRouter, Depends, Query
from typing import Annotated, Any
from data_platform.app.services import LogsService
from data_platform.app.schemas.logs import LogsUpload, LogsPriceFilters, LogsTradeFilters, LogsOrderFilters

router = APIRouter(
    prefix="/logs",
    tags=["logs"]
)


@router.put("")
def upload_logs(
    logs: LogsUpload,
    service: Annotated[LogsService, Depends()]
) -> None:
    return service.upload(logs)


@router.get("/prices")
def get_prices(
    price_filters: Annotated[LogsPriceFilters, Query()],
    service: Annotated[LogsService, Depends()]
) -> list[dict[str, Any]]:
    return service.get_prices(price_filters)


@router.get("/trades")
def get_trades(
    trade_filters: Annotated[LogsTradeFilters, Query()],
    service: Annotated[LogsService, Depends()]
) -> list[dict[str, Any]]:
    return service.get_trades(trade_filters)


@router.get("/orders")
def get_orders(
    order_filters: Annotated[LogsOrderFilters, Query()],
    service: Annotated[LogsService, Depends()]
) -> list[dict[str, Any]]:
    return service.get_orders(order_filters)
