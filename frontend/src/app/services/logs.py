import streamlit as st
import pandas as pd
from typing import Any
from data_platform_sdk.client import SyncDataPlatformClient
from data_platform_sdk.schema import LogsUpload, LogsPriceFilters, LogsTradeFilters, LogsOrderFilters


class LogsService:
    def __init__(self, client: SyncDataPlatformClient):
        self.client = client

    def upload_logs(self, raw_logs: dict[str, Any]) -> None:
        logs = LogsUpload.model_validate(raw_logs)
        self.client.logs.upload(logs)

    @st.cache_data
    def get_prices(_self, filters: LogsPriceFilters) -> pd.DataFrame:
        response = _self.client.logs.get_prices(filters=filters)
        return pd.DataFrame(response)

    @st.cache_data
    def get_trades(_self, filters: LogsTradeFilters) -> pd.DataFrame:
        response = _self.client.logs.get_trades(filters=filters)
        return pd.DataFrame(response)

    @st.cache_data
    def get_orders(_self, filters: LogsOrderFilters) -> pd.DataFrame:
        response = _self.client.logs.get_orders(filters=filters)
        return pd.DataFrame(response)
