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

## Project Structure
- `data/data.csv`: Raw ecommerce dataset
- `data/processed_data.csv`: Cleaned dataset (generated)
- `src/ingestion/`: Pipeline components
- `src/dashboard/`: Streamlit dashboard app
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
