import streamlit as st
from app.types import SidebarState, Indicators
from data_platform_sdk.schema import PriceFilters, TradeFilters, Product, NormaliseOption


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
            indicators = self.load_indicators()
            normalise_option = self.load_normalise_option()
            show_trades, quantity_min, quantity_max = self.load_trade_filters()


            price_filters = PriceFilters(
                round_number=selected_round,
                day=day,
                product=product,
                timestamp_min=timestamp_min,
                timestamp_max=timestamp_max,
                normalise_option=normalise_option
            )

            trade_filters = TradeFilters(
                round_number=selected_round,
                day=day,
                symbol=product,
                timestamp_min=timestamp_min,
                timestamp_max=timestamp_max,
                normalise_option=normalise_option,
                quantity_min=quantity_min,
                quantity_max=quantity_max
            )

            return SidebarState(
                round_number=selected_round,
                show_trades=show_trades,
                indicators=indicators,
                price_filters=price_filters,
                trade_filters=trade_filters
            )

    def load_shared_filters(self) -> tuple[int, Product, int, int]:
        st.subheader('Filters', divider='grey')

        day: int = st.selectbox(
            'Day',
            (-2, -1),
            index=None,
            placeholder='Select Day'
        )

        product: Product = st.selectbox(
            'Product',
            list(Product),
            format_func=lambda prod: prod.name,
            index=None,
            placeholder='Select Product'
        )

        timestamp_slider: tuple[int, int] = st.slider(
            'Timeframe',
            0,
            999900,
            (0, 10000),
            step=1000
        )
        timestamp_min: int = timestamp_slider[0]
        timestamp_max: int = timestamp_slider[1]

        return day, product, timestamp_min, timestamp_max

    def load_indicators(self) -> Indicators:
        st.subheader('Indicators', divider='grey')

        show_mid_price = st.checkbox('Mid Price')
        show_mid_wall = st.checkbox('Mid Wall')

        return Indicators(
            show_mid_price=show_mid_price,
            show_mid_wall=show_mid_wall
        )

    def load_normalise_option(self) -> NormaliseOption:
        st.subheader('Normalise Option', divider='grey')

        normalise_option = st.selectbox(
            'Normalise',
            list(NormaliseOption),
            format_func=lambda option: option.name,
            index=None,
            placeholder='Select Normalise Option'
        )

        return normalise_option

    def load_trade_filters(self) -> tuple[bool, int, int]:
        st.subheader('Trade Filters', divider='grey')

        show_trades = st.checkbox('Show Trades')
        quantity_min = st.number_input('Min Quantity', min_value=0, step=1)
        quantity_max = st.number_input('Max Quantity', min_value=0, step=1, value=20)

        return show_trades, quantity_min, quantity_max
