import streamlit as st
import pandas as pd
from data_platform_sdk.client import SyncDataPlatformClient
from data_platform_sdk.schema import PriceFilters


class PricesService:
    def __init__(self, client: SyncDataPlatformClient):
        self.client = client

    @st.cache_data
    def read_prices(_self, round_num: int, filters: PriceFilters) -> pd.DataFrame:
        response = _self.client.prices.read_prices(round_num=round_num, filters=filters)
        return pd.DataFrame(response)
