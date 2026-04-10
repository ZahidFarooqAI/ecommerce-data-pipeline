"""Project configuration for data pipeline paths and GCS/BigQuery settings."""

import os


def _get_env_or_default(name, default):
    value = os.getenv(name)
    return value if value not in (None, "") else default


# TODO: replace these values with your actual Google Cloud resources.
GCS_BUCKET = _get_env_or_default("GCS_BUCKET", "your-gcs-bucket-name")
BIGQUERY_PROJECT = _get_env_or_default("BIGQUERY_PROJECT", "your-gcp-project-id")
BIGQUERY_DATASET = _get_env_or_default("BIGQUERY_DATASET", "ecommerce")
BIGQUERY_TABLE = _get_env_or_default("BIGQUERY_TABLE", "raw_orders")
BIGQUERY_CLEAN_TABLE = _get_env_or_default("BIGQUERY_CLEAN_TABLE", "clean_orders")
BIGQUERY_AGG_TABLE = _get_env_or_default("BIGQUERY_AGG_TABLE", "daily_sales_summary")

PATHS = {
    "raw": "raw/",
    "processed": "processed/",
    "warehouse": "warehouse/",
}

DATA_FILE = _get_env_or_default("DATA_FILE", "data/data.csv")
PROCESSED_FILE = _get_env_or_default("PROCESSED_FILE", "data/processed_data.csv")
GOOGLE_CREDENTIALS = _get_env_or_default("GOOGLE_CREDENTIALS", "keys/gcp-key.json")
