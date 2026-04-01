import streamlit as st
from plotly.subplots import make_subplots
from app.components import Sidebar, OrderBookChart, PnlChart, PositionChart, VolumeChart
from app.types import Mode

st.title("Logs")

sidebar = Sidebar(Mode.LOGS)
sidebar_state = sidebar.load()

if sidebar_state.logs_uploaded:
    order_book_chart = OrderBookChart(sidebar_state)
    volume_chart = VolumeChart(sidebar_state)
    position_chart = PositionChart(sidebar_state)
    pnl_chart = PnlChart(sidebar_state)

    fig = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.5, 0.2, 0.15, 0.15],
        column_titles=["Order Book"]
    )

    for trace in order_book_chart.fig.data:
        fig.add_trace(trace, row=1, col=1)

    for trace in volume_chart.fig.data:
        fig.add_trace(trace, row=2, col=1)

    for trace in position_chart.fig.data:
        fig.add_trace(trace, row=3, col=1)

    for trace in pnl_chart.fig.data:
        fig.add_trace(trace, row=4, col=1)

    fig.update_traces(xaxis='x1')
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_yaxes(title_text="Position", row=3, col=1)
    fig.update_yaxes(title_text="PnL", row=4, col=1)

    fig.update_layout(
        hoversubplots="axis",
        hovermode="x unified",
        showlegend=True
    )

    st.plotly_chart(fig, height=1200)
