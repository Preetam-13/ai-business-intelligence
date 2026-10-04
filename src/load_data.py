import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
DATABASE_URL = "postgresql+psycopg2://urluser:urlpassword@localhost:5432/ai_business_intelligence"

engine = create_engine(DATABASE_URL)

# CSV files
customers_file = "data/raw/customers.csv"
products_file = "data/raw/products.csv"
orders_file = "data/raw/orders.csv"
order_items_file = "data/raw/order_items.csv"

print("Loading CSV files...")

customers = pd.read_csv(customers_file)
products = pd.read_csv(products_file)
orders = pd.read_csv(orders_file)
order_items = pd.read_csv(order_items_file)

print(f"Customers: {len(customers):,}")
print(f"Products: {len(products):,}")
print(f"Orders: {len(orders):,}")
print(f"Order Items: {len(order_items):,}")

print("\nLoading customers...")
customers.to_sql(
    "customers",
    engine,
    if_exists="append",
    index=False,
    chunksize=5000
)

print("Loading products...")
products.to_sql(
    "products",
    engine,
    if_exists="append",
    index=False,
    chunksize=5000
)

print("Loading orders...")
orders.to_sql(
    "orders",
    engine,
    if_exists="append",
    index=False,
    chunksize=5000
)

print("Loading order items...")
order_items.to_sql(
    "order_items",
    engine,
    if_exists="append",
    index=False,
    chunksize=5000
)

print("\nData loading completed successfully!")