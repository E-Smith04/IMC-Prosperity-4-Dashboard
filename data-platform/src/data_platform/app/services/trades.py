import numpy as np

from fastapi import Depends
from pyspark.sql import SparkSession
from typing import Annotated, Any

from data_platform.app.core.dependencies import get_spark
from data_platform.app.schemas.trades import TradeFilters

class TradesService:
    def __init__(self, spark: Annotated[SparkSession, Depends(get_spark)]):
        self.spark = spark

    def read_trades(self, round_num: int, trade_filters: TradeFilters) -> list[dict[str, Any]]:
        filters_dict = trade_filters.model_dump(mode="json", exclude_none=True)

        table_name = f"imc_prosperity.bronze.trades_{round_num}"
        query = f"SELECT * FROM {table_name}"

        where_clauses = []

        if trade_filters.day is not None:
            where_clauses.append("day = {day}")
        if trade_filters.timestamp_min is not None:
            where_clauses.append("timestamp >= {timestamp_min}")
        if trade_filters.timestamp_max is not None:
            where_clauses.append("timestamp <= {timestamp_max}")
        if trade_filters.symbol is not None:
            where_clauses.append("symbol = {symbol}")
        if trade_filters.quantity_min is not None:
            where_clauses.append("quantity >= {quantity_min}")
        if trade_filters.quantity_max is not None:
            where_clauses.append("quantity <= {quantity_max}")
        if trade_filters.buyers is not None:
            where_clauses.append("buyers IN {buyers}")
        if trade_filters.sellers is not None:
            where_clauses.append("sellers IN {sellers}")

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        df = self.spark.sql(query, **filters_dict)
        pdf = df.toPandas()
        pdf = pdf.replace({np.nan: None})
        return pdf.to_dict(orient="records")