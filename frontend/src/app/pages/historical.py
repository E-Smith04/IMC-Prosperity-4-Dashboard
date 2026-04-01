import streamlit as st
from plotly.subplots import make_subplots
from app.components import Sidebar, OrderBookChart, VolumeChart
from app.types import Mode

st.title("Historical Data")

sidebar = Sidebar(mode=Mode.HISTORICAL)
sidebar_state = sidebar.load()

order_book_chart = OrderBookChart(sidebar_state)
volume_chart = VolumeChart(sidebar_state)

fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3],
        column_titles=["Order Book"]
    )

for trace in order_book_chart.fig.data:
    fig.add_trace(trace, row=1, col=1)

for trace in volume_chart.fig.data:
    fig.add_trace(trace, row=2, col=1)

fig.update_traces(xaxis='x1')
fig.update_yaxes(title_text="Price", row=1, col=1)
fig.update_yaxes(title_text="Volume", row=2, col=1)

fig.update_layout(
    hoversubplots="axis",
    hovermode="x unified",
    showlegend=True
)

st.plotly_chart(fig, height=800)
