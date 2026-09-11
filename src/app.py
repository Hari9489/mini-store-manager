from flask import Flask, render_template
from database import get_db_connection
from routes.products import products_bp
from routes.customers import customers_bp
from routes.orders import orders_bp 
from routes.analytics import analytics_bp


app = Flask(__name__)
app.secret_key = "mini-store-manager-secret-key"

app.register_blueprint(products_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(analytics_bp)

@app.route("/")
def dashboard():
    connection = get_db_connection()

    # Total number of products
    product_count = connection.execute(
        "SELECT COUNT(*) AS count FROM products"
    ).fetchone()["count"]

    # Total number of customers
    customer_count = connection.execute(
        "SELECT COUNT(*) AS count FROM customers"
    ).fetchone()["count"]

    # Total number of orders
    order_count = connection.execute(
        "SELECT COUNT(*) AS count FROM orders"
    ).fetchone()["count"]

    # Total revenue
    revenue = connection.execute(
        """
        SELECT COALESCE(SUM(quantity * unit_price), 0) AS total
        FROM order_items
        """
    ).fetchone()["total"]

    # Five most recent orders
    recent_orders = connection.execute(
        """
        SELECT
            o.order_id,
            o.order_date,
            c.first_name,
            c.last_name,
            COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total
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
        ORDER BY o.order_date DESC
        LIMIT 5
        """
    ).fetchall()

    # Best-selling product by quantity
    best_selling_product = connection.execute(
        """
        SELECT
            p.product_id,
            p.name,
            SUM(oi.quantity) AS quantity_sold
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        GROUP BY p.product_id, p.name
        ORDER BY quantity_sold DESC
        LIMIT 1
        """
    ).fetchone()

    connection.close()

    return render_template(
        "dashboard.html",
        product_count=product_count,
        customer_count=customer_count,
        order_count=order_count,
        revenue=revenue,
        recent_orders=recent_orders,
        best_selling_product=best_selling_product
    )


if __name__ == "__main__":
    app.run(debug=True)