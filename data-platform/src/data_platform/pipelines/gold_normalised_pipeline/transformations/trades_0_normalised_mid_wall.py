from pyspark import pipelines as dp
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col

spark = SparkSession.active()


@dp.materialized_view(
    name="trades_0_normalised_mid_wall",
    table_properties={
        "delta.feature.catalogManaged": "supported"
    },
    format="delta"
)
def trades_normalise() -> DataFrame:
    prices_df = (
        spark.read.table("imc_prosperity.gold.prices_0")
        .select("day", "timestamp", "product", "mid_wall")
        .withColumnRenamed("product", "symbol")
    )

    trades_df = spark.read.table("imc_prosperity.bronze.trades_0")
    return (
        trades_df.join(prices_df, on=["day", "timestamp", "symbol"], how="inner")
        .withColumn("price", (col("price") - col("mid_wall")) / col("mid_wall"))
        .drop("mid_wall")
    )
