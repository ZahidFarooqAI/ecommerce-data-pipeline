import os
import sys
from pathlib import Path

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from google.cloud import bigquery
from src.config import (
    BIGQUERY_PROJECT,
    BIGQUERY_DATASET,
    BIGQUERY_TABLE,
    BIGQUERY_CLEAN_TABLE,
    BIGQUERY_AGG_TABLE,
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


def _load_sql_file(filename):
    path = Path(__file__).resolve().parent.parent / "sql" / filename
    return path.read_text()


def _render_sql(template):
    return (
        template
        .replace("{PROJECT}", BIGQUERY_PROJECT)
        .replace("{DATASET}", BIGQUERY_DATASET)
        .replace("{TABLE}", BIGQUERY_TABLE)
        .replace("{CLEAN_TABLE}", BIGQUERY_CLEAN_TABLE)
        .replace("{AGG_TABLE}", BIGQUERY_AGG_TABLE)
    )


def build_clean_orders_table():
    client = _get_client()
    query = _render_sql(_load_sql_file("clean_orders.sql"))
    destination = f"{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.{BIGQUERY_CLEAN_TABLE}"
    job_config = bigquery.QueryJobConfig(
        destination=destination,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        time_partitioning=bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="InvoiceDateOnly",
        ),
        clustering_fields=["Country", "CustomerID"],
    )
    job = client.query(query, job_config=job_config)
    job.result()
    print(f"Created cleaned orders table: {destination}")
    return destination


def build_aggregate_table():
    client = _get_client()
    query = _render_sql(_load_sql_file("aggregate_orders.sql"))
    destination = f"{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.{BIGQUERY_AGG_TABLE}"
    job_config = bigquery.QueryJobConfig(
        destination=destination,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        time_partitioning=bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="order_date",
        ),
        clustering_fields=["unique_customers"],
    )
    job = client.query(query, job_config=job_config)
    job.result()
    print(f"Created aggregated dashboard table: {destination}")
    return destination


if __name__ == "__main__":
    build_clean_orders_table()
    build_aggregate_table()
