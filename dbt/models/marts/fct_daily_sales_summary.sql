{{ config(
    partition_by={"field": "order_date", "data_type": "date"},
    cluster_by=["unique_customers"]
) }}

select
  InvoiceDateOnly as order_date,
  count(distinct InvoiceNo) as total_orders,
  sum(TotalPrice) as total_revenue,
  sum(Quantity) as total_quantity,
  count(distinct CustomerID) as unique_customers
from {{ ref('stg_clean_orders') }}
group by order_date
