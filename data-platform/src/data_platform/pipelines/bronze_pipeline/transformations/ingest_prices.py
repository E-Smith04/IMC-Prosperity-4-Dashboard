from pyspark import pipelines as dp
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType
from pyspark.sql.functions import input_file_name, regexp_extract

spark = SparkSession.active()

schema = StructType(
    [
        StructField("day", IntegerType(), True),
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

@dp.table(
    name="prices",
    table_properties={
        "delta.feature.catalogManaged": "supported"
    },
    format="delta"
)
def bronze_prices() -> DataFrame:
    return (
        spark.readStream
        .format("csv")
        .schema(schema)
        .option("header", "true")
        .option("delimiter", ";")
        .load("./data/*/prices_*.csv")
        .withColumn("source_file", input_file_name())
        .withColumn(
            "round",
            regexp_extract("source_file", r"round_(\d+)", 1).cast("int")
        )
        .drop("source_file")
    )