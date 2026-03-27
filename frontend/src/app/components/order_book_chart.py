import streamlit as st
import plotly.graph_objects as go
from app.services import PricesService, TradesService
from app.types import SidebarState


class OrderBookChart:
    def __init__(self, sidebar_state: SidebarState):
        self.round_number = sidebar_state.round_number
        self.show_trades = sidebar_state.show_trades
        self.indicators = sidebar_state.indicators
        self.prices_filter = sidebar_state.price_filters
        self.trades_filter = sidebar_state.trade_filters

        self.prices_service: PricesService = st.session_state.prices_service
        self.trades_service: TradesService = st.session_state.trades_service

    def load(self):
        fig = self.create_fig()
        event = st.plotly_chart(fig, on_select="rerun", selection_mode="points")
        points = event.selection.points
        return points

    def create_fig(self):
        fig = go.Figure()

        self.add_bid_1(fig)
        self.add_bid_2(fig)
        self.add_bid_3(fig)
        self.add_ask_1(fig)
        self.add_ask_2(fig)
        self.add_ask_3(fig)

        if self.show_trades:
            self.add_trades(fig)
        if self.indicators.show_mid_price:
            self.add_mid_price(fig)
        if self.indicators.show_mid_wall:
            self.add_mid_wall(fig)

        fig.update_layout(
            title="Order Book Chart",
            xaxis_title="Timestamp",
            yaxis_title="Price",
            legend_title="Markers",
            hovermode="x unified",
            hoverdistance=1
        )

        return fig

    def add_bid_1(self, fig: go.Figure):
        df = self.prices_service.get(self.prices_filter)

        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["bid_price_1"],
                customdata=df["bid_volume_1"],
                mode="markers",
                marker={
                    "color": "blue"
                },
                name=f"Bid 1",
                hovertemplate="<br>".join([
                    "<b>Bid 1</b>",
                    "Price: %{y}",
                    "Volume: %{customdata}",
                    "<extra></extra>"
                ])
            )
        )

    def add_bid_2(self, fig: go.Figure):
        df = self.prices_service.get(self.prices_filter)

        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["bid_price_2"],
                customdata=df["bid_volume_2"],
                mode="markers",
                marker={
                    "color": "blue"
                },
                name="Bid 2",
                hovertemplate="<br>".join([
                    "<b>Bid 2</b>",
                    "Price: %{y}",
                    "Volume: %{customdata}",
                    "<extra></extra>"
                ])
            )
        )

    def add_bid_3(self, fig: go.Figure):
        df = self.prices_service.get(self.prices_filter)

        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["bid_price_3"],
                customdata=df["bid_volume_3"],
                mode="markers",
                marker={
                    "color": "blue"
                },
                name="Bid 3",
                hovertemplate="<br>".join([
                    "<b>Bid 3</b>",
                    "Price: %{y}",
                    "Volume: %{customdata}",
                    "<extra></extra>"
                ])
            )
        )

    def add_ask_1(self, fig: go.Figure):
        df = self.prices_service.get(self.prices_filter)

        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["ask_price_1"],
                customdata=df["ask_volume_1"],
                mode="markers",
                marker={
                    "color": "red"
                },
                name="Ask 1",
                hovertemplate="<br>".join([
                    "<b>Ask 1</b>",
                    "Price: %{y}",
                    "Volume: %{customdata}",
                    "<extra></extra>"
                ])
            )
        )

    def add_ask_2(self, fig: go.Figure):
        df = self.prices_service.get(self.prices_filter)

        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["ask_price_2"],
                customdata=df["ask_volume_2"],
                mode="markers",
                marker={
                    "color": "red"
                },
                name="Ask 2",
                hovertemplate="<br>".join([
                    "<b>Ask 2</b>",
                    "Price: %{y}",
                    "Volume: %{customdata}",
                    "<extra></extra>"
                ])
            )
        )

    def add_ask_3(self, fig: go.Figure):
        df = self.prices_service.get(self.prices_filter)

        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["ask_price_3"],
                customdata=df["ask_volume_3"],
                mode="markers",
                marker={
                    "color": "red"
                },
                name=f"Ask 3",
                hovertemplate="<br>".join([
                    "<b>Ask 3</b>",
                    "Price: %{y}",
                    "Volume: %{customdata}",
                    "<extra></extra>"
                ])
            )
        )

    def add_trades(self, fig: go.Figure):
        df = self.trades_service.get(self.trades_filter)

        if df.empty:
            return

        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["price"],
                customdata=df[["quantity", "buyer", "seller"]],
                mode="markers",
                marker={
                    "symbol": "x",
                    "size": 10,
                    "color": "yellow"
                },
                name="Trade",
                hovertemplate="<br>".join([
                    "<b>Trade</b>",
                    "Price: %{y}",
                    "Quantity: %{customdata[0]}",
                    "Buyer: %{customdata[1]}",
                    "Seller: %{customdata[2]}",
                    "<extra></extra>"
                ])
            )
        )

    def add_mid_price(self, fig: go.Figure):
        df = self.prices_service.get(self.prices_filter)

        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["mid_price"],
                mode="lines",
                name="Mid Price",
                line={
                    "color": "lightgrey",
                    "dash": "dash"
                },
                hovertemplate="<br>".join([
                    "<b>Mid Price:</b> %{y}",
                    "<extra></extra>"
                ])
            )
        )

    def add_mid_wall(self, fig: go.Figure):
        df = self.prices_service.get(self.prices_filter)

        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["mid_wall"],
                mode="lines",
                name="Mid Wall",
                line={
                    "color": "lightgrey",
                    "dash": "dash"
                },
                hovertemplate="<br>".join([
                    "<b>Mid Wall:</b> %{y}",
                    "<extra></extra>"
                ])
            )
        )
