# dbt Transformations

This optional dbt project mirrors the SQL transformations used by the Python pipeline so the repository can demonstrate a transformation layer with a dedicated analytics tool.

## Models

- `stg_clean_orders`: cleans and standardizes the raw BigQuery orders table
- `fct_daily_sales_summary`: aggregates daily revenue, quantity, order count, and unique customers

## How to run

1. Install dbt for BigQuery in your environment.
2. Copy `dbt/profiles.yml.example` into your local dbt profiles directory and update the project, dataset, and keyfile path.
3. Update `dbt/models/schema.yml` so the source points to your BigQuery project and dataset.
4. Run:

   ```bash
   dbt debug
   dbt run
   dbt test
   ```

The dbt models use partitioning and clustering settings that match the warehouse optimization choices described in the main README.
