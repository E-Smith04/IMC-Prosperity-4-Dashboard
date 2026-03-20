from typing import Any

from data_platform_sdk._sync.http import SyncHttpClient
from data_platform_sdk.schema import TradeFilters


class SyncTradesClient:
    def __init__(self, http: SyncHttpClient) -> None:
        self.http = http

    def read_trades(
        self,
        round_num: int,
        filters: TradeFilters,
    ) -> list[dict[str, Any]]:
        response = self.http.get(
            f"/trades/{round_num}",
            params=filters.model_dump(exclude_none=True)
        )
        return response