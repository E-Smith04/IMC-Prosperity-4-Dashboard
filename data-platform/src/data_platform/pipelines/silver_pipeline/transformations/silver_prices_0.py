from pyspark import pipelines as dp
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col

spark = SparkSession.active()


@dp.materialized_view(
    name="prices_0",
    table_properties={
        "delta.feature.catalogManaged": "supported"
    },
    format="delta"
)
def prices_drop_cols() -> DataFrame:
    profit_and_loss_col = col("profit_and_loss")

    return (
        spark.read
        .table("imc_prosperity.bronze.prices_0")
        .drop(profit_and_loss_col)
    )
