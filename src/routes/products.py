from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_db_connection


products_bp = Blueprint("products", __name__, url_prefix="/products")


@products_bp.route("/")
def product_list():
    connection = get_db_connection()

    search = request.args.get("search", "").strip()
    category_id = request.args.get("category_id", "")
    sort = request.args.get("sort", "name")

    query = """
        SELECT
            p.product_id,
            p.name,
            p.description,
            p.price,
            p.stock,
            c.name AS category_name
        FROM products p
        JOIN categories c
            ON p.category_id = c.category_id
        WHERE 1 = 1
    """

    parameters = []

    # Search by product name
    if search:
        query += " AND p.name LIKE ?"
        parameters.append(f"%{search}%")

    # Filter by category
    if category_id:
        query += " AND p.category_id = ?"
        parameters.append(category_id)

    # Sorting
    allowed_sorts = {
        "name": "p.name ASC",
        "price_asc": "p.price ASC",
        "price_desc": "p.price DESC",
        "stock_asc": "p.stock ASC",
        "stock_desc": "p.stock DESC"
    }

    query += " ORDER BY " + allowed_sorts.get(sort, "p.name ASC")

    products = connection.execute(query, parameters).fetchall()

    categories = connection.execute(
        """
        SELECT category_id, name
        FROM categories
        ORDER BY name
        """
    ).fetchall()

    connection.close()

    return render_template(
        "products.html",
        products=products,
        categories=categories,
        search=search,
        selected_category=category_id,
        selected_sort=sort
    )
@products_bp.route("/create", methods=["GET", "POST"])
def create_product():
    connection = get_db_connection()

    categories = connection.execute(
        """
        SELECT category_id, name
        FROM categories
        ORDER BY name
        """
    ).fetchall()

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        category_id = request.form.get("category_id", "").strip()
        price = request.form.get("price", "").strip()
        stock = request.form.get("stock", "").strip()

        errors = []

        # Validate product name
        if not name:
            errors.append("Product name is required.")

        # Validate category
        if not category_id:
            errors.append("Category is required.")

        # Validate price
        try:
            price_value = float(price)

            if price_value < 0:
                errors.append("Price cannot be negative.")

        except ValueError:
            errors.append("Price must be a valid number.")
            price_value = 0

        # Validate stock
        try:
            stock_value = int(stock)

            if stock_value < 0:
                errors.append("Stock cannot be negative.")

        except ValueError:
            errors.append("Stock must be a whole number.")
            stock_value = 0

        # If there are no errors, insert the product
        if not errors:

            connection.execute(
                """
                INSERT INTO products
                    (category_id, name, description, price, stock)
                VALUES
                    (?, ?, ?, ?, ?)
                """,
                (
                    category_id,
                    name,
                    description,
                    price_value,
                    stock_value
                )
            )

            connection.commit()
            connection.close()

            return redirect(url_for("products.product_list"))

        # If validation failed
        connection.close()

        return render_template(
            "product_form.html",
            categories=categories,
            errors=errors,
            form=request.form,
            title="Add Product"
        )

    # GET request
    connection.close()

    return render_template(
        "product_form.html",
        categories=categories,
        errors=[],
        form={},
        title="Add Product"
    )
@products_bp.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    connection = get_db_connection()

    product = connection.execute(
        """
        SELECT product_id, category_id, name, description, price, stock
        FROM products
        WHERE product_id = ?
        """,
        (product_id,)
    ).fetchone()

    if product is None:
        connection.close()
        return "Product not found", 404

    categories = connection.execute(
        """
        SELECT category_id, name
        FROM categories
        ORDER BY name
        """
    ).fetchall()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        category_id = request.form.get("category_id", "").strip()
        price = request.form.get("price", "").strip()
        stock = request.form.get("stock", "").strip()

        errors = []

        if not name:
            errors.append("Product name is required.")

        if not category_id:
            errors.append("Category is required.")

        try:
            price_value = float(price)

            if price_value < 0:
                errors.append("Price cannot be negative.")

        except ValueError:
            errors.append("Price must be a valid number.")
            price_value = 0

        try:
            stock_value = int(stock)

            if stock_value < 0:
                errors.append("Stock cannot be negative.")

        except ValueError:
            errors.append("Stock must be a whole number.")
            stock_value = 0

        if not errors:
            connection.execute(
                """
                UPDATE products
                SET
                    category_id = ?,
                    name = ?,
                    description = ?,
                    price = ?,
                    stock = ?
                WHERE product_id = ?
                """,
                (
                    category_id,
                    name,
                    description,
                    price_value,
                    stock_value,
                    product_id
                )
            )

            connection.commit()
            connection.close()

            return redirect(url_for("products.product_list"))

        form = request.form

        connection.close()

        return render_template(
            "product_form.html",
            categories=categories,
            errors=errors,
            form=form,
            title="Edit Product"
        )

    form = {
        "name": product["name"],
        "description": product["description"] or "",
        "category_id": product["category_id"],
        "price": product["price"],
        "stock": product["stock"]
    }

    connection.close()

    return render_template(
        "product_form.html",
        categories=categories,
        errors=[],
        form=form,
        title="Edit Product"
    )
@products_bp.route("/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    connection = get_db_connection()

    product = connection.execute(
        """
        SELECT product_id, name
        FROM products
        WHERE product_id = ?
        """,
        (product_id,)
    ).fetchone()

    if product is None:
        connection.close()
        flash("Product not found.")
        return redirect(url_for("products.product_list"))

    # Check whether this product has been used in an order
    order_item = connection.execute(
        """
        SELECT order_item_id
        FROM order_items
        WHERE product_id = ?
        LIMIT 1
        """,
        (product_id,)
    ).fetchone()

    if order_item:
        connection.close()
        flash(
            f'Cannot delete "{product["name"]}" because it has already been used in an order.'
        )
        return redirect(url_for("products.product_list"))

    connection.execute(
        """
        DELETE FROM products
        WHERE product_id = ?
        """,
        (product_id,)
    )

    connection.commit()
    connection.close()

    flash(f'Product "{product["name"]}" deleted successfully.')

    return redirect(url_for("products.product_list"))