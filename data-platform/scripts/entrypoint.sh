#!/bin/sh

set -e

echo "Running pipelines..."

spark-pipelines run \
    --remote "$SPARK_CONNECT_URL" \
    --spec "src/data_platform/pipelines/bronze_pipeline/spark-pipeline.yml"

spark-pipelines run \
    --remote "$SPARK_CONNECT_URL" \
    --spec "src/data_platform/pipelines/silver_pipeline/spark-pipeline.yml"

spark-pipelines run \
    --remote "$SPARK_CONNECT_URL" \
    --spec "src/data_platform/pipelines/gold_pipeline/spark-pipeline.yml"

spark-pipelines run \
    --remote "$SPARK_CONNECT_URL" \
    --spec "src/data_platform/pipelines/gold_normalised_pipeline/spark-pipeline.yml"

echo "Pipelines complete. Starting API..."

exec "$@"