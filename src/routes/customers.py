from flask import Blueprint, render_template, request
from database import get_db_connection


customers_bp = Blueprint(
    "customers",
    __name__,
    url_prefix="/customers"
)


@customers_bp.route("/")
def customer_list():
    connection = get_db_connection()

    customer_filter = request.args.get("filter", "all")

    query = """
        SELECT
            c.customer_id,
            c.first_name,
            c.last_name,
            c.email,
            c.phone,
            c.created_at,
            COUNT(DISTINCT o.order_id) AS order_count,
            COALESCE(
                SUM(oi.quantity * oi.unit_price),
                0
            ) AS total_spent
        FROM customers c
        LEFT JOIN orders o
            ON c.customer_id = o.customer_id
        LEFT JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY
            c.customer_id,
            c.first_name,
            c.last_name,
            c.email,
            c.phone,
            c.created_at
    """

    if customer_filter == "with_orders":
        query += """
            HAVING COUNT(DISTINCT o.order_id) > 0
        """

    elif customer_filter == "without_orders":
        query += """
            HAVING COUNT(DISTINCT o.order_id) = 0
        """

    query += """
        ORDER BY c.last_name ASC, c.first_name ASC
    """

    customers = connection.execute(query).fetchall()

    connection.close()

    return render_template(
        "customers.html",
        customers=customers,
        selected_filter=customer_filter
    )


@customers_bp.route("/<int:customer_id>")
def customer_detail(customer_id):
    connection = get_db_connection()

    customer = connection.execute(
        """
        SELECT
            customer_id,
            first_name,
            last_name,
            email,
            phone,
            created_at
        FROM customers
        WHERE customer_id = ?
        """,
        (customer_id,)
    ).fetchone()

    if customer is None:
        connection.close()
        return "Customer not found", 404

    orders = connection.execute(
        """
        SELECT
            o.order_id,
            o.order_date,
            SUM(oi.quantity * oi.unit_price) AS order_total
        FROM orders o
        JOIN order_items oi
            ON o.order_id = oi.order_id
        WHERE o.customer_id = ?
        GROUP BY
            o.order_id,
            o.order_date
        ORDER BY o.order_date DESC
        """,
        (customer_id,)
    ).fetchall()

    total_spent = connection.execute(
        """
        SELECT
            COALESCE(
                SUM(oi.quantity * oi.unit_price),
                0
            ) AS total_spent
        FROM orders o
        JOIN order_items oi
            ON o.order_id = oi.order_id
        WHERE o.customer_id = ?
        """,
        (customer_id,)
    ).fetchone()["total_spent"]

    connection.close()

    return render_template(
        "customer_detail.html",
        customer=customer,
        orders=orders,
        total_spent=total_spent
    )