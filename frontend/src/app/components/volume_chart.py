import streamlit as st
import plotly.graph_objects as go
from app.services import HistoricalService, LogsService
from app.types import SidebarState, VolumeMode, Mode


class VolumeChart:
    def __init__(self, sidebar_state: SidebarState):
        self.filters = sidebar_state.filters
        self.volume_mode = sidebar_state.volume_mode

        self.historical_service: HistoricalService = st.session_state.historical_service
        self.logs_service: LogsService = st.session_state.logs_service

        if sidebar_state.mode == Mode.HISTORICAL:
            self.prices = self.historical_service.get_prices(self.filters.price_filters)
        else:
            self.prices = self.logs_service.get_prices(self.filters.price_filters)

        self.fig = self.create_fig()

    def create_fig(self):
        fig = go.Figure()

        if self.volume_mode == VolumeMode.LEVEL:
            self.add_bid_volume_1(fig)
            self.add_bid_volume_2(fig)
            self.add_bid_volume_3(fig)
            self.add_ask_volume_1(fig)
            self.add_ask_volume_2(fig)
            self.add_ask_volume_3(fig)
        elif self.volume_mode == VolumeMode.NET:
            self.add_volume_net(fig)


        fig.update_layout(
            title="Volume Chart",
            xaxis_title="Timestamp",
            yaxis_title="Volume",
            legend_title="Markers",
            hovermode="x unified",
            hoverdistance=1,
            showlegend=True
        )

        return fig

    def add_bid_volume_1(self, fig: go.Figure):
        df = self.prices

        fig.add_trace(
            go.Bar(
                x=df["timestamp"],
                y=df["bid_volume_1"],
                name="Bid 1",
                marker={
                    "color": "blue"
                },
                hovertemplate="<br>".join([
                    "<b>Bid Vol 1:</b> %{y}",
                    "<extra></extra>"
                ])
            )
        )

    def add_bid_volume_2(self, fig: go.Figure):
        df = self.prices

        fig.add_trace(
            go.Bar(
                x=df["timestamp"],
                y=df["bid_volume_2"],
                name="Bid 2",
                marker={
                    "color": "blue"
                },
                hovertemplate="<br>".join([
                    "<b>Bid Vol 2:</b> %{y}",
                    "<extra></extra>"
                ])
            )
        )

    def add_bid_volume_3(self, fig: go.Figure):
        df = self.prices

        fig.add_trace(
            go.Bar(
                x=df["timestamp"],
                y=df["bid_volume_3"],
                name="Bid 3",
                marker={
                    "color": "blue"
                },
                hovertemplate="<br>".join([
                    "<b>Bid Vol 3:</b> %{y}",
                    "<extra></extra>"
                ])
            )
        )

    def add_ask_volume_1(self, fig: go.Figure):
        df = self.prices

        fig.add_trace(
            go.Bar(
                x=df["timestamp"],
                y=df["ask_volume_1"],
                name="Ask 1",
                marker={
                    "color": "red"
                },
                hovertemplate="<br>".join([
                    "<b>Ask Vol 1:</b> %{y}",
                    "<extra></extra>"
                ])
            )
        )

    def add_ask_volume_2(self, fig: go.Figure):
        df = self.prices

        fig.add_trace(
            go.Bar(
                x=df["timestamp"],
                y=df["ask_volume_2"],
                name="Ask 2",
                marker={
                    "color": "red"
                },
                hovertemplate="<br>".join([
                    "<b>Ask Vol 2:</b> %{y}",
                    "<extra></extra>"
                ])
            )
        )

    def add_ask_volume_3(self, fig: go.Figure):
        df = self.prices

        fig.add_trace(
            go.Bar(
                x=df["timestamp"],
                y=df["ask_volume_3"],
                name="Ask 3",
                marker={
                    "color": "red"
                },
                hovertemplate="<br>".join([
                    "<b>Ask Vol 3:</b> %{y}",
                    "<extra></extra>"
                ])
            )
        )


    def add_volume_net(self, fig: go.Figure):
        df = self.prices

        colors = ["blue" if v > 0 else "red" for v in df["volume_net"]]

        fig.add_trace(
            go.Bar(
                x=df["timestamp"],
                y=df["volume_net"].abs(),
                name="Net Volume",
                marker={
                    "color": colors
                },
                hovertemplate="<br>".join([
                    "<b>Net Volume:</b> %{y}",
                    "<extra></extra>"
                ])
            )
        )
