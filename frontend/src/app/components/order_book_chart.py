import streamlit as st
import plotly.graph_objects as go
from app.services import HistoricalService, LogsService
from app.types import SidebarState


class OrderBookChart:
    def __init__(self, sidebar_state: SidebarState):
        self.show_trades = sidebar_state.show_trades
        self.show_orders = sidebar_state.show_orders
        self.indicators = sidebar_state.indicators
        self.filters = sidebar_state.filters

        self.historical_service: HistoricalService = st.session_state.historical_service
        self.logs_service: LogsService = st.session_state.logs_service

        if sidebar_state.mode == 'historical':
            self.prices = self.historical_service.get_prices(self.filters.price_filters)
            self.trades = self.historical_service.get_trades(self.filters.trade_filters)
        else:
            self.prices = self.logs_service.get_prices(self.filters.price_filters)
            self.trades = self.logs_service.get_trades(self.filters.trade_filters)
            self.orders = self.logs_service.get_orders(self.filters.order_filters)

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

        if self.show_orders:
            self.add_orders(fig)
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
            hoverdistance=1,
            showlegend=True
        )

        return fig

    def add_bid_1(self, fig: go.Figure):
        df = self.prices

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
        df = self.prices

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
        df = self.prices

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
        df = self.prices

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
        df = self.prices

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
        df = self.prices

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
        df = self.trades

        if df.empty:
            return

        submission_buys = df[df["buyer"] == "SUBMISSION"]
        submission_sells = df[df["seller"] == "SUBMISSION"]
        market_trades = df[(df["buyer"] != "SUBMISSION") & (df["seller"] != "SUBMISSION")]

        fig.add_trace(
            go.Scatter(
                x=submission_buys["timestamp"],
                y=submission_buys["price"],
                customdata=df[["quantity", "buyer", "seller"]],
                mode="markers",
                marker={
                    "symbol": "triangle-up",
                    "size": 15,
                    "color": "lime"
                },
                name="Buy Trade",
                hovertemplate="<br>".join([
                    "<b>Buy Trade</b>",
                    "Price: %{y}",
                    "Quantity: %{customdata[0]}",
                    "Buyer: %{customdata[1]}",
                    "Seller: %{customdata[2]}",
                    "<extra></extra>"
                ])
            )
        )

        fig.add_trace(
            go.Scatter(
                x=submission_sells["timestamp"],
                y=submission_sells["price"],
                customdata=df[["quantity", "buyer", "seller"]],
                mode="markers",
                marker={
                    "symbol": "triangle-down",
                    "size": 15,
                    "color": "orange"
                },
                name="Sell Trade",
                hovertemplate="<br>".join([
                    "<b>Sell Trade</b>",
                    "Price: %{y}",
                    "Quantity: %{customdata[0]}",
                    "Buyer: %{customdata[1]}",
                    "Seller: %{customdata[2]}",
                    "<extra></extra>"
                ])
            )
        )

        fig.add_trace(
            go.Scatter(
                x=market_trades["timestamp"],
                y=market_trades["price"],
                customdata=df[["quantity", "buyer", "seller"]],
                mode="markers",
                marker={
                    "symbol": "x",
                    "size": 10,
                    "color": "yellow"
                },
                name="Market Trade",
                hovertemplate="<br>".join([
                    "<b>Market Trade</b>",
                    "Price: %{y}",
                    "Quantity: %{customdata[0]}",
                    "Buyer: %{customdata[1]}",
                    "Seller: %{customdata[2]}",
                    "<extra></extra>"
                ])
            )
        )

    def add_orders(self, fig: go.Figure):
        df = self.orders

        if df.empty:
            return

        buy_orders = df[df["quantity"] > 0]
        sell_orders = df[df["quantity"] < 0]

        fig.add_trace(
            go.Scatter(
                x=buy_orders["timestamp"],
                y=buy_orders["price"],
                customdata=buy_orders["quantity"],
                mode="markers",
                marker={
                    "symbol": "triangle-up-open",
                    "size": 10,
                    "color": "darkgreen"
                },
                name="Buy Order",
                hovertemplate="<br>".join([
                    "<b>Buy Order</b>",
                    "Price: %{y}",
                    "Quantity: %{customdata}",
                    "<extra></extra>"
                ])
            )
        )

        fig.add_trace(
            go.Scatter(
                x=sell_orders["timestamp"],
                y=sell_orders["price"],
                customdata=sell_orders["quantity"],
                mode="markers",
                marker={
                    "symbol": "triangle-down-open",
                    "size": 10,
                    "color": "maroon"
                },
                name="Sell Order",
                hovertemplate="<br>".join([
                    "<b>Sell Order</b>",
                    "Price: %{y}",
                    "Quantity: %{customdata}",
                    "<extra></extra>"
                ])
            )
        )

    def add_mid_price(self, fig: go.Figure):
        df = self.prices

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
        df = self.prices

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
