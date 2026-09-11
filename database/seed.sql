PRAGMA foreign_keys = ON;

-- ==========================================
-- CLEAR EXISTING DATA
-- ==========================================

DELETE FROM order_items;
DELETE FROM orders;
DELETE FROM products;
DELETE FROM customers;
DELETE FROM categories;


-- ==========================================
-- CATEGORIES (5)
-- ==========================================

INSERT INTO categories (category_id, name) VALUES
(1, 'Electronics'),
(2, 'Computer Accessories'),
(3, 'Office Supplies'),
(4, 'Home & Lifestyle'),
(5, 'Mobile Accessories');


-- ==========================================
-- PRODUCTS (20)
-- ==========================================

INSERT INTO products
(product_id, category_id, name, description, price, stock)
VALUES
(1, 1, 'Laptop Pro 14', '14-inch professional laptop', 1299.99, 8),
(2, 1, 'Desktop PC', 'Powerful desktop computer', 999.99, 5),
(3, 1, '27-inch Monitor', '27-inch Full HD monitor', 249.99, 3),
(4, 1, 'Smart TV 50', '50-inch 4K smart television', 599.99, 2),

(5, 2, 'Wireless Mouse', 'Ergonomic wireless mouse', 29.99, 25),
(6, 2, 'Mechanical Keyboard', 'RGB mechanical keyboard', 89.99, 15),
(7, 2, 'USB-C Hub', 'Multi-port USB-C hub', 49.99, 4),
(8, 2, 'Laptop Stand', 'Adjustable aluminium laptop stand', 39.99, 10),

(9, 3, 'Notebook Pack', 'Pack of five notebooks', 12.99, 40),
(10, 3, 'Ballpoint Pens', 'Pack of ten blue pens', 7.99, 50),
(11, 3, 'Desk Organizer', 'Desktop stationery organizer', 18.99, 6),
(12, 3, 'Printer Paper', '500-sheet A4 paper pack', 8.99, 30),

(13, 4, 'Desk Lamp', 'LED adjustable desk lamp', 34.99, 12),
(14, 4, 'Office Chair', 'Ergonomic office chair', 179.99, 4),
(15, 4, 'Water Bottle', 'Reusable stainless steel bottle', 24.99, 20),
(16, 4, 'Backpack', 'Laptop-compatible backpack', 59.99, 7),

(17, 5, 'Phone Case', 'Protective smartphone case', 19.99, 30),
(18, 5, 'USB-C Charger', 'Fast USB-C wall charger', 32.99, 9),
(19, 5, 'Power Bank', '10000mAh portable power bank', 44.99, 5),
(20, 5, 'Screen Protector', 'Tempered glass screen protector', 14.99, 35);


-- ==========================================
-- CUSTOMERS (12)
-- ==========================================

INSERT INTO customers
(customer_id, first_name, last_name, email, phone)
VALUES
(1, 'Alice', 'Martin', 'alice.martin@example.com', '0600000001'),
(2, 'Bob', 'Dupont', 'bob.dupont@example.com', '0600000002'),
(3, 'Claire', 'Bernard', 'claire.bernard@example.com', '0600000003'),
(4, 'David', 'Robert', 'david.robert@example.com', '0600000004'),
(5, 'Emma', 'Petit', 'emma.petit@example.com', '0600000005'),
(6, 'Frank', 'Moreau', 'frank.moreau@example.com', '0600000006'),
(7, 'Grace', 'Laurent', 'grace.laurent@example.com', '0600000007'),
(8, 'Hugo', 'Simon', 'hugo.simon@example.com', '0600000008'),
(9, 'Isabelle', 'Michel', 'isabelle.michel@example.com', '0600000009'),
(10, 'Julien', 'Garcia', 'julien.garcia@example.com', '0600000010'),
(11, 'Karen', 'Leroy', 'karen.leroy@example.com', '0600000011'),
(12, 'Louis', 'Roux', 'louis.roux@example.com', '0600000012');


