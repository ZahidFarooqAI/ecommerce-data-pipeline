import os
import sys
from google.cloud import storage

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.config import GCS_BUCKET, PATHS, GOOGLE_CREDENTIALS


def upload_to_gcs(local_file_path, gcs_folder, credentials_path=None):
    """Upload a local file to Google Cloud Storage."""
    credentials_path = (
        credentials_path
        or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        or GOOGLE_CREDENTIALS
    )
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
    print(f"Uploaded {local_file_path} to gs://{GCS_BUCKET}/{gcs_folder}")


if __name__ == "__main__":
    local_file = "data/data.csv"
    upload_to_gcs(local_file, PATHS["raw"])
    upload_to_gcs(local_file, PATHS["raw"])