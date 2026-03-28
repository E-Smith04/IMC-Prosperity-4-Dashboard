import numpy as np

from fastapi import Depends
from pyspark.sql import SparkSession
from typing import Annotated, Any

from data_platform.app.core.dependencies import get_spark
from data_platform.app.schemas.historical import PriceFilters, TradeFilters

_PRICE_CLAUSES: dict[str, str] = {
    "round_number": "round = {round_number}",
    "day": "day = {day}",
    "timestamp_min": "timestamp >= {timestamp_min}",
    "timestamp_max": "timestamp <= {timestamp_max}",
    "product": "product = {product}",
}

_TRADE_CLAUSES: dict[str, str] = {
    "round_number": "round = {round_number}",
    "day": "day = {day}",
    "timestamp_min": "timestamp >= {timestamp_min}",
    "timestamp_max": "timestamp <= {timestamp_max}",
    "symbol": "symbol = {symbol}",
    "quantity_min": "quantity >= {quantity_min}",
    "quantity_max": "quantity <= {quantity_max}",
    "buyers": "buyers IN {buyers}",
    "sellers": "sellers IN {sellers}",
}


class HistoricalService:
    def __init__(self, spark: Annotated[SparkSession, Depends(get_spark)]):
        self.spark = spark

    def get_prices(self, price_filters: PriceFilters) -> list[dict[str, Any]]:
        table_name = f"imc_prosperity.gold.prices"
        if price_filters.normalise_option is not None:
            table_name += f"_normalised_{price_filters.normalise_option}"

        return self._execute_query(table_name, price_filters, _PRICE_CLAUSES)

    def get_trades(self, trade_filters: TradeFilters) -> list[dict[str, Any]]:
        table_name = "imc_prosperity.bronze.trades"
        if trade_filters.normalise_option is not None:
            table_name = f"imc_prosperity.gold.trades_normalised_{trade_filters.normalise_option}"

        return self._execute_query(table_name, trade_filters, _TRADE_CLAUSES)

    def _execute_query(
            self,
            table_name: str,
            filters: PriceFilters | TradeFilters,
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

        query = f"SELECT * FROM {table_name}"
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        df = self.spark.sql(query, **sql_params)
        pdf = df.toPandas()
        pdf = pdf.replace({np.nan: None})
        return pdf.to_dict(orient="records")