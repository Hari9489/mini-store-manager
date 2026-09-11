# Mini Store Manager

## Project Overview

Mini Store Manager is a Flask-based web application backed by SQLite. It manages products, categories, customers, orders and order items.

The project was developed for the Advanced SQL Development Project.

## Technologies

- Python 3
- Flask
- SQLite
- HTML/CSS
- SQL

## Database

The database contains the following tables:

- categories
- products
- customers
- orders
- order_items

The database uses primary keys, foreign keys, NOT NULL constraints, UNIQUE constraints, and CHECK constraints.

## Application Features

### Dashboard
Provides an overview of the store, including product, customer and order information.

### Products
- View products
- Search products
- Filter by category
- Sort products
- Add products
- Edit products
- Delete products when they are not already used in an order
- Identify low-stock products

### Customers
- View customers
- Filter customers with or without orders
- View customer order history
- View customer order totals

### Orders
- Create orders
- Add multiple products to an order
- Validate available stock
- Update stock after a successful order
- View order details
- Use transactions to maintain stock consistency

### Analytics
The application provides the following SQL analyses:

A. Revenue by category  
B. Top 5 customers  
C. Products that have never been ordered  
D. Average order value and orders above average  
E. Low-stock products  
F. Sales by month  

## SQL Features Demonstrated

The project demonstrates:

- CREATE TABLE
- INSERT
- UPDATE
- DELETE
- WHERE
- INNER JOIN
- LEFT JOIN
- COUNT
- SUM
- AVG
- GROUP BY
- HAVING
- Subqueries
- Common Table Expressions (CTEs)
- NOT EXISTS
- Transactions
- Parameterized queries

## Project Structure

mini-store-manager/
├── database/
│   ├── schema.sql
│   ├── seed.sql
│   └── store.db
├── src/
│   ├── app.py
│   ├── database.py
│   ├── routes/
│   └── templates/
├── report/
│   └── report.pdf
├── .gitignore
├── README.md
└── requirements.txt
Running the Application

Create and activate a Python virtual environment, then install the required packages:

pip install -r requirements.txt

Run the application:

python src/app.py

Then open:

http://127.0.0.1:5000
Database Setup

The database schema is provided in:

database/schema.sql

The seed data is provided in:

database/seed.sql

The SQLite database is:

database/store.db
Project Deliverables
Source code
SQLite database
SQL schema
Seed data
README
Final project report
