from collections import defaultdict

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    """
    total_revenue = 0.0

    for t in transactions:
        total_revenue += t["Quantity"] * t["UnitPrice"]

    return round(total_revenue, 2)

def region_wise_sales(transactions):
    """
    Analyzes sales by region
    """
    region_data = defaultdict(lambda: {
        "total_sales": 0.0,
        "transaction_count": 0
    })

    total_revenue = calculate_total_revenue(transactions)

    for t in transactions:
        region = t["Region"]
        revenue = t["Quantity"] * t["UnitPrice"]

        region_data[region]["total_sales"] += revenue
        region_data[region]["transaction_count"] += 1

    # Calculate percentage contribution
    for region in region_data:
        sales = region_data[region]["total_sales"]
        region_data[region]["percentage"] = round(
            (sales / total_revenue) * 100, 2
        ) if total_revenue else 0.0

    # Sort by total_sales descending
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_regions

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    """
    product_data = defaultdict(lambda: {
        "quantity": 0,
        "revenue": 0.0
    })

    for t in transactions:
        product = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        product_data[product]["quantity"] += qty
        product_data[product]["revenue"] += revenue

    sorted_products = sorted(
        product_data.items(),
        key=lambda x: x[1]["quantity"],
        reverse=True
    )

    return [
        (product, data["quantity"], round(data["revenue"], 2))
        for product, data in sorted_products[:n]
    ]

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    """
    customer_data = defaultdict(lambda: {
        "total_spent": 0.0,
        "purchase_count": 0,
        "products_bought": set()
    })

    for t in transactions:
        customer = t["CustomerID"]
        revenue = t["Quantity"] * t["UnitPrice"]

        customer_data[customer]["total_spent"] += revenue
        customer_data[customer]["purchase_count"] += 1
        customer_data[customer]["products_bought"].add(t["ProductName"])

    # Final formatting
    final_data = {}

    for customer, data in customer_data.items():
        avg_order_value = (
            data["total_spent"] / data["purchase_count"]
            if data["purchase_count"] else 0.0
        )

        final_data[customer] = {
            "total_spent": round(data["total_spent"], 2),
            "purchase_count": data["purchase_count"],
            "avg_order_value": round(avg_order_value, 2),
            "products_bought": sorted(list(data["products_bought"]))
        }

    # Sort by total_spent descending
    sorted_customers = dict(
        sorted(
            final_data.items(),
            key=lambda x: x[1]["total_spent"],
            reverse=True
        )
    )

    return sorted_customers
