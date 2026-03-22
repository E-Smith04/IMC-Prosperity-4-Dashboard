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
        StructField("quantity", IntegerType(), True),
        StructField("day", IntegerType(), True),
    ]
)

@dp.materialized_view(
    name="trades_0",
    table_properties={
        "delta.feature.catalogManaged": "supported"
    },
    schema=schema,
    format="delta"
)
def ingest_trades_raw() -> DataFrame:
    return (
        spark.read
        .format("csv")
        .schema(schema)
        .options(
            delimiter=";",
            header=True
        )
        .load("./data/TUTORIAL_ROUND_1/trades_*.csv")
        .withColumn("source_file", input_file_name())
        .withColumn(
            "day",
            regexp_extract(col("source_file"), r"day_(-?\d+)\.csv", 1).cast(IntegerType())
        )
        .drop("source_file")
    )
