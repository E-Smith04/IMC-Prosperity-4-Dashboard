from pyspark import pipelines as dp
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType
from pyspark.sql.functions import input_file_name, col, regexp_extract

spark = SparkSession.active()

schema = StructType(
    [
        StructField("timestamp", IntegerType(), True),
        StructField("buyer", StringType(), True),
        StructField("seller", StringType(), True),
        StructField("symbol", StringType(), True),
        StructField("currency", StringType(), True),
        StructField("price", FloatType(), True),
        StructField("quantity", IntegerType(), True)
    ]
)

@dp.table(
    name="trades",
    table_properties={
        "delta.feature.catalogManaged": "supported"
    },
    format="delta"
)
def bronze_trades() -> DataFrame:
    return (
        spark.readStream
        .format("csv")
        .schema(schema)
        .option("header", "true")
        .option("delimiter", ";")
        .load("./data/*/trades_*.csv")
        .withColumn("source_file", input_file_name())
        .withColumn(
            "round",
            regexp_extract("source_file", r"round_(\d+)", 1).cast("int")
        )
        .withColumn(
            "day",
            regexp_extract("source_file", r"day_(-?\d+)", 1).cast("int")
        )
        .drop("source_file")
    )
