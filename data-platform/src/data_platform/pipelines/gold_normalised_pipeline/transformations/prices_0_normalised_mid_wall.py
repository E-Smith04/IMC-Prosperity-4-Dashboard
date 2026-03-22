from pyspark import pipelines as dp
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col

spark = SparkSession.active()


@dp.materialized_view(
    name="prices_0_normalised_mid_wall",
    table_properties={
        "delta.feature.catalogManaged": "supported"
    },
    format="delta"
)
def prices_normalise() -> DataFrame:
    df = spark.read.table("imc_prosperity.gold.prices_0")

    price_cols = [
        "bid_price_1", "bid_price_2", "bid_price_3",
        "ask_price_1", "ask_price_2", "ask_price_3",
        "mid_price", "mid_wall"
    ]

    normalisation_map = {
        c: (col(c) - col("mid_wall")) / col("mid_wall")
        for c in price_cols
    }

    return df.withColumns(normalisation_map)
