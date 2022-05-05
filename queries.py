"""
Queries for the Chinook_Sqlite_db.sqlite DB
"""

ALL_INVOICES_QUERY = """
SELECT TotalPaid.CustomerId ,Customer.FirstName, Customer.LastName, round(TotalPaid.total_paid, 2) as total_paid, Invoice.InvoiceDate, Invoice.Total
FROM (
	SELECT CustomerId, sum( Total) as total_paid
	from Invoice 
	GROUP BY CustomerId
	ORDER  BY total_paid DESC )AS TotalPaid
LEFT JOIN Invoice
ON TotalPaid.CustomerId = Invoice.CustomerId
LEFT JOIN Customer
ON TotalPaid.CustomerId = Customer.CustomerId;
"""

FILTERED_INVOICES_QUERY = """
SELECT TotalPaid.CustomerId ,Customer.FirstName, Customer.LastName, round(TotalPaid.total_paid, 2) as total_paid, FilteredInvoice.InvoiceDate, FilteredInvoice.Total
FROM (
	SELECT CustomerId, sum( Total) as total_paid
	from Invoice 
		WHERE  InvoiceDate BETWEEN datetime( :start )   and datetime( :end ) 
	GROUP BY CustomerId
	ORDER  BY total_paid DESC )AS TotalPaid
LEFT JOIN (
	SELECT *
	FROM Invoice 
	WHERE  InvoiceDate BETWEEN datetime( :start )   and datetime( :end ) 
) AS FilteredInvoice
ON TotalPaid.CustomerId = FilteredInvoice.CustomerId
LEFT JOIN Customer
ON TotalPaid.CustomerId = Customer.CustomerId;
"""
