import os
import sys
from pathlib import Path

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
import streamlit as st

from src.config import (
    PROCESSED_FILE,
    BIGQUERY_PROJECT,
    BIGQUERY_DATASET,
    BIGQUERY_AGG_TABLE,
    GOOGLE_CREDENTIALS,
)

try:
    from google.cloud import bigquery
except ImportError:
    bigquery = None


def get_dashboard_data_source():
    return os.getenv("DASHBOARD_DATA_SOURCE", "auto").strip().lower()


def load_local_data():
    csv_path = Path(PROCESSED_FILE)
    if not csv_path.exists():
        st.error(
            f"Processed dataset not found at {csv_path}. Run the pipeline first: `python src/ingestion/run_pipeline.py`."
        )
        st.stop()

    df = pd.read_csv(csv_path, parse_dates=["InvoiceDate"])
    return df


def load_bigquery_data():
    if bigquery is None:
        st.error("google-cloud-bigquery is not installed. Add it to requirements and reinstall.")
        st.stop()

    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or GOOGLE_CREDENTIALS
    if credentials_path and Path(credentials_path).exists():
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    client = bigquery.Client(project=BIGQUERY_PROJECT)
    query = f"""
        SELECT order_date, total_orders, total_revenue, total_quantity, unique_customers
        FROM `{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.{BIGQUERY_AGG_TABLE}`
        ORDER BY order_date
    """
    return client.query(query).to_dataframe()


def build_tiles(df):
    total_revenue = df["TotalPrice"].sum() if "TotalPrice" in df.columns else df["total_revenue"].sum()
    total_orders = df["InvoiceNo"].nunique() if "InvoiceNo" in df.columns else int(df["total_orders"].sum())

    col1, col2 = st.columns(2)
    col1.metric("Total revenue", f"${total_revenue:,.2f}")
    col2.metric("Total orders", f"{total_orders:,}")


def main():
    st.set_page_config(page_title="Ecommerce Dashboard", layout="wide")
    st.title("Ecommerce Data Pipeline Dashboard")

    st.markdown(
        "This dashboard displays key metrics from the cleaned ecommerce dataset."
    )

    data_source = get_dashboard_data_source()
    using_bigquery = data_source == "bigquery"

    if data_source == "bigquery":
        daily = load_bigquery_data()
    else:
        local_path = Path(PROCESSED_FILE)
        if data_source == "local" or local_path.exists():
            df = load_local_data()
            df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
            df["InvoiceDateOnly"] = df["InvoiceDate"].dt.date
            daily = df.groupby("InvoiceDateOnly").agg(
                total_orders=("InvoiceNo", "nunique"),
                total_revenue=("TotalPrice", "sum"),
                total_quantity=("Quantity", "sum"),
            ).reset_index()
        else:
            daily = load_bigquery_data()
            using_bigquery = True

    country_revenue = None
    if not using_bigquery:
        country_revenue = df.groupby("Country")["TotalPrice"].sum().sort_values(ascending=False).head(10)

    build_tiles(daily if using_bigquery else df)

    col1, col2 = st.columns(2)

    with col1:
        if using_bigquery:
            st.subheader("Daily Orders")
            st.bar_chart(
                daily.set_index("order_date")["total_orders"].rename("Orders")
            )
        else:
            st.subheader("Revenue by Country (Top 10)")
            st.bar_chart(country_revenue)

    with col2:
        st.subheader("Daily Revenue Trend")
        st.line_chart(
            daily.set_index("order_date" if using_bigquery else "InvoiceDateOnly")["total_revenue"].rename("Revenue")
        )

    with st.expander("Daily summary table"):
        sort_column = "order_date" if using_bigquery else "InvoiceDateOnly"
        st.dataframe(daily.sort_values(sort_column, ascending=False).head(50))

    st.sidebar.markdown("## Notes")
    if using_bigquery:
        st.sidebar.markdown(
            "- Data source: BigQuery aggregate table\n"
            f"- Table: `{BIGQUERY_PROJECT}.{BIGQUERY_DATASET}.{BIGQUERY_AGG_TABLE}`\n"
            "- Runtime: container/cloud friendly mode"
        )
    else:
        st.sidebar.markdown(
            "- Data source: `data/processed_data.csv`\n"
            "- Run `python src/ingestion/processing/clean_data.py` to refresh data."
        )


if __name__ == "__main__":
    main()
