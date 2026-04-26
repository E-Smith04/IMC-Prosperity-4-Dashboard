import pandas as pd
import numpy as np
from io import StringIO
from fastapi import Depends
from pyspark.sql import SparkSession
from typing import Annotated, Any

from data_platform.app.core.dependencies import get_spark
from data_platform.app.schemas.logs import LogsUpload, LogsPriceFilters, LogsTradeFilters, LogsOrderFilters

_PRICE_CLAUSES: dict[str, str] = {
    "timestamp_min": "timestamp >= {timestamp_min}",
    "timestamp_max": "timestamp <= {timestamp_max}",
    "product": "product = {product}",
}

_TRADE_CLAUSES: dict[str, str] = {
    "timestamp_min": "timestamp >= {timestamp_min}",
    "timestamp_max": "timestamp <= {timestamp_max}",
    "symbol": "symbol = {symbol}",
    "quantity_min": "quantity >= {quantity_min}",
    "quantity_max": "quantity <= {quantity_max}",
}

_ORDER_CLAUSES: dict[str, str] = {
    "timestamp_min": "timestamp >= {timestamp_min}",
    "timestamp_max": "timestamp <= {timestamp_max}",
    "symbol": "symbol = {symbol}",
}


class LogsService:
    def __init__(self, spark: Annotated[SparkSession, Depends(get_spark)]):
        self.spark = spark

    def upload(self, logs: LogsUpload) -> None:
        activities_log = StringIO(logs.activitiesLog)
        activities_log_df = pd.read_csv(activities_log, sep=";")
        prices_df = (
            activities_log_df
            .merge(
                pd.DataFrame(logs.flattened_positions),
                on=["timestamp", "product"],
                how="left"
            )
            .assign(position=lambda d: d["position"].fillna(0).astype(int))
            .assign(
                total_bid_volume=lambda d: d[["bid_volume_1", "bid_volume_2", "bid_volume_3"]].sum(axis=1),
                total_ask_volume=lambda d: d[["ask_volume_1", "ask_volume_2", "ask_volume_3"]].sum(axis=1),
                volume_net=lambda d: d["total_bid_volume"] - d["total_ask_volume"]
            )
        )
        self._create_table("imc_prosperity.logs.prices", prices_df)

        trade_history = logs.tradeHistory
        self._create_table("imc_prosperity.logs.trades", trade_history)

        flattened_orders = logs.flattened_orders
        self._create_table("imc_prosperity.logs.orders", flattened_orders)

    def get_prices(self, price_filters: LogsPriceFilters) -> list[dict[str, Any]]:
        table_name = "imc_prosperity.logs.prices"

        return self._execute_query(table_name, price_filters, _PRICE_CLAUSES)

    def get_trades(self, trade_filters: LogsTradeFilters) -> list[dict[str, Any]]:
        table_name = "imc_prosperity.logs.trades"

        return self._execute_query(table_name, trade_filters, _TRADE_CLAUSES)

    def get_orders(self, order_filters: LogsOrderFilters) -> list[dict[str, Any]]:
        table_name = "imc_prosperity.logs.orders"

        return self._execute_query(table_name, order_filters, _ORDER_CLAUSES)

    def _execute_query(
            self,
            table_name: str,
            filters: LogsPriceFilters | LogsTradeFilters | LogsOrderFilters,
            clause_map: dict[str, str]
    ) -> list[dict[str, Any]]:
        sql_params = filters.model_dump(
            mode="json",
            exclude_none=True,
            exclude={"normalise_option"},
        )

        where_clauses = [
            clause
            for field, clause in clause_map.items()
            if getattr(filters, field) is not None
        ]

        if "buyers" in sql_params:
            where_clauses.append(
                self._build_or_clause("buyer", filters.buyers)
            )

        if "sellers" in sql_params:
            where_clauses.append(
                self._build_or_clause("seller", filters.sellers)
            )

        query = f"SELECT * FROM {table_name}"
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        try:
            df = self.spark.sql(query, **sql_params)
        except Exception:
            return []

        pdf = df.toPandas()
        pdf = pdf.replace({np.nan: None})
        return pdf.to_dict(orient="records")

    def _create_table(self, table_name: str, data: list[dict[str, Any]] | pd.DataFrame) -> None:
        self.spark.sql(f"DROP TABLE IF EXISTS {table_name}")
        self.spark.createDataFrame(data) \
            .orderBy('timestamp') \
            .writeTo(f"{table_name}") \
            .using("delta") \
            .tableProperty("delta.feature.catalogManaged", "supported") \
            .create()

    @staticmethod
    def _build_or_clause(column: str, values: list[str]) -> str:
        return "(" + " OR ".join(f"{column} = '{v}'" for v in values) + ")"
