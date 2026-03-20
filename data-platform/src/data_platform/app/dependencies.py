from pyspark.sql import SparkSession
from data_platform.app.core.config import settings

spark = SparkSession.builder \
    .remote(settings.SPARK_CONNECT_URL) \
    .getOrCreate()

def get_spark():
   return spark
