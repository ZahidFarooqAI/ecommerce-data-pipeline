-- Clean raw order data in BigQuery after loading from the processed CSV.
-- Replace project, dataset, and table names when executing the query.

SELECT
  InvoiceNo,
  StockCode,
  Description,
  Quantity,
  InvoiceDate,
  UnitPrice,
  CustomerID,
  Country,
  Quantity * UnitPrice AS TotalPrice,
  DATE(InvoiceDate) AS InvoiceDateOnly
FROM `{PROJECT}.{DATASET}.{TABLE}`
WHERE Quantity > 0
  AND UnitPrice >= 0
  AND InvoiceDate IS NOT NULL
  AND CustomerID IS NOT NULL;
