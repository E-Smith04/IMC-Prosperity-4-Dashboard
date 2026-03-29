import streamlit as st
import pandas as pd
from data_platform_sdk.client import SyncDataPlatformClient
from data_platform_sdk.schema import PriceFilters, TradeFilters


class HistoricalService:
    def __init__(self, client: SyncDataPlatformClient):
        self.client = client

    @st.cache_data
    def get_prices(_self, filters: PriceFilters) -> pd.DataFrame:
        response = _self.client.historical.get_prices(filters=filters)
        return pd.DataFrame(response)

    @st.cache_data
    def get_trades(_self, filters: TradeFilters) -> pd.DataFrame:
        response = _self.client.historical.get_trades(filters=filters)
        return pd.DataFrame(response)
