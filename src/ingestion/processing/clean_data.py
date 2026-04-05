import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
from google.cloud import storage
from src.config import DATA_FILE, PROCESSED_FILE, PATHS, GCS_BUCKET, GOOGLE_CREDENTIALS


def clean_local_data(input_path=None, output_path=None):
    """Clean the source CSV and write a processed CSV file."""
    input_path = input_path or DATA_FILE
    output_path = output_path or PROCESSED_FILE

    df = pd.read_csv(input_path, parse_dates=["InvoiceDate"], dayfirst=False)
    expected_columns = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country",
    ]
    df = df.loc[:, expected_columns]

    df = df.dropna(subset=["InvoiceNo", "Quantity", "UnitPrice", "CustomerID", "InvoiceDate"])
    df = df[df["Quantity"] > 0]
    df = df[df["UnitPrice"] >= 0]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df = df.dropna(subset=["InvoiceDate"])
    df["CustomerID"] = df["CustomerID"].astype(int)
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
    df["Country"] = df["Country"].astype(str).str.strip()

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    df.to_csv(output_path, index=False)
    print(f"Cleaned data written to {output_path}")
    return output_path


def upload_processed_data(local_file_path=None, gcs_folder=None, credentials_path=None):
    """Upload the cleaned dataset to the processed layer in GCS."""
    local_file_path = local_file_path or PROCESSED_FILE
    gcs_folder = gcs_folder or PATHS["processed"]
    credentials_path = credentials_path or os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or GOOGLE_CREDENTIALS

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            f"GCP credentials not found: {credentials_path}. "
            "Set GOOGLE_APPLICATION_CREDENTIALS or update src/config.py."
        )
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    if not gcs_folder.endswith("/"):
        gcs_folder = f"{gcs_folder}/"

    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET)
    blob = bucket.blob(f"{gcs_folder}{os.path.basename(local_file_path)}")
    blob.upload_from_filename(local_file_path)
    print(f"Uploaded processed file to gs://{GCS_BUCKET}/{gcs_folder}{os.path.basename(local_file_path)}")
    return f"gs://{GCS_BUCKET}/{gcs_folder}{os.path.basename(local_file_path)}"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Clean ecommerce data and optionally upload it to GCS.")
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Upload the cleaned CSV to the GCS processed path. Requires valid GCS config.",
    )
    args = parser.parse_args()

    cleaned_path = clean_local_data()
    if args.upload:
        upload_processed_data(cleaned_path)
