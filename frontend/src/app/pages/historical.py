import streamlit as st
from app.components import Sidebar, OrderBookChart

st.title("Historical Data")

sidebar = Sidebar(mode="historical")
sidebar_state = sidebar.load()

order_book_chart = OrderBookChart(sidebar_state)
order_book_chart.load()
