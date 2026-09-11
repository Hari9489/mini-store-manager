# Mini Store Manager

## Advanced SQL Development Project

A small web-based store management application developed for the Advanced SQL Development Project.

The application uses SQLite for database management and Python with Flask for the web interface. It provides product, customer, order, dashboard, and analytics functionality while demonstrating SQL concepts such as joins, aggregation, subqueries, CTEs, parameterized queries, and transactions.

---

## 1. Technologies Used

- Python 3.13.5
- Flask
- SQLite
- HTML
- CSS
- Jinja2
- Python `sqlite3` module

SQLite is used as the mandatory relational database.

---

## 2. Project Structure

```text
mini-store-manager/
│
├── database/
│   ├── schema.sql
│   ├── seed.sql
│   ├── store.db
│   ├── init_db.py
│   ├── seed_db.py
│   ├── count_data.py
│   ├── test_relationships.py
│   ├── check_db.py
│   ├── check_orders.py
│   └── add_order_status.py
│
├── src/
│   ├── app.py
│   ├── database.py
│   │
│   ├── routes/
│   │   ├── products.py
│   │   ├── customers.py
│   │   ├── orders.py
│   │   └── analytics.py
│   │
│   └── templates/
│       ├── dashboard.html
│       ├── products.html
│       ├── product_form.html
│       ├── customers.html
│       ├── customer_detail.html
│       ├── orders.html
│       ├── create_order.html
│       ├── order_details.html
│       └── analytics.html
│
├── report/
│   └── report.pdf
│
├── requirements.txt
├── README.md
└── .gitignore
3. Database Design

The database contains five main tables:

categories
products
customers
orders
order_items
Relationships
One category can contain many products.
One customer can place many orders.
One order can contain many order items.
One product can appear in many order items.
The order_items table connects orders and products and stores the quantity and unit price for each product sold.
Main Constraints

The database uses:

Primary keys
Foreign keys
NOT NULL
UNIQUE
CHECK constraints
Foreign-key enforcement

Examples:

Customer email addresses must be unique.
Product prices cannot be negative.
Product stock cannot be negative.
Order-item quantities must be greater than zero.
Order-item unit prices cannot be negative.

Foreign keys are enabled in the application using:

connection.execute("PRAGMA foreign_keys = ON")
4. Seed Data

The database contains the minimum required seed data:

Table	Records
Categories	5
Products	20
Customers	12
Orders	25
Order Items	50

The database was also checked for foreign-key violations.

Run:

python database\count_data.py

and:

python database\test_relationships.py

The relationship test should report:

Foreign key violations:
None - all foreign keys are valid.
5. Installation
5.1 Create the Virtual Environment

From the project directory:

python -m venv venv
5.2 Activate the Virtual Environment

On Windows PowerShell:

.\venv\Scripts\Activate.ps1
5.3 Install Dependencies
python -m pip install -r requirements.txt
6. Database Setup

The project includes the database schema and seed data.

The schema can be found in:

database/schema.sql

The seed data can be found in:

database/seed.sql

The database is stored in:

database/store.db

Database helper scripts are also included for initialization, seeding, counting records, and checking relationships.

7. Running the Application

Activate the virtual environment:

.\venv\Scripts\Activate.ps1

Start the Flask application:

python src\app.py

The application runs locally at:

http://127.0.0.1:5000

Open this address in a web browser.

To stop the application:

Ctrl + C

8. Application Features
8.1 Dashboard

The Dashboard provides an overview of the store.

It displays:

Number of products
Number of customers
Number of orders
Total revenue
Recent orders
Best-selling product

The dashboard uses SQL aggregate functions such as COUNT() and SUM().

8.2 Products

The Products page provides product management functionality.

Features include:

View products
Add products
Edit products
Delete products
Search products
Filter by category
Sort products
Low-stock warning

Product searches and filters use parameterized SQL queries.

Product sorting uses an allowlist of permitted sort fields rather than inserting arbitrary user input into SQL.

A product that has already been used in an order cannot be deleted. This protects existing order history.

8.3 Customers

The Customers page provides customer information and order history.

Features include:

View customers
Filter customers with orders
Filter customers without orders
View customer order history
Calculate customer order totals

The customer listing uses SQL joins, grouping, counting, and aggregation.

Customers with no orders are identified using a LEFT JOIN.

8.4 Orders

The Orders section provides order creation and order details.

When creating an order, the application:

Selects a customer.
Selects products.
Checks requested quantities.
Checks available stock.
Creates the order.
Creates the order items.
Decreases product stock.
Commits the transaction.

The order creation process uses a database transaction.

If an error occurs, the transaction is rolled back so that incomplete orders do not remain in the database.

Stock is updated using a condition that prevents the stock value from becoming negative.

Example:

UPDATE products
SET stock = stock - ?
WHERE product_id = ?
  AND stock >= ?
9. Analytics

The Analytics page contains the required SQL analyses.

A. Revenue by Category

Calculates total revenue for each product category using joins and aggregate functions.

SQL concepts demonstrated:

JOIN
LEFT JOIN
SUM()
GROUP BY
B. Top 5 Customers

Identifies the five customers who generated the highest order revenue.

SQL concepts demonstrated:

JOIN
SUM()
GROUP BY
ORDER BY
LIMIT
C. Products Never Ordered

Finds products that have never appeared in an order.

This analysis uses NOT EXISTS.

Example:

SELECT p.product_id, p.name
FROM products p
WHERE NOT EXISTS (
    SELECT 1
    FROM order_items oi
    WHERE oi.product_id = p.product_id
);

This query identifies products without matching records in order_items.

D. Average Order Value

Calculates the average order value and identifies orders whose value is above the average.

The implementation demonstrates:

AVG()
A derived subquery
A Common Table Expression (CTE)
Aggregation
E. Low Stock Products

Displays products whose stock is at or below the low-stock threshold.

The threshold is supplied as a parameter rather than being directly inserted into the SQL statement.

Example:

connection.execute(
    "... WHERE stock <= ?",
    (5,)
)
F. Sales by Month

Groups sales by month using SQLite date functions.

The analysis demonstrates:

strftime()
SUM()
GROUP BY
ORDER BY
10. SQL Concepts Demonstrated

The project demonstrates the following SQL requirements.

Database Definition
CREATE TABLE
Primary keys
Foreign keys
NOT NULL
UNIQUE
CHECK
Data Manipulation
INSERT
UPDATE
DELETE
Querying
WHERE
JOIN
LEFT JOIN
ORDER BY
GROUP BY
HAVING
Aggregate Functions
COUNT()
SUM()
AVG()
Advanced SQL
Subqueries
Common Table Expressions (WITH)
NOT EXISTS
Derived tables
Date functions
Transactions

Order creation uses:

BEGIN
INSERT order
INSERT order items
UPDATE stock
COMMIT

If an error occurs:

ROLLBACK

This ensures that order creation and stock updates are handled safely as one transaction.

11. Parameterized Queries

User-provided values are passed to SQLite using parameters.

Example:

connection.execute(
    "SELECT * FROM products WHERE name LIKE ?",
    (search_pattern,)
)

This avoids directly inserting user input into SQL statements and helps prevent SQL injection.

Parameterized queries are used throughout the application for values such as:

Search terms
Category filters
Product IDs
Customer IDs
Quantities
Low-stock thresholds
12. Testing and Validation

The project was tested using the included database checking scripts.

Check Record Counts
python database\count_data.py

Expected minimum data:

categories   : 5
products     : 20
customers    : 12
orders       : 25
order_items  : 50
Check Foreign-Key Relationships
python database\test_relationships.py

Expected result:

Foreign key violations:
None - all foreign keys are valid.
Application Testing

The following application functionality was tested:

Product creation
Product editing
Product deletion
Product search
Product category filtering
Product sorting
Low-stock warning
Customer order filtering
Customer order history
Order creation
Stock validation
Insufficient-stock error handling
Order details
Analytics A–F


13. Evaluation / Quick Test Commands

After cloning the repository, the project can be tested with:

python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python database\count_data.py
python database\test_relationships.py
python src\app.py

Then open:

http://127.0.0.1:5000