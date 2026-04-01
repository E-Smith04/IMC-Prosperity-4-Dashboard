import streamlit as st
import json
from app.services import LogsService
from app.types import SidebarState, Indicators, HistoricalFilters, LogsFilters, Mode, VolumeMode
from data_platform_sdk.schema import (
    PriceFilters,
    TradeFilters,
    Product,
    NormaliseOption,
    Traders,
    LogsPriceFilters,
    LogsTradeFilters,
    LogsOrderFilters
)

class Sidebar:
    def __init__(self, mode: Mode) -> None:
        self.mode = mode

        self.round_number: int | None = None
        self.day: int | None = None
        self.product: Product | None = None
        self.timestamp_min: int | None = None
        self.timestamp_max: int | None = None
        self.quantity_min: int | None = None
        self.quantity_max: int | None = None
        self.buyers: list[Traders] | None = None
        self.sellers: list[Traders] | None = None
        self.normalise_option: NormaliseOption | None = None
        self.indicators: Indicators = Indicators()
        self.show_trades: bool = False
        self.show_orders: bool = False
        self.logs_uploaded: bool = False
        self.volume_mode: VolumeMode | None = None

        self.logs_service: LogsService = st.session_state.logs_service

    def load(self) -> SidebarState:
        with st.sidebar:
            if self.mode == Mode.HISTORICAL:
                self.load_file_options()
                self.load_volume_options()
                self.load_shared_filters()
                self.load_indicators()
                self.load_normalise_option()
                self.load_trade_filters()

                price_filters = PriceFilters(
                    round_number=self.round_number,
                    day=self.day,
                    product=self.product,
                    timestamp_min=self.timestamp_min,
                    timestamp_max=self.timestamp_max,
                    normalise_option=self.normalise_option
                )

                trade_filters = TradeFilters(
                    round_number=self.round_number,
                    day=self.day,
                    symbol=self.product,
                    timestamp_min=self.timestamp_min,
                    timestamp_max=self.timestamp_max,
                    normalise_option=self.normalise_option,
                    quantity_min=self.quantity_min,
                    quantity_max=self.quantity_max
                )

                filters = HistoricalFilters(
                    price_filters=price_filters,
                    trade_filters=trade_filters,
                )

            else:
                logs_file = st.file_uploader("Upload logs")
                if logs_file is not None:
                    logs_json = json.load(logs_file)

                    if logs_json["submissionId"] != st.session_state.logs_submission_id:
                        self.logs_service.upload_logs(logs_json)
                        st.session_state.logs_submission_id = logs_json["submissionId"]

                    self.logs_uploaded = True

                self.load_volume_options()
                self.load_shared_filters()
                self.load_trade_filters()
                self.load_order_filters()

                price_filters = LogsPriceFilters(
                    timestamp_min=self.timestamp_min,
                    timestamp_max=self.timestamp_max,
                    product=self.product,
                )

                trade_filters = LogsTradeFilters(
                    symbol=self.product,
                    timestamp_min=self.timestamp_min,
                    timestamp_max=self.timestamp_max,
                    quantity_min=self.quantity_min,
                    quantity_max=self.quantity_max
                )

                order_filters = LogsOrderFilters(
                    timestamp_min=self.timestamp_min,
                    timestamp_max=self.timestamp_max,
                    symbol=self.product,
                )

                filters = LogsFilters(
                    price_filters=price_filters,
                    trade_filters=trade_filters,
                    order_filters=order_filters
                )

            return SidebarState(
                mode=self.mode,
                logs_uploaded=self.logs_uploaded,
                show_trades=self.show_trades,
                show_orders=self.show_orders,
                indicators=self.indicators,
                filters=filters,
                volume_mode=self.volume_mode
            )

    def load_file_options(self) -> None:
        st.subheader('Options', divider='grey')

        self.round_number = st.selectbox(
            'Round',
            (0),
            placeholder='Select Round'
        )

        self.day = st.selectbox(
            'Day',
            (-2, -1),
            placeholder='Select Day'
        )

    def load_shared_filters(self) -> None:
        st.subheader('Filters', divider='grey')

        self.product = st.selectbox(
            'Product',
            list(Product),
            format_func=lambda prod: prod.name,
            placeholder='Select Product'
        )

        self.timestamp_min, self.timestamp_max = st.slider(
            'Timeframe',
            0,
            999900 if self.mode == Mode.HISTORICAL else 199900,
            (0, 10000),
            step=1000
        )

    def load_indicators(self) -> None:
        st.subheader('Indicators', divider='grey')

        show_mid_price = st.checkbox('Mid Price')
        show_mid_wall = st.checkbox('Mid Wall')

        self.indicators = Indicators(
            show_mid_price=show_mid_price,
            show_mid_wall=show_mid_wall
        )

    def load_normalise_option(self) -> None:
        st.subheader('Normalise Option', divider='grey')

        self.normalise_option = st.selectbox(
            'Normalise',
            list(NormaliseOption),
            format_func=lambda option: option.name,
            index=None,
            placeholder='Select Normalise Option'
        )

    def load_trade_filters(self) -> None:
        st.subheader('Trade Filters', divider='grey')

        self.show_trades = st.checkbox('Show Trades')
        self.quantity_min = st.number_input('Min Quantity', min_value=0, step=1)
        self.quantity_max = st.number_input('Max Quantity', min_value=0, step=1, value=20)

    def load_order_filters(self) -> None:
        st.subheader('Order Filters', divider='grey')

        self.show_orders = st.checkbox('Show Orders')

    def load_volume_options(self) -> None:
        st.subheader('Volume Options', divider='grey')

        self.volume_mode = st.selectbox(
            'Volume Mode',
            list(VolumeMode),
            format_func=lambda mode: mode.name,
            placeholder='Select Volume Mode'
        )
