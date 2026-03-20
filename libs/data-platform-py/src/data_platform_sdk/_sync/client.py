from __future__ import annotations

import httpx

from data_platform_sdk._sync.http import SyncHttpClient
from data_platform_sdk._sync.prices import SyncPricesClient
from data_platform_sdk._sync.trades import SyncTradesClient


def get_sync_client(
    *,
    url: str
) -> SyncDataPlatformClient:
    """Get a synchronous DataPlatformClient instance"""
    client = httpx.Client(base_url=url)
    return SyncDataPlatformClient(client)


class SyncDataPlatformClient:
    def __init__(self, client: httpx.Client) -> None:
        self.http = SyncHttpClient(client)
        self.prices: SyncPricesClient = SyncPricesClient(self.http)
        self.trades: SyncTradesClient = SyncTradesClient(self.http)

    def __enter__(self) -> SyncDataPlatformClient:
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb
    ) -> None:
        self.close()

    def close(self) -> None:
        if hasattr(self, "client"):
            self.client.close()