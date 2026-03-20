import httpx
import orjson
from typing import Any


class SyncHttpClient:
    def __init__(self, client: httpx.Client) -> None:
        self.client = client

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None
    ) -> Any:
        response = self.client.get(path, params=params)
        response.raise_for_status()
        return _decode_json(response)


def _decode_json(response: httpx.Response) -> Any:
    body = response.read()
    return orjson.loads(body) if body else None
