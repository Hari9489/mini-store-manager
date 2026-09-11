from flask import Blueprint, render_template
from database import get_db_connection


analytics_bp = Blueprint(
    "analytics",
    __name__,
    url_prefix="/analytics"
)


@analytics_bp.route("/")
def analytics():
    connection = get_db_connection()

    # A. Revenue by Category
    revenue_by_category = connection.execute(
        """
        SELECT
            c.name AS category_name,
            COALESCE(
                SUM(oi.quantity * oi.unit_price),
                0
            ) AS revenue
        FROM categories c
        LEFT JOIN products p
            ON c.category_id = p.category_id
        LEFT JOIN order_items oi
            ON p.product_id = oi.product_id
        GROUP BY
            c.category_id,
            c.name
        ORDER BY revenue DESC
        """
    ).fetchall()


    # B. Top 5 Customers by Total Spending
    top_customers = connection.execute(
        """
        SELECT
            c.customer_id,
            c.first_name,
            c.last_name,
            c.email,
            COALESCE(
                SUM(oi.quantity * oi.unit_price),
                0
            ) AS total_spent
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY
            c.customer_id,
            c.first_name,
            c.last_name,
            c.email
        ORDER BY total_spent DESC
        LIMIT 5
        """
    ).fetchall()


    # C. Customers Who Have Never Ordered
    customers_never_ordered = connection.execute(
        """
        SELECT
            c.customer_id,
            c.first_name,
            c.last_name,
            c.email
        FROM customers c
        WHERE NOT EXISTS (
            SELECT 1
            FROM orders o
            WHERE o.customer_id = c.customer_id
        )
        ORDER BY
            c.last_name,
            c.first_name
        """
    ).fetchall()

    # D. Average Order Value + Orders Above Average
    average_order_value = connection.execute(
        """
        SELECT AVG(order_total) AS average_order_value
        FROM (
            SELECT
                o.order_id,
                COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS order_total
            FROM orders o
            LEFT JOIN order_items oi
                ON o.order_id = oi.order_id
            GROUP BY o.order_id
        )
        """
    ).fetchone()["average_order_value"]

    orders_above_average = connection.execute(
        """
        WITH order_totals AS (
            SELECT
                o.order_id,
                o.order_date,
                c.first_name,
                c.last_name,
                COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS order_total
            FROM orders o
            JOIN customers c
                ON o.customer_id = c.customer_id
            LEFT JOIN order_items oi
                ON o.order_id = oi.order_id
            GROUP BY
                o.order_id,
                o.order_date,
                c.first_name,
                c.last_name
        )
        SELECT
            order_id,
            order_date,
            first_name,
            last_name,
            order_total
        FROM order_totals
        WHERE order_total > (
            SELECT AVG(order_total)
            FROM order_totals
        )
        ORDER BY order_total DESC
        """
    ).fetchall()
            # E. Low Stock Products
    low_stock_products = connection.execute(
        """
        SELECT
            p.product_id,
            p.name,
            c.name AS category_name,
            p.stock
        FROM products p
        JOIN categories c
            ON p.category_id = c.category_id
        WHERE p.stock <= ?
        ORDER BY p.stock ASC, p.name
        """,
        (5,)
    ).fetchall()
    # F. Sales by Month
    sales_by_month = connection.execute(
        """
        SELECT
            strftime('%Y-%m', o.order_date) AS sales_month,
            ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
        FROM orders o
        JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY sales_month
        ORDER BY sales_month
        """
    ).fetchall()
    connection.close()
        


    return render_template(
        "analytics.html",
        revenue_by_category=revenue_by_category,
        top_customers=top_customers,
        customers_never_ordered=customers_never_ordered,
        average_order_value=average_order_value,
        orders_above_average=orders_above_average,
        low_stock_products=low_stock_products,
        sales_by_month=sales_by_month
    )