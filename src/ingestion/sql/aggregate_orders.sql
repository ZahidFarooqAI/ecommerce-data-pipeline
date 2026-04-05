-- Aggregate cleaned order data for dashboard consumption.
-- Replace project and dataset values when executing the query.

SELECT
  InvoiceDateOnly AS order_date,
  COUNT(DISTINCT InvoiceNo) AS total_orders,
  SUM(TotalPrice) AS total_revenue,
  SUM(Quantity) AS total_quantity,
  COUNT(DISTINCT CustomerID) AS unique_customers
FROM `{PROJECT}.{DATASET}.clean_orders`
GROUP BY order_date
ORDER BY order_date;
