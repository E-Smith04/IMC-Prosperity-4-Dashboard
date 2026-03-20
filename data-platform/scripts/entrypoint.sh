#!/bin/sh

set -e

# Temporary fix
echo "Waiting for spark connect server"
sleep 40

echo "Running pipelines..."

spark-pipelines run \
    --remote "$SPARK_CONNECT_URL" \
    --spec "src/data_platform/pipelines/imc_prosperity_pipeline/spark-pipeline.yml"

echo "Pipelines complete. Starting API..."

exec "$@"