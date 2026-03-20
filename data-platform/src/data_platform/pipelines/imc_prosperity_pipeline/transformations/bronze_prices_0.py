from pyspark import pipelines as dp
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

spark = SparkSession.active()

schema = StructType(
    [
        StructField("day", StringType(), True),
        StructField("timestamp", IntegerType(), True),
        StructField("product", StringType(), True),
        StructField("bid_price_1", IntegerType(), True),
        StructField("bid_volume_1", IntegerType(), True),
        StructField("bid_price_2", IntegerType(), True),
        StructField("bid_volume_2", IntegerType(), True),
        StructField("bid_price_3", IntegerType(), True),
        StructField("bid_volume_3", IntegerType(), True),
        StructField("ask_price_1", IntegerType(), True),
        StructField("ask_volume_1", IntegerType(), True),
        StructField("ask_price_2", IntegerType(), True),
        StructField("ask_volume_2", IntegerType(), True),
        StructField("ask_price_3", IntegerType(), True),
        StructField("ask_volume_3", IntegerType(), True),
        StructField("mid_price", FloatType(), True),
        StructField("profit_and_loss", FloatType(), True)
    ]
)

@dp.materialized_view(
    name="imc_prosperity.bronze.prices_0",
    table_properties={
        "delta.feature.catalogManaged": "supported"
    },
    schema=schema,
    format="delta"
)
def prices_tutorial_raw() -> DataFrame:
    return (
        spark.read
        .format("csv")
        .schema(schema)
        .options(
            delimiter=";",
            header=True
        )
        .load("./data/TUTORIAL_ROUND_1/prices_*.csv")
    )
