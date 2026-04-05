import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from google.cloud import bigquery
from src.config import (
    BIGQUERY_PROJECT,
    BIGQUERY_DATASET,
    BIGQUERY_TABLE,
    GOOGLE_CREDENTIALS,
)


def _get_client():
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or GOOGLE_CREDENTIALS
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f"GCP credentials not found: {credentials_path}. "
            "Set GOOGLE_APPLICATION_CREDENTIALS or update src/config.py."
        )
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    return bigquery.Client(project=BIGQUERY_PROJECT)


def ensure_dataset(client):
    dataset_id = f"{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    client.create_dataset(dataset, exists_ok=True)
    print(f"Ensured BigQuery dataset exists: {dataset_id}")


def load_csv_to_bigquery(source_uri, destination_table=None):
    """Load a CSV file from GCS into BigQuery."""
    client = _get_client()
    ensure_dataset(client)

    destination_table = destination_table or f"{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE}"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    load_job = client.load_table_from_uri(source_uri, destination_table, job_config=job_config)
    load_job.result()
    table = client.get_table(destination_table)

    print(
        f"Loaded {table.num_rows} rows into BigQuery table {destination_table} "
        f"from {source_uri}."
    )
    return destination_table


def run_query(query, destination_table=None):
    client = _get_client()
    if destination_table:
        job_config = bigquery.QueryJobConfig(
            destination=destination_table,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )
    else:
        job_config = None

    query_job = client.query(query, job_config=job_config)
    query_job.result()
    print(f"Executed query. Destination: {destination_table or 'temporary result'}")
    return query_job


if __name__ == "__main__":
    print("This module contains loader utilities for BigQuery.")
