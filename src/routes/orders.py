from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_db_connection


orders_bp = Blueprint(
    "orders",
    __name__,
    url_prefix="/orders"
)


@orders_bp.route("/")
def order_list():
    connection = get_db_connection()

    orders = connection.execute(
        """
        SELECT
            o.order_id,
            o.order_date,
            o.status,
            c.first_name,
            c.last_name,
            COALESCE(
                SUM(oi.quantity * oi.unit_price),
                0
            ) AS order_total
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        LEFT JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY
            o.order_id,
            o.order_date,
            o.status,
            c.first_name,
            c.last_name
        ORDER BY o.order_date DESC
        """
    ).fetchall()

    connection.close()

    return render_template(
        "orders.html",
        orders=orders
    )


@orders_bp.route("/create", methods=["GET", "POST"])
def create_order():
    connection = get_db_connection()

    customers = connection.execute(
        """
        SELECT
            customer_id,
            first_name,
            last_name
        FROM customers
        ORDER BY last_name, first_name
        """
    ).fetchall()

    products = connection.execute(
        """
        SELECT
            product_id,
            name,
            price,
            stock
        FROM products
        ORDER BY name
        """
    ).fetchall()

    if request.method == "POST":

        customer_id = request.form.get("customer_id", "").strip()
        product_ids = request.form.getlist("product_id[]")
        quantities = request.form.getlist("quantity[]")

        errors = []

        # -----------------------------
        # Validate customer
        # -----------------------------

        if not customer_id:
            errors.append("Please select a customer.")
        else:
            customer = connection.execute(
                """
                SELECT customer_id
                FROM customers
                WHERE customer_id = ?
                """,
                (customer_id,)
            ).fetchone()

            if customer is None:
                errors.append("Selected customer does not exist.")

        # -----------------------------
        # Validate order items
        # -----------------------------

        if not product_ids:
            errors.append("Please add at least one product.")

        if len(product_ids) != len(quantities):
            errors.append("Invalid order item data.")

        items = []

        if len(product_ids) == len(quantities):

            seen_products = set()

            for product_id, quantity in zip(product_ids, quantities):

                if not product_id:
                    errors.append("Please select a product.")
                    continue

                # Prevent the same product being added twice
                if product_id in seen_products:
                    errors.append(
                        "The same product cannot be added more than once."
                    )
                    continue

                seen_products.add(product_id)

                try:
                    quantity_value = int(quantity)

                    if quantity_value <= 0:
                        errors.append(
                            "Quantity must be greater than zero."
                        )
                        continue

                except ValueError:
                    errors.append(
                        "Quantity must be a whole number."
                    )
                    continue

                product = connection.execute(
                    """
                    SELECT
                        product_id,
                        name,
                        price,
                        stock
                    FROM products
                    WHERE product_id = ?
                    """,
                    (product_id,)
                ).fetchone()

                if product is None:
                    errors.append(
                        "One of the selected products does not exist."
                    )
                    continue

                if quantity_value > product["stock"]:
                    errors.append(
                        f'Not enough stock for "{product["name"]}". '
                        f'Available stock: {product["stock"]}.'
                    )
                    continue

                items.append(
                    {
                        "product_id": product["product_id"],
                        "name": product["name"],
                        "quantity": quantity_value,
                        "price": product["price"]
                    }
                )

        # -----------------------------
        # If validation failed
        # -----------------------------

        if errors:
            connection.close()

            flash("Order was not created.")

            return render_template(
                "create_order.html",
                customers=customers,
                products=products,
                form=request.form,
                errors=errors
            )

        # -----------------------------
        # Create order transaction
        # -----------------------------

        try:

            connection.execute("BEGIN")

            # Create the order
            cursor = connection.execute(
                """
                INSERT INTO orders
                    (customer_id, status)
                VALUES
                    (?, ?)
                """,
                (
                    customer_id,
                    "Completed"
                )
            )

            order_id = cursor.lastrowid

            # Create order items and reduce stock
            for item in items:

                connection.execute(
                    """
                    INSERT INTO order_items
                        (order_id, product_id, quantity, unit_price)
                    VALUES
                        (?, ?, ?, ?)
                    """,
                    (
                        order_id,
                        item["product_id"],
                        item["quantity"],
                        item["price"]
                    )
                )

                # Stock-safe update
                cursor = connection.execute(
                    """
                    UPDATE products
                    SET stock = stock - ?
                    WHERE product_id = ?
                      AND stock >= ?
                    """,
                    (
                        item["quantity"],
                        item["product_id"],
                        item["quantity"]
                    )
                )

                if cursor.rowcount != 1:
                    raise ValueError(
                        f'Not enough stock for "{item["name"]}".'
                    )

            # Everything succeeded
            connection.commit()

            connection.close()

            flash(
                f"Order #{order_id} created successfully."
            )

            return redirect(
                url_for("orders.order_list")
            )

        except Exception as error:

            # Something failed:
            # undo the entire transaction
            connection.rollback()
            connection.close()

            flash(
                f"Order could not be created: {error}"
            )

            return redirect(
                url_for("orders.create_order")
            )

    # GET request

    connection.close()

    return render_template(
        "create_order.html",
        customers=customers,
        products=products,
        form={},
        errors=[]
    )
@orders_bp.route("/<int:order_id>")
def order_details(order_id):
    connection = get_db_connection()

    order = connection.execute(
        """
        SELECT
            o.order_id,
            o.order_date,
            o.status,
            c.first_name,
            c.last_name,
            c.email,
            c.phone
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        WHERE o.order_id = ?
        """,
        (order_id,)
    ).fetchone()

    if order is None:
        connection.close()
        return "Order not found", 404

    items = connection.execute(
        """
        SELECT
            p.name AS product_name,
            oi.quantity,
            oi.unit_price,
            oi.quantity * oi.unit_price AS line_total
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        WHERE oi.order_id = ?
        ORDER BY p.name
        """,
        (order_id,)
    ).fetchall()

    order_total = connection.execute(
        """
        SELECT
            COALESCE(
                SUM(quantity * unit_price),
                0
            ) AS order_total
        FROM order_items
        WHERE order_id = ?
        """,
        (order_id,)
    ).fetchone()["order_total"]

    connection.close()

    return render_template(
        "order_details.html",
        order=order,
        items=items,
        order_total=order_total
    )