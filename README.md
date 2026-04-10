# ecommerce-data-pipeline
Built an end-to-end batch data pipeline on Google Cloud Platform that ingests data from external sources, stores data in a data lake (GCS), transforms and loads data into BigQuery, and visualizes insights using a dashboard.

## Features
- **Data Ingestion**: Upload raw CSV to Google Cloud Storage (GCS) data lake
- **Data Processing**: Clean and transform data locally or in the cloud
- **Data Warehouse**: Load processed data into BigQuery and create aggregated tables
- **Dashboard**: Streamlit app with two key metric tiles (Total Revenue, Total Orders) and daily sales chart
- link to dash board   https://orange-lamp-v6gp9w6566jvhpq56-8501.app.github.dev/

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Update `src/config.py` with your GCP settings (bucket, project, dataset)

## Test the Pipeline
```bash
python test_pipeline.py
```

## Run Local Data Processing
```bash
python src/ingestion/processing/clean_data.py
```

## Run Full Pipeline (requires GCP setup)
```bash
python src/ingestion/run_pipeline.py
```

## Run the Dashboard
```bash
streamlit run src/dashboard/app.py
```

## Terraform Infrastructure
This project now includes an optional Terraform scaffold in [`terraform/`](/workspaces/ecommerce-data-pipeline/terraform) for provisioning the GCS bucket and BigQuery dataset used by the pipeline.

Example workflow:
```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
cd terraform
terraform init
terraform plan
terraform apply
```

After provisioning, copy the Terraform outputs into `src/config.py` so the Python pipeline uses the created resources.

## Docker Container
This project also includes a [`Dockerfile`](/workspaces/ecommerce-data-pipeline/Dockerfile) for containerizing the Streamlit dashboard.

Build locally:
```bash
docker build -t ecommerce-dashboard:latest .
docker run -p 8080:8080 \
  -e DASHBOARD_DATA_SOURCE=bigquery \
  -e BIGQUERY_PROJECT=your-gcp-project-id \
  -e BIGQUERY_DATASET=ecommerce \
  -e BIGQUERY_AGG_TABLE=daily_sales_summary \
  ecommerce-dashboard:latest
```

You can combine this with Terraform to provision Artifact Registry and an optional Cloud Run deployment for the container image.

## Docker Compose
For a simpler local demo, you can run the dashboard with [`docker-compose.yml`](/workspaces/ecommerce-data-pipeline/docker-compose.yml).

Start the app:
```bash
docker compose up --build
```

Then open `http://localhost:8080`.

This compose setup uses `DASHBOARD_DATA_SOURCE=local` so it works with the processed CSV and does not require BigQuery for a basic submission demo.
It also generates `data/processed_data.csv` inside the container automatically before starting the dashboard.

## Suggested Demo Flow
For submission purposes, the easiest way to demo the project is:

```bash
docker compose up --build
```

For cloud deployment, use the Terraform scaffold to provision GCS, BigQuery, Artifact Registry, and optionally Cloud Run for the dashboard container.

## Project Structure
- `data/data.csv`: Raw ecommerce dataset
- `data/processed_data.csv`: Cleaned dataset (generated)
- `src/ingestion/`: Pipeline components
- `src/dashboard/`: Streamlit dashboard app
- `docker-compose.yml`: Local container demo setup
- `terraform/`: Optional infrastructure-as-code for GCP resources
- `src/config.py`: Configuration settings
- `requirements.txt`: Python dependencies
- `test_pipeline.py`: Pipeline validation script

## Dashboard Features
- **Metric Tiles**:
  - Total Revenue ($)
  - Total Orders (count)
- **Graphs**:
  - Revenue by Country (Top 10) - Bar chart showing categorical distribution
  - Daily Revenue Trend - Line chart showing temporal distribution
- **Interactive Elements**: Expandable data table for daily summaries

## Notes
- The dashboard defaults to local processed data for easy testing
- Full cloud pipeline requires valid GCP credentials and billing
- Dataset: Online Retail II (UCI Machine Learning Repository)
