import os
import random
import numpy as np
import pandas as pd
from faker import Faker

# ============================================================
# CONFIGURATION
# ============================================================

SEED = 42

random.seed(SEED)
np.random.seed(SEED)
fake = Faker("en_IN")
fake.seed_instance(SEED)

NUM_CUSTOMERS = 25_000
NUM_PRODUCTS = 150
NUM_ORDERS = 150_000

START_DATE = "2023-01-01"
END_DATE = "2025-12-31"

OUTPUT_DIR = "data/raw"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# BUSINESS CONFIGURATION
# ============================================================

REGIONS = {
    "North": [
        "Delhi",
        "Jaipur",
        "Lucknow",
        "Chandigarh",
    ],
    "South": [
        "Bengaluru",
        "Chennai",
        "Hyderabad",
        "Kochi",
    ],
    "East": [
        "Kolkata",
        "Bhubaneswar",
        "Guwahati",
        "Patna",
    ],
    "West": [
        "Mumbai",
        "Pune",
        "Ahmedabad",
        "Surat",
    ],
    "Central": [
        "Bhopal",
        "Indore",
        "Nagpur",
        "Raipur",
    ],
}

CATEGORIES = {
    "Electronics": [
        "Smartphones",
        "Laptops",
        "Headphones",
        "Accessories",
    ],
    "Home & Kitchen": [
        "Kitchen Appliances",
        "Furniture",
        "Cookware",
        "Home Decor",
    ],
    "Fashion": [
        "Men's Clothing",
        "Women's Clothing",
        "Footwear",
        "Accessories",
    ],
    "Beauty": [
        "Skincare",
        "Haircare",
        "Makeup",
        "Personal Care",
    ],
    "Sports": [
        "Fitness Equipment",
        "Sportswear",
        "Outdoor",
        "Team Sports",
    ],
    "Grocery": [
        "Staples",
        "Snacks",
        "Beverages",
        "Packaged Foods",
    ],
}

SALES_CHANNELS = [
    "Website",
    "Mobile App",
    "Marketplace",
    "Retail Store",
]

PAYMENT_METHODS = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash on Delivery",
]


# ============================================================
# 1. GENERATE CUSTOMERS
# ============================================================

print("Generating customers...")

customer_ids = np.arange(1, NUM_CUSTOMERS + 1)

region_names = list(REGIONS.keys())

customers = []

for customer_id in customer_ids:

    region = random.choice(region_names)
    city = random.choice(REGIONS[region])

    signup_date = fake.date_between(
        start_date="-4y",
        end_date="-30d"
    )

    age = int(np.clip(
        np.random.normal(34, 10),
        18,
        70
    ))

    gender = random.choice([
        "Male",
        "Female",
        "Other"
    ])

    # Customer segments will later be recalculated
    # using actual purchasing behavior.
    customer_segment = random.choice([
        "Consumer",
        "Small Business",
        "Enterprise"
    ])

    customers.append({
        "customer_id": customer_id,
        "customer_name": fake.name(),
        "gender": gender,
        "age": age,
        "city": city,
        "region": region,
        "customer_segment": customer_segment,
        "signup_date": signup_date,
    })

customers_df = pd.DataFrame(customers)

customers_df["signup_date"] = pd.to_datetime(
    customers_df["signup_date"]
)

print(f"Customers generated: {len(customers_df):,}")


# ============================================================
# 2. GENERATE PRODUCTS
# ============================================================

print("Generating products...")

products = []

# Flatten all category/subcategory combinations
product_types = []

for category, subcategories in CATEGORIES.items():
    for subcategory in subcategories:
        product_types.append((category, subcategory))


# Generate exactly NUM_PRODUCTS products
for product_id in range(1, NUM_PRODUCTS + 1):

    # Cycle through all category/subcategory combinations
    category, subcategory = product_types[
        (product_id - 1) % len(product_types)
    ]

    product_name = (
        f"{subcategory} "
        f"{fake.word().title()} "
        f"{product_id}"
    )

    # Different categories have different price ranges
    if category == "Electronics":
        cost = random.uniform(800, 60000)

    elif category == "Home & Kitchen":
        cost = random.uniform(300, 30000)

    elif category == "Fashion":
        cost = random.uniform(200, 10000)

    elif category == "Beauty":
        cost = random.uniform(100, 5000)

    elif category == "Sports":
        cost = random.uniform(250, 15000)

    else:
        cost = random.uniform(50, 3000)

    margin = random.uniform(0.15, 0.45)

    price = cost * (1 + margin)

    products.append({
        "product_id": product_id,
        "product_name": product_name,
        "category": category,
        "sub_category": subcategory,
        "unit_cost": round(cost, 2),
        "unit_price": round(price, 2),
    })


products_df = pd.DataFrame(products)

print(f"Products generated: {len(products_df):,}")

# ============================================================
# 3. GENERATE ORDERS
# ============================================================

print("Generating orders...")

order_ids = np.arange(1, NUM_ORDERS + 1)

# Create dates with seasonality
date_range = pd.date_range(
    START_DATE,
    END_DATE,
    freq="D"
)

# Base weights
date_weights = np.ones(len(date_range))

