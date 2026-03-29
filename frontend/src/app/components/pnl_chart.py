import streamlit as st
import plotly.graph_objects as go
from app.services import LogsService
from app.types import SidebarState


class PnlChart:
    def __init__(self, sidebar_state: SidebarState):
        self.filters = sidebar_state.filters

        self.logs_service: LogsService = st.session_state.logs_service
        self.prices = self.logs_service.get_prices(self.filters.price_filters)

    def load(self):
        fig = self.create_fig()
        st.plotly_chart(fig, on_select="ignore", selection_mode="points")

    def create_fig(self):
        fig = go.Figure()

        self.add_pnl(fig)

        fig.update_layout(
            title="PnL Chart",
            xaxis_title="Timestamp",
            yaxis_title="PnL",
            legend_title="Markers",
            hovermode="x unified",
            hoverdistance=1,
            showlegend=True
        )

        return fig

    def add_pnl(self, fig: go.Figure):
        df = self.prices

        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["profit_and_loss"],
                mode="lines",
                name="PnL",
                line={
                    "color": "blue",
                    "dash": "solid"
                },
                hovertemplate="<br>".join([
                    "<b>PnL:</b> %{y}",
                    "<extra></extra>"
                ])
            )
        )