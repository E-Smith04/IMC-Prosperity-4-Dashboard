from typing import Any

from data_platform_sdk._sync.http import SyncHttpClient
from data_platform_sdk.schema import PriceFilters, TradeFilters


class SyncHistoricalClient:
    def __init__(self, http: SyncHttpClient) -> None:
        self.http = http

    def get_prices(
        self,
        filters: PriceFilters,
    ) -> list[dict[str, Any]]:
        response = self.http.get(
            "/historical/prices",
            params=filters.model_dump(mode="json", exclude_none=True)
        )
        return response

    def get_trades(
        self,
        filters: TradeFilters,
    ) -> list[dict[str, Any]]:
        response = self.http.get(
            "/historical/trades",
            params=filters.model_dump(mode="json", exclude_none=True)
        )
        return response
