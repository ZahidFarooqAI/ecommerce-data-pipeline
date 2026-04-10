{{ config(
    partition_by={"field": "InvoiceDateOnly", "data_type": "date"},
    cluster_by=["Country", "CustomerID"]
) }}

select
  InvoiceNo,
  StockCode,
  Description,
  Quantity,
  InvoiceDate,
  UnitPrice,
  CustomerID,
  Country,
  Quantity * UnitPrice as TotalPrice,
  date(InvoiceDate) as InvoiceDateOnly
from {{ source('raw', 'raw_orders') }}
where Quantity > 0
  and UnitPrice >= 0
  and InvoiceDate is not null
  and CustomerID is not null
