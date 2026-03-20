from fastapi import APIRouter, Depends, Query
from typing import Annotated, Any
from data_platform.app.services import PricesService
from data_platform.app.schemas.prices import PriceFilters

router = APIRouter(
    prefix="/prices",
    tags=["prices"]
)


@router.get("/{round_num}")
def read_prices(
    round_num: int,
    price_filters: Annotated[PriceFilters, Query()],
    service: Annotated[PricesService, Depends()]
) -> list[dict[str, Any]]:
    return service.read_prices(round_num, price_filters)
