def read_sales_file(file_path):
    records = []

    try:
        with open(file_path, "r", encoding="latin-1") as file:
            for line in file:
                line = line.strip()
                if line:
                    records.append(line)
    except FileNotFoundError:
        print("Sales data file not found.")

    return records

def parse_transactions(raw_lines):
    transactions = []

    # Skip header
    for line in raw_lines[1:]:
        parts = line.split("|")

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        transaction_id, date, product_id, product_name, quantity, price, customer_id, region = parts

        # Remove commas from ProductName
        product_name = product_name.replace(",", "")

        try:
            quantity = int(quantity.replace(",", ""))
            unit_price = float(price.replace(",", ""))
        except ValueError:
            continue

        transactions.append({
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        })

    return transactions

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid_transactions = []
    invalid_count = 0

    total_input = len(transactions)
    filtered_by_region = 0
    filtered_by_amount = 0

    regions = sorted(set(t["Region"] for t in transactions if t.get("Region")))
    amounts = [
        t["Quantity"] * t["UnitPrice"]
        for t in transactions
        if isinstance(t.get("Quantity"), int) and isinstance(t.get("UnitPrice"), float)
    ]

    print(f"Regions: {', '.join(regions)}")
    if amounts:
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

    apply_filter = input("\nDo you want to filter data? (y/n): ").strip().lower()

    if apply_filter == "y":
        region_input = input("Enter region (or press Enter to skip): ").strip()
        region = region_input if region_input else None

        min_amount = parse_amount_input("Enter minimum amount (or press Enter to skip): ")
        max_amount = parse_amount_input("Enter maximum amount (or press Enter to skip): ")

    for t in transactions:
        required_fields = [
            "TransactionID", "ProductID", "CustomerID",
            "Quantity", "UnitPrice", "Region"
        ]

        if not all(t.get(field) for field in required_fields):
            invalid_count += 1
            continue

        if not (
            t["TransactionID"].startswith("T") and
            t["ProductID"].startswith("P") and
            t["CustomerID"].startswith("C")
        ):
            invalid_count += 1
            continue

        if t["Quantity"] <= 0 or t["UnitPrice"] <= 0:
            invalid_count += 1
            continue

        amount = t["Quantity"] * t["UnitPrice"]

        if region and t["Region"] != region:
            filtered_by_region += 1
            continue

        if min_amount and amount < min_amount:
            filtered_by_amount += 1
            continue

        if max_amount and amount > max_amount:
            filtered_by_amount += 1
            continue

        valid_transactions.append(t)

    filter_summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(valid_transactions)
    }

    print(f"Total records parsed: {total_input}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {total_input - invalid_count}")

    return valid_transactions, invalid_count, filter_summary

def parse_amount_input(prompt):
    value = input(prompt).strip()

    if not value:
        return None

    try:
        amount = float(value.replace(",", ""))
        if amount < 0:
            print("Amount cannot be negative. Ignoring filter.")
            return None
        return amount
    except ValueError:
        print("Invalid amount entered. Ignoring filter.")
        return None
