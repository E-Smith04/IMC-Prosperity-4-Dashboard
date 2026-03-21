import streamlit as st
from app.types import SidebarState
from data_platform_sdk.schema import PriceFilters, TradeFilters, Product


class Sidebar:
    def __init__(self) -> None:
        pass

    def load(self) -> SidebarState:
        with st.sidebar:
            st.subheader('Options', divider='grey')

            selected_round = st.selectbox(
                'Round',
                (0),
                placeholder='Select Round'
            )

            day, product, timestamp_min, timestamp_max = self.load_shared_filters()
            show_trades, quantity_min, quantity_max = self.load_trade_filters()

            price_filters = PriceFilters(
                day=day,
                product=product,
                timestamp_min=timestamp_min,
                timestamp_max=timestamp_max,
            )

            trade_filters = TradeFilters(
                day=day,
                symbol=product,
                timestamp_min=timestamp_min,
                timestamp_max=timestamp_max,
                quantity_min=quantity_min,
                quantity_max=quantity_max
            )

            return SidebarState(
                round=selected_round,
                show_trades=show_trades,
                price_filters=price_filters,
                trade_filters=trade_filters
            )

    def load_shared_filters(self):
        st.subheader('Filters', divider='grey')

        day = st.selectbox(
            'Day',
            (-2, -1),
            index=None,
            placeholder='Select Day'
        )

        product_enum = st.selectbox(
            'Product',
            list(Product),
            format_func=lambda prod: prod.name,
            index=None,
            placeholder='Select Product'
        )
        product = product_enum.value if product_enum else None


        timestamp_slider = st.slider('Timeframe', 0, 999900, (0, 10000), step=1000)
        timestamp_min = timestamp_slider[0]
        timestamp_max = timestamp_slider[1]

        return day, product, timestamp_min, timestamp_max

    def load_trade_filters(self):
        st.subheader('Trade Filters', divider='grey')

        show_trades = st.checkbox('Show Trades')
        quantity_min = st.number_input('Min Quantity', min_value=0, step=1)
        quantity_max = st.number_input('Max Quantity', min_value=0, step=1, value=20)

        return show_trades, quantity_min, quantity_max
