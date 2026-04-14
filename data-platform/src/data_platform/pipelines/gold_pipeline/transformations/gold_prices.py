from pyspark import pipelines as dp
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, least, greatest, coalesce, lit

spark = SparkSession.active()


@dp.materialized_view(
    name="prices",
    table_properties={
        "delta.feature.catalogManaged": "supported"
    },
    format="delta"
)
def prices_add_features() -> DataFrame:
    return (
        spark.read
        .table("imc_prosperity.bronze.prices")
        .withColumn(
            "total_bid_volume",
            coalesce(col("bid_volume_1"), lit(0)) +
            coalesce(col("bid_volume_2"), lit(0)) +
            coalesce(col("bid_volume_3"), lit(0))
        )
        .withColumn(
            "total_ask_volume",
            coalesce(col("ask_volume_1"), lit(0)) +
            coalesce(col("ask_volume_2"), lit(0)) +
            coalesce(col("ask_volume_3"), lit(0))
        )
        .withColumn(
            "volume_net",
            col("total_bid_volume") - col("total_ask_volume")
        )
        .withColumn("bid_wall", least(col("bid_price_1"), col("bid_price_2"), col("bid_price_3")))
        .withColumn("ask_wall", greatest(col("ask_price_1"), col("ask_price_2"), col("ask_price_3")))
        .withColumn("mid_wall", (col("bid_wall") + col("ask_wall")) / 2)
    )
