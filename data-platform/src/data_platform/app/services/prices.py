import numpy as np

from fastapi import Depends
from pyspark.sql import SparkSession
from typing import Annotated, Any

from data_platform.app.dependencies import get_spark
from data_platform.app.schemas.prices import PriceFilters

class PricesService:
    def __init__(self, spark: Annotated[SparkSession, Depends(get_spark)]):
        self.spark = spark

    def read_prices(self, round_num: int, price_filters: PriceFilters) -> list[dict[str, Any]]:
        filters_dict = price_filters.model_dump(mode="json", exclude_none=True)

        table_name = f"imc_prosperity.bronze.prices_{round_num}"
        query = f"SELECT * FROM {table_name}"

        where_clauses = []

        if price_filters.day is not None:
            where_clauses.append("day = {day}")
        if price_filters.timestamp_min is not None:
            where_clauses.append("timestamp >= {timestamp_min}")
        if price_filters.timestamp_max is not None:
            where_clauses.append("timestamp <= {timestamp_max}")
        if price_filters.product is not None:
            where_clauses.append("product = {product}")

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        df = self.spark.sql(query, **filters_dict)
        pdf = df.toPandas()
        pdf = pdf.replace({np.nan: None})
        return pdf.to_dict(orient="records")