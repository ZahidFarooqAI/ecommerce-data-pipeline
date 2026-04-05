import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.config import (
    PATHS,
    DATA_FILE,
    BIGQUERY_PROJECT,
    BIGQUERY_DATASET,
    BIGQUERY_TABLE,
)
from src.ingestion.upload_to_gcs import upload_to_gcs
from src.ingestion.processing.clean_data import clean_local_data, upload_processed_data
from src.ingestion.warehouse.load_to_bigquery import load_csv_to_bigquery
from src.ingestion.warehouse.transform_data import build_clean_orders_table, build_aggregate_table


def run_pipeline():
    print("Starting ingestion pipeline...")
    upload_to_gcs(DATA_FILE, PATHS["raw"])

    print("Cleaning local source data...")
    cleaned_path = clean_local_data()

    print("Uploading cleaned data to processed lake...")
    processed_uri = upload_processed_data(cleaned_path)

    print("Loading cleaned data into BigQuery...")
    target_table = f"{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE}"
    load_csv_to_bigquery(processed_uri, target_table)

    print("Building cleaned warehouse table...")
    build_clean_orders_table()

    print("Building aggregated dashboard table...")
    build_aggregate_table()

    print("Pipeline complete.")
    print(f"BigQuery table: {target_table}")


if __name__ == "__main__":
    run_pipeline()
