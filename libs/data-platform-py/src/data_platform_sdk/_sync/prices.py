from typing import Any

from data_platform_sdk._sync.http import SyncHttpClient
from data_platform_sdk.schema import PriceFilters


class SyncPricesClient:
    def __init__(self, http: SyncHttpClient) -> None:
        self.http = http

    def read_prices(
        self,
        round_num: int,
        filters: PriceFilters,
    ) -> list[dict[str, Any]]:
        response = self.http.get(
            f"/prices/{round_num}",
            params=filters.model_dump(exclude_none=True)
        )
        return response