# Terraform Infrastructure

This directory adds an isolated Terraform scaffold for the existing ecommerce data pipeline.

It is intentionally separate from the Python pipeline so the current project structure, scripts, and submission flow remain unchanged.

## What It Provisions

- A Google Cloud Storage bucket for the data lake
- A BigQuery dataset for warehouse tables
- An optional Artifact Registry repository for Docker images
- An optional Cloud Run service for the Streamlit dashboard

The Python pipeline still creates and refreshes the BigQuery tables during execution.

## Structure

```text
terraform/
├── main.tf
├── modules/
│   ├── artifact_registry/
│   ├── bigquery/
│   ├── cloud_run_dashboard/
│   └── gcs_bucket/
├── outputs.tf
├── providers.tf
├── terraform.tfvars.example
├── variables.tf
└── versions.tf
```

## Usage

1. Install Terraform.
2. Copy the example variables file:

   ```bash
   cp terraform/terraform.tfvars.example terraform/terraform.tfvars
   ```

3. Update the values to match your GCP project and desired bucket/dataset names.
4. Authenticate with Google Cloud before applying Terraform.
5. Run:

   ```bash
   cd terraform
   terraform init
   terraform plan
   terraform apply
   ```

## Docker and Cloud Run Flow

If you want to deploy the dashboard container:

1. Build the Docker image from the repository root:

   ```bash
   docker build -t ecommerce-dashboard:latest .
   ```

2. Push the image to Artifact Registry after Terraform creates the repository.
3. Set `dashboard_container_image` in `terraform.tfvars`.
4. Set `deploy_dashboard = true`.
5. Run `terraform apply` again to create the Cloud Run service.

The dashboard container defaults to `DASHBOARD_DATA_SOURCE=bigquery`, which makes it suitable for Cloud Run where a local CSV file is usually not the primary data source.

## How It Fits This Project

- Set the bucket name from Terraform into `src/config.py` as `GCS_BUCKET`
- Set the project ID into `src/config.py` as `BIGQUERY_PROJECT`
- Set the dataset name into `src/config.py` as `BIGQUERY_DATASET`
- Keep the current Python pipeline as the runtime orchestration layer
- Use environment variables in container deployments instead of hardcoding values where possible

This keeps the original project behavior intact while adding an infrastructure-as-code layer for deployment and submission purposes.
