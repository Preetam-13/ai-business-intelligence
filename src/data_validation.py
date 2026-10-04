import pandas as pd
import os

DATA_DIR = "data/raw"

print("=" * 60)
print("DATA QUALITY VALIDATION")
print("=" * 60)

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

customers = pd.read_csv(f"{DATA_DIR}/customers.csv")
products = pd.read_csv(f"{DATA_DIR}/products.csv")
orders = pd.read_csv(f"{DATA_DIR}/orders.csv")
order_items = pd.read_csv(f"{DATA_DIR}/order_items.csv")


# ------------------------------------------------------------
# 1. BASIC RECORD COUNTS
# ------------------------------------------------------------

print("\n1. RECORD COUNTS")

print(f"Customers    : {len(customers):,}")
print(f"Products     : {len(products):,}")
print(f"Orders       : {len(orders):,}")
print(f"Order Items  : {len(order_items):,}")


# ------------------------------------------------------------
# 2. DUPLICATE PRIMARY KEYS
# ------------------------------------------------------------

print("\n2. DUPLICATE CHECKS")

print(
    "Duplicate customers:",
    customers["customer_id"].duplicated().sum()
)

print(
    "Duplicate products:",
    products["product_id"].duplicated().sum()
)

print(
    "Duplicate orders:",
    orders["order_id"].duplicated().sum()
)

print(
    "Duplicate order items:",
    order_items["order_item_id"].duplicated().sum()
)


# ------------------------------------------------------------
# 3. MISSING VALUES
# ------------------------------------------------------------

print("\n3. MISSING VALUES")

print("\nCustomers:")
print(customers.isnull().sum())

print("\nProducts:")
print(products.isnull().sum())

print("\nOrders:")
print(orders.isnull().sum())

print("\nOrder Items:")
print(order_items.isnull().sum())


# ------------------------------------------------------------
# 4. FOREIGN KEY VALIDATION
# ------------------------------------------------------------

print("\n4. FOREIGN KEY VALIDATION")

invalid_order_customers = (
    ~orders["customer_id"].isin(
        customers["customer_id"]
    )
).sum()

invalid_item_orders = (
    ~order_items["order_id"].isin(
        orders["order_id"]
    )
).sum()

invalid_item_products = (
    ~order_items["product_id"].isin(
        products["product_id"]
    )
).sum()

print(
    "Orders with invalid customer:",
    invalid_order_customers
)

print(
    "Order items with invalid order:",
    invalid_item_orders
)

print(
    "Order items with invalid product:",
    invalid_item_products
)


# ------------------------------------------------------------
# 5. VALUE VALIDATION
# ------------------------------------------------------------

print("\n5. VALUE VALIDATION")

print(
    "Negative quantities:",
    (order_items["quantity"] < 0).sum()
)

print(
    "Zero quantities:",
    (order_items["quantity"] == 0).sum()
)

print(
    "Negative prices:",
    (order_items["unit_price"] < 0).sum()
)

print(
    "Invalid discounts:",
    (
        (order_items["discount"] < 0)
        | (order_items["discount"] > 1)
    ).sum()
)


# ------------------------------------------------------------
# 6. DATE VALIDATION
# ------------------------------------------------------------

print("\n6. DATE VALIDATION")

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)

print(
    "Earliest order:",
    orders["order_date"].min()
)

print(
    "Latest order:",
    orders["order_date"].max()
)


# ------------------------------------------------------------
# 7. REVENUE CALCULATION VALIDATION
# ------------------------------------------------------------

print("\n7. REVENUE VALIDATION")

calculated_gross = (
    order_items["quantity"]
    * order_items["unit_price"]
)

calculated_discount = (
    calculated_gross
    * order_items["discount"]
)

calculated_net = (
    calculated_gross
    - calculated_discount
)

revenue_difference = (
    calculated_net
    - order_items["net_revenue"]
).abs()

print(
    "Revenue calculation mismatches:",
    (revenue_difference > 0.01).sum()
)


# ------------------------------------------------------------
# 8. PROFIT CALCULATION VALIDATION
# ------------------------------------------------------------

print("\n8. PROFIT VALIDATION")

calculated_cost = (
    order_items["quantity"]
    * order_items["unit_cost"]
)

calculated_profit = (
    calculated_net
    - calculated_cost
)

profit_difference = (
    calculated_profit
    - order_items["gross_profit"]
).abs()

print(
    "Profit calculation mismatches:",
    (profit_difference > 0.01).sum()
)


# ------------------------------------------------------------
# 9. BUSINESS SUMMARY
# ------------------------------------------------------------

print("\n9. BUSINESS SUMMARY")

total_revenue = order_items["net_revenue"].sum()
total_profit = order_items["gross_profit"].sum()

number_of_orders = orders["order_id"].nunique()

aov = total_revenue / number_of_orders

gross_margin = (
    total_profit / total_revenue
) * 100

print(f"Total Revenue : ₹{total_revenue:,.2f}")
print(f"Total Profit  : ₹{total_profit:,.2f}")
print(f"Orders        : {number_of_orders:,}")
print(f"AOV           : ₹{aov:,.2f}")
print(f"Gross Margin  : {gross_margin:.2f}%")


# ------------------------------------------------------------
# 10. FINAL RESULT
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("VALIDATION COMPLETE")
print("=" * 60)