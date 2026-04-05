"""Project configuration for data pipeline paths and GCS/BigQuery settings."""

# TODO: replace these values with your actual Google Cloud resources.
GCS_BUCKET = "your-gcs-bucket-name"
BIGQUERY_PROJECT = "your-gcp-project-id"
BIGQUERY_DATASET = "ecommerce"
BIGQUERY_TABLE = "raw_orders"
BIGQUERY_CLEAN_TABLE = "clean_orders"
BIGQUERY_AGG_TABLE = "daily_sales_summary"

PATHS = {
    "raw": "raw/",
    "processed": "processed/",
    "warehouse": "warehouse/",
}

DATA_FILE = "data/data.csv"
PROCESSED_FILE = "data/processed_data.csv"
GOOGLE_CREDENTIALS = "keys/gcp-key.json"
