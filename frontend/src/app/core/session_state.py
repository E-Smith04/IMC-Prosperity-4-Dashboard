import streamlit as st
from app.services import HistoricalService, LogsService
from app.core.config import settings
from data_platform_sdk import get_sync_client


def init_session_state():
    if "data_platform_client" not in st.session_state:
        st.session_state.data_platform_client = get_sync_client(url=settings.DATA_PLATFORM_BASE_URL)
        st.session_state.historical_service = HistoricalService(st.session_state.data_platform_client)
        st.session_state.logs_service = LogsService(st.session_state.data_platform_client)
    if "logs_submission_id" not in st.session_state:
        st.session_state.logs_submission_id = None