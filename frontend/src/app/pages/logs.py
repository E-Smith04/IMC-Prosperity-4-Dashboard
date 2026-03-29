import streamlit as st
from app.components import Sidebar, OrderBookChart, PnlChart

st.title("Logs")

sidebar = Sidebar(mode="logs")
sidebar_state = sidebar.load()

if sidebar_state.logs_uploaded:
    order_book_chart = OrderBookChart(sidebar_state)
    order_book_chart.load()

    pnl_chart = PnlChart(sidebar_state)
    pnl_chart.load()
