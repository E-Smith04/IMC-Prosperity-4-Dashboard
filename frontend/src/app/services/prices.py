import streamlit as st
import pandas as pd
from data_platform_sdk.client import SyncDataPlatformClient
from data_platform_sdk.schema import PriceFilters


class PricesService:
    def __init__(self, client: SyncDataPlatformClient):
        self.client = client

    @st.cache_data
    def get(_self, filters: PriceFilters) -> pd.DataFrame:
        response = _self.client.prices.get(filters=filters)
        return pd.DataFrame(response)
