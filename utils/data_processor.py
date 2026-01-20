from collections import defaultdict
from datetime import datetime

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

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    """
    daily_data = defaultdict(lambda: {
        "revenue": 0.0,
        "transaction_count": 0,
        "unique_customers": set()
    })

    for t in transactions:
        date = t["Date"]
        revenue = t["Quantity"] * t["UnitPrice"]

        daily_data[date]["revenue"] += revenue
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["unique_customers"].add(t["CustomerID"])

    # Final formatting & sort by date
    formatted_data = {}

    for date in sorted(daily_data.keys()):
        formatted_data[date] = {
            "revenue": round(daily_data[date]["revenue"], 2),
            "transaction_count": daily_data[date]["transaction_count"],
            "unique_customers": len(daily_data[date]["unique_customers"])
        }

    return formatted_data

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    """
    daily_revenue = defaultdict(lambda: {
        "revenue": 0.0,
        "transaction_count": 0
    })

    for t in transactions:
        date = t["Date"]
        revenue = t["Quantity"] * t["UnitPrice"]

        daily_revenue[date]["revenue"] += revenue
        daily_revenue[date]["transaction_count"] += 1

    peak_day = max(
        daily_revenue.items(),
        key=lambda x: x[1]["revenue"]
    )

    return (
        peak_day[0],
        round(peak_day[1]["revenue"], 2),
        peak_day[1]["transaction_count"]
    )

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
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

    low_products = [
        (product, data["quantity"], round(data["revenue"], 2))
        for product, data in product_data.items()
        if data["quantity"] < threshold
    ]

    return sorted(
        low_products,
        key=lambda x: x[1]
    )

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_records = len(transactions)

    # ---------- OVERALL SUMMARY ----------
    total_revenue = calculate_total_revenue(transactions)
    total_transactions = total_records
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = [t["Date"] for t in transactions]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

    # ---------- REGION PERFORMANCE ----------
    region_stats = region_wise_sales(transactions)

    # ---------- TOP PRODUCTS ----------
    top_products = top_selling_products(transactions, n=5)

    # ---------- CUSTOMER ANALYSIS ----------
    customers = customer_analysis(transactions)
    top_customers = list(customers.items())[:5]

    # ---------- DAILY TREND ----------
    daily_trend = daily_sales_trend(transactions)

    # ---------- PRODUCT PERFORMANCE ----------
    peak_day, peak_revenue, peak_txns = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    # Average transaction value per region
    avg_region_value = {
        region: data["total_sales"] / data["transaction_count"]
        for region, data in region_stats.items()
    }

    # ---------- API ENRICHMENT SUMMARY ----------
    enriched_count = sum(1 for t in enriched_transactions if t["API_Match"])
    enrichment_rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0

    unenriched_products = sorted(
        {t["ProductName"] for t in enriched_transactions if not t["API_Match"]}
    )

    # ---------- WRITE REPORT ----------
    with open(output_file, "w", encoding="utf-8") as f:

        f.write("=" * 44 + "\n")
        f.write("           SALES ANALYTICS REPORT\n")
        f.write(f"         Generated: {now}\n")
        f.write(f"         Records Processed: {total_records}\n")
        f.write("=" * 44 + "\n\n")

        # OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        # REGION PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 44 + "\n")

        # Header
        f.write(f"{'Region':<10}{'Sales':<15}{'% of Total':<12}{'Transactions':<14}\n")

        # Rows
        for region, data in region_stats.items():
            f.write(
                f"{region:<10}"
                f"₹{data['total_sales']:<14,.0f} "
                f"{data['percentage']:<9.2f}% "
                f"{data['transaction_count']:<14}\n"
            )

        f.write("\n")

        # TOP PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Rank':<6}{'Product':<20}{'Qty':<8}{'Revenue'}\n")

        for idx, (name, qty, revenue) in enumerate(top_products, start=1):
            f.write(f"{idx:<6}{name:<20}{qty:<8}₹{revenue:,.2f}\n")

        f.write("\n")

        # TOP CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Rank':<6}{'Customer':<12}{'Spent':<15}{'Orders':<10}\n")

        for idx, (cust, data) in enumerate(top_customers, start=1):
            f.write(
                f"{idx:<6}"
                f"{cust:<12}"
                f"₹{data['total_spent']:<14.2f} "
                f"{data['purchase_count']:<10}\n"
            )


        f.write("\n")

        # DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 44 + "\n")

        # Header
        f.write(f"{'Date':<12}{'Revenue':<15}{'Txns':<8}{'Customers':<10}\n")

        # Rows
        for date, data in daily_trend.items():
            f.write(
                f"{date:<12}"
                f"₹{data['revenue']:<14,.2f} "
                f"{data['transaction_count']:<8}"
                f"{data['unique_customers']:<10}\n"
            )


        f.write("\n")

        # PRODUCT PERFORMANCE
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 44 + "\n")
        f.write(f"Best Selling Day: {peak_day} (₹{peak_revenue:,.2f}, {peak_txns} transactions)\n\n")

        if low_products:
            f.write("Low Performing Products:\n")
            for name, qty, rev in low_products:
                f.write(f"- {name}: {qty} units, ₹{rev:,.2f}\n")
        else:
            f.write("No low performing products found.\n")

        f.write("\nAverage Transaction Value per Region:\n")
        for region, value in avg_region_value.items():
            f.write(f"- {region}: ₹{value:,.2f}\n")

        f.write("\n")

        # API ENRICHMENT
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Records Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {enrichment_rate:.2f}%\n")

        if unenriched_products:
            f.write("Products Not Enriched:\n")
            for p in unenriched_products:
                f.write(f"- {p}\n")
        else:
            f.write("All products enriched successfully.\n")

    print(f"Sales report generated successfully at '{output_file}'")