for i, date in enumerate(date_range):

    # Festival / holiday season
    if date.month in [10, 11, 12]:
        date_weights[i] *= 1.35

    # Summer
    elif date.month in [4, 5, 6]:
        date_weights[i] *= 1.10

    # Slightly lower demand in February
    elif date.month == 2:
        date_weights[i] *= 0.90


date_weights = date_weights / date_weights.sum()

order_dates = np.random.choice(
    date_range,
    size=NUM_ORDERS,
    p=date_weights
)

# Customers have different purchasing probabilities.
# This creates high-value customers naturally.
customer_weights = np.random.exponential(
    scale=1.0,
    size=NUM_CUSTOMERS
)

customer_weights = customer_weights / customer_weights.sum()

selected_customers = np.random.choice(
    customer_ids,
    size=NUM_ORDERS,
    p=customer_weights
)

orders = []

for i in range(NUM_ORDERS):

    customer_id = selected_customers[i]

    customer = customers_df.loc[
        customers_df["customer_id"] == customer_id
    ].iloc[0]

    region = customer["region"]

    # South and West get slightly higher order volume
    if region == "South":
        region_multiplier = 1.15

    elif region == "West":
        region_multiplier = 1.12

    elif region == "North":
        region_multiplier = 1.05

    else:
        region_multiplier = 1.0

    orders.append({
        "order_id": order_ids[i],
        "customer_id": customer_id,
        "order_date": order_dates[i],
        "region": region,
        "sales_channel": random.choice(SALES_CHANNELS),
        "payment_method": random.choice(PAYMENT_METHODS),
    })


orders_df = pd.DataFrame(orders)

orders_df["order_date"] = pd.to_datetime(
    orders_df["order_date"]
)

print(f"Orders generated: {len(orders_df):,}")


# ============================================================
# 4. GENERATE ORDER ITEMS
# ============================================================

print("Generating order items...")

order_items = []

order_item_id = 1

product_ids = products_df["product_id"].values

for _, order in orders_df.iterrows():

    # Most orders contain 1–3 products
    num_items = np.random.choice(
        [1, 2, 3, 4, 5],
        p=[0.45, 0.30, 0.15, 0.07, 0.03]
    )

    selected_products = np.random.choice(
        product_ids,
        size=num_items,
        replace=False
    )

    for product_id in selected_products:

        product = products_df.loc[
            products_df["product_id"] == product_id
        ].iloc[0]

        # Quantity distribution
        quantity = np.random.choice(
            [1, 2, 3, 4, 5],
            p=[0.60, 0.22, 0.10, 0.05, 0.03]
        )

        # Discount behavior
        discount = np.random.choice(
            [0, 0.05, 0.10, 0.15, 0.20, 0.25],
            p=[0.45, 0.20, 0.15, 0.10, 0.07, 0.03]
        )

        order_items.append({
            "order_item_id": order_item_id,
            "order_id": order["order_id"],
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": product["unit_price"],
            "unit_cost": product["unit_cost"],
            "discount": discount,
        })

        order_item_id += 1


order_items_df = pd.DataFrame(order_items)

print(
    f"Order items generated: "
    f"{len(order_items_df):,}"
)


# ============================================================
# 5. CALCULATE TRANSACTION METRICS
# ============================================================

order_items_df["gross_revenue"] = (
    order_items_df["quantity"]
    * order_items_df["unit_price"]
)

order_items_df["discount_amount"] = (
    order_items_df["gross_revenue"]
    * order_items_df["discount"]
)

order_items_df["net_revenue"] = (
    order_items_df["gross_revenue"]
    - order_items_df["discount_amount"]
)

order_items_df["total_cost"] = (
    order_items_df["quantity"]
    * order_items_df["unit_cost"]
)

order_items_df["gross_profit"] = (
    order_items_df["net_revenue"]
    - order_items_df["total_cost"]
)


# ============================================================
# 6. SAVE DATA
# ============================================================

print("Saving datasets...")

customers_df.to_csv(
    f"{OUTPUT_DIR}/customers.csv",
    index=False
)

products_df.to_csv(
    f"{OUTPUT_DIR}/products.csv",
    index=False
)

orders_df.to_csv(
    f"{OUTPUT_DIR}/orders.csv",
    index=False
)

order_items_df.to_csv(
    f"{OUTPUT_DIR}/order_items.csv",
    index=False
)


# ============================================================
# 7. DATA SUMMARY
# ============================================================

total_revenue = order_items_df["net_revenue"].sum()
total_profit = order_items_df["gross_profit"].sum()

print("\n" + "=" * 60)
print("DATA GENERATION COMPLETE")
print("=" * 60)

print(f"Customers     : {len(customers_df):,}")
print(f"Products      : {len(products_df):,}")
print(f"Orders        : {len(orders_df):,}")
print(f"Order Items   : {len(order_items_df):,}")
print(f"Revenue       : ₹{total_revenue:,.2f}")
print(f"Gross Profit  : ₹{total_profit:,.2f}")
print(
    f"Gross Margin  : "
    f"{(total_profit / total_revenue) * 100:.2f}%"
)

print("\nFiles created:")

print("data/raw/customers.csv")
print("data/raw/products.csv")
print("data/raw/orders.csv")
print("data/raw/order_items.csv")