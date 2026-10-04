DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(150) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    age INTEGER NOT NULL,
    city VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    customer_segment VARCHAR(50) NOT NULL,
    signup_date DATE NOT NULL,

    CHECK (age BETWEEN 18 AND 100)
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    sub_category VARCHAR(100) NOT NULL,
    unit_cost NUMERIC(12,2) NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,

    CHECK (unit_cost >= 0),
    CHECK (unit_price >= 0)
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    region VARCHAR(50) NOT NULL,
    sales_channel VARCHAR(50) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    unit_cost NUMERIC(12,2) NOT NULL,
    discount NUMERIC(5,4) NOT NULL,

    gross_revenue NUMERIC(14,2) NOT NULL,
    discount_amount NUMERIC(14,2) NOT NULL,
    net_revenue NUMERIC(14,2) NOT NULL,
    total_cost NUMERIC(14,2) NOT NULL,
    gross_profit NUMERIC(14,2) NOT NULL,

    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CHECK (quantity > 0),
    CHECK (discount BETWEEN 0 AND 1),
    CHECK (unit_price >= 0),
    CHECK (unit_cost >= 0),
    CHECK (gross_revenue >= 0),
    CHECK (discount_amount >= 0),
    CHECK (net_revenue >= 0),
    CHECK (total_cost >= 0)
);

CREATE INDEX idx_orders_customer
    ON orders(customer_id);

CREATE INDEX idx_orders_date
    ON orders(order_date);

CREATE INDEX idx_orders_region
    ON orders(region);

CREATE INDEX idx_order_items_order
    ON order_items(order_id);

CREATE INDEX idx_order_items_product
    ON order_items(product_id);