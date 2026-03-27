from pyspark import pipelines as dp
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col

spark = SparkSession.active()


@dp.materialized_view(
    name="trades_normalised_mid_wall",
    table_properties={
        "delta.feature.catalogManaged": "supported"
    },
    format="delta"
)
def trades_normalise_mid_wall() -> DataFrame:
    return (
        spark.table("imc_prosperity.bronze.trades")
        .join(
            spark.table("imc_prosperity.gold.prices")
            .select("round", "day", "timestamp", "product", "mid_wall")
            .withColumnRenamed("product", "symbol"),
            on=["round", "day", "timestamp", "symbol"],
            how="inner"
        )
        .withColumn("price", (col("price") - col("mid_wall")) / col("mid_wall"))
        .drop("mid_wall")
    )
