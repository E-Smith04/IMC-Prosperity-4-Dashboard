from __future__ import annotations

import httpx

from data_platform_sdk._sync.http import SyncHttpClient
from data_platform_sdk._sync.historical import SyncHistoricalClient
from data_platform_sdk._sync.logs import SyncLogsClient


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
        self.historical: SyncHistoricalClient = SyncHistoricalClient(self.http)
        self.logs: SyncLogsClient = SyncLogsClient(self.http)

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