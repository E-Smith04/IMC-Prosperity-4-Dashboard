import streamlit as st
from app.core.session_state import init_session_state
from app.components import Sidebar, OrderBookChart

st.set_page_config(layout="wide")
st.title("IMC Prosperity 4 Dashboard")

init_session_state()

sidebar = Sidebar()
sidebar_state = sidebar.load()

order_book_chart = OrderBookChart(sidebar_state)
order_book_chart.load()
