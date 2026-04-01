import streamlit as st
import plotly.graph_objects as go
from app.services import LogsService
from app.types import SidebarState


class PositionChart:
    def __init__(self, sidebar_state: SidebarState):
        self.filters = sidebar_state.filters

        self.logs_service: LogsService = st.session_state.logs_service
        self.prices = self.logs_service.get_prices(self.filters.price_filters)

        self.fig = self.create_fig()

    def create_fig(self):
        fig = go.Figure()

        self.add_position(fig)

        fig.update_layout(
            title="Position Chart",
            xaxis_title="Timestamp",
            yaxis_title="Position",
            legend_title="Markers",
            hovermode="x unified",
            hoverdistance=1,
            showlegend=True
        )

        return fig

    def add_position(self, fig: go.Figure):
        df = self.prices

        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["position"],
                mode="lines",
                name="Pos",
                line={
                    "color": "blue",
                    "dash": "solid"
                },
                hovertemplate="<br>".join([
                    "<b>Pos:</b> %{y}",
                    "<extra></extra>"
                ])
            )
        )