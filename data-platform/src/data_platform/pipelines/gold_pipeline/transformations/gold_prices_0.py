from pyspark import pipelines as dp
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, least, greatest

spark = SparkSession.active()


@dp.materialized_view(
    name="prices_0",
    table_properties={
        "delta.feature.catalogManaged": "supported"
    },
    format="delta"
)
def prices_add_features() -> DataFrame:
    return (
        spark.read
        .table("imc_prosperity.silver.prices_0")
        .withColumn("bid_wall", least(col("bid_price_1"), col("bid_price_2"), col("bid_price_3")))
        .withColumn("ask_wall", greatest(col("ask_price_1"), col("ask_price_2"), col("ask_price_3")))
        .withColumn("mid_wall", (col("bid_wall") + col("ask_wall")) / 2)
    )
