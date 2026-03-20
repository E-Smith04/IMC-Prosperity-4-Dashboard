from pyspark.sql import SparkSession
from data_platform.app.core.config import settings


def get_spark():
    spark = SparkSession.builder \
        .remote(settings.SPARK_CONNECT_URL) \
        .getOrCreate()
    return spark
