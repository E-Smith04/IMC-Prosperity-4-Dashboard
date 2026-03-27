import streamlit as st
import pandas as pd
from data_platform_sdk.client import SyncDataPlatformClient
from data_platform_sdk.schema import TradeFilters


class TradesService:
    def __init__(self, client: SyncDataPlatformClient):
        self.client = client

    @st.cache_data
    def get(_self, filters: TradeFilters) -> pd.DataFrame:
        response = _self.client.trades.get(filters=filters)
        return pd.DataFrame(response)
