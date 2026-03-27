from fastapi import APIRouter, Depends, Query
from typing import Annotated, Any
from data_platform.app.services import PricesService
from data_platform.app.schemas.prices import PriceFilters

router = APIRouter(
    prefix="/prices",
    tags=["prices"]
)


@router.get("")
def get_prices(
    price_filters: Annotated[PriceFilters, Query()],
    service: Annotated[PricesService, Depends()]
) -> list[dict[str, Any]]:
    return service.read_prices(price_filters)
