from fastapi import APIRouter, Depends, Query
from typing import Annotated, Any
from data_platform.app.services import TradesService
from data_platform.app.schemas.trades import TradeFilters

router = APIRouter(
    prefix="/trades",
    tags=["trades"]
)


@router.get("")
def get_trades(
    trade_filters: Annotated[TradeFilters, Query()],
    service: Annotated[TradesService, Depends()]
) -> list[dict[str, Any]]:
    return service.read_trades(trade_filters)