-- ==========================================
-- ORDERS (25)
-- ==========================================

INSERT INTO orders
(order_id, customer_id, order_date)
VALUES
(1, 1, '2026-01-05 10:15:00'),
(2, 2, '2026-01-12 14:30:00'),
(3, 3, '2026-01-20 09:45:00'),
(4, 4, '2026-02-03 11:20:00'),
(5, 5, '2026-02-15 16:10:00'),
(6, 6, '2026-02-25 13:40:00'),
(7, 7, '2026-03-04 10:05:00'),
(8, 8, '2026-03-18 15:25:00'),
(9, 9, '2026-03-29 12:00:00'),
(10, 10, '2026-04-07 09:30:00'),
(11, 1, '2026-04-19 14:45:00'),
(12, 2, '2026-04-27 17:20:00'),
(13, 3, '2026-05-05 10:10:00'),
(14, 4, '2026-05-16 11:35:00'),
(15, 5, '2026-05-28 15:50:00'),
(16, 6, '2026-06-06 09:15:00'),
(17, 7, '2026-06-14 13:25:00'),
(18, 8, '2026-06-23 16:40:00'),
(19, 9, '2026-07-02 10:55:00'),
(20, 10, '2026-07-11 14:05:00'),
(21, 1, '2026-07-20 11:45:00'),
(22, 2, '2026-08-01 09:20:00'),
(23, 3, '2026-08-12 15:15:00'),
(24, 4, '2026-08-22 12:35:00'),
(25, 5, '2026-08-30 16:05:00');


-- ==========================================
-- ORDER ITEMS (50+)
-- ==========================================

INSERT INTO order_items
(order_item_id, order_id, product_id, quantity, unit_price)
VALUES

(1, 1, 1, 1, 1299.99),
(2, 1, 5, 2, 29.99),

(3, 2, 6, 1, 89.99),
(4, 2, 7, 1, 49.99),

(5, 3, 9, 3, 12.99),
(6, 3, 10, 2, 7.99),

(7, 4, 2, 1, 999.99),
(8, 4, 5, 1, 29.99),

(9, 5, 3, 1, 249.99),
(10, 5, 6, 1, 89.99),

(11, 6, 14, 1, 179.99),
(12, 6, 13, 2, 34.99),

(13, 7, 18, 2, 32.99),
(14, 7, 17, 1, 19.99),

(15, 8, 4, 1, 599.99),
(16, 8, 5, 1, 29.99),

(17, 9, 8, 1, 39.99),
(18, 9, 16, 1, 59.99),

(19, 10, 19, 1, 44.99),


(21, 11, 1, 1, 1299.99),
(22, 11, 6, 1, 89.99),

(23, 12, 7, 2, 49.99),
(24, 12, 18, 1, 32.99),

(25, 13, 11, 2, 18.99),
(26, 13, 12, 3, 8.99),

(27, 14, 15, 2, 24.99),
(28, 14, 16, 1, 59.99),

(29, 15, 3, 1, 249.99),
(30, 15, 5, 2, 29.99),

(31, 16, 2, 1, 999.99),
(32, 16, 8, 1, 39.99),

(33, 17, 13, 1, 34.99),
(34, 17, 14, 1, 179.99),

(35, 18, 9, 4, 12.99),
(36, 18, 10, 5, 7.99),

(37, 19, 17, 2, 19.99),
(38, 19, 18, 1, 32.99),

(39, 20, 4, 1, 599.99),
(40, 20, 6, 1, 89.99),

(41, 21, 1, 1, 1299.99),
(42, 21, 5, 1, 29.99),

(43, 22, 19, 2, 44.99),


(45, 23, 3, 2, 249.99),
(46, 23, 7, 1, 49.99),

(47, 24, 14, 1, 179.99),
(48, 24, 16, 1, 59.99),

(49, 25, 6, 1, 89.99),
(50, 25, 18, 2, 32.99),

(51, 25, 10, 3, 7.99),
(52, 25, 13, 1, 34.99);