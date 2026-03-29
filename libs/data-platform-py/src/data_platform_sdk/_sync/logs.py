from typing import Any

from data_platform_sdk._sync.http import SyncHttpClient
from data_platform_sdk.schema import LogsUpload, LogsPriceFilters, LogsTradeFilters, LogsOrderFilters


class SyncLogsClient:
    def __init__(self, http: SyncHttpClient) -> None:
        self.http = http

    def upload(
        self,
        logs: LogsUpload
    ) -> None:
        response = self.http.put(
            "/logs",
            json=logs.model_dump(mode="json", exclude_none=True)
        )
        return response

    def get_prices(
        self,
        filters: LogsPriceFilters,
    ) -> list[dict[str, Any]]:
        response = self.http.get(
            "/logs/prices",
            params=filters.model_dump(mode="json", exclude_none=True)
        )
        return response

    def get_trades(
        self,
        filters: LogsTradeFilters,
    ) -> list[dict[str, Any]]:
        response = self.http.get(
            "/logs/trades",
            params=filters.model_dump(mode="json", exclude_none=True)
        )
        return response

    def get_orders(
        self,
        filters: LogsOrderFilters,
    ) -> list[dict[str, Any]]:
        response = self.http.get(
            "/logs/orders",
            params=filters.model_dump(mode="json", exclude_none=True)
        )
        return response
