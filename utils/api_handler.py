import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    """
    url = "https://dummyjson.com/products?limit=120"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        formatted_products = [
            {
                "id": p.get("id"),
                "title": p.get("title"),
                "category": p.get("category"),
                "brand": p.get("brand"),
                "price": p.get("price"),
                "rating": p.get("rating"),
            }
            for p in products
        ]

        print(f"Successfully fetched {len(formatted_products)} products from API.")
        return formatted_products

    except requests.RequestException as e:
        print(f"Failed to fetch products from API: {e}")
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    """
    product_mapping = {}

    for product in api_products:
        product_id = product.get("id")
        if product_id is None:
            continue

        product_mapping[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating"),
        }

    return product_mapping

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """
    enriched_transactions = []

    for t in transactions:
        enriched = t.copy()

        api_category = None
        api_brand = None
        api_rating = None
        api_match = False

        try:
            # Extract numeric ID from ProductID (e.g., P101 -> 101)
            product_id_str = t.get("ProductID", "")
            numeric_id = int(product_id_str.replace("P", ""))

            if numeric_id in product_mapping:
                api_info = product_mapping[numeric_id]
                api_category = api_info.get("category")
                api_brand = api_info.get("brand")
                api_rating = api_info.get("rating")
                api_match = True

        except Exception:
            api_match = False

        enriched.update({
            "API_Category": api_category,
            "API_Brand": api_brand,
            "API_Rating": api_rating,
            "API_Match": api_match
        })

        enriched_transactions.append(enriched)

    save_enriched_data(enriched_transactions)

    print(f"Enriched {len(enriched_transactions)} transactions.")
    return enriched_transactions

def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file
    """
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w") as file:
        file.write("|".join(headers) + "\n")

        for t in enriched_transactions:
            row = [
                str(t.get("TransactionID", "NULL")),
                str(t.get("Date", "NULL")),
                str(t.get("ProductID", "NULL")),
                str(t.get("ProductName", "NULL")),
                str(t.get("Quantity", "NULL")),
                str(t.get("UnitPrice", "NULL")),
                str(t.get("CustomerID", "NULL")),
                str(t.get("Region", "NULL")),
                str(t.get("API_Category") or "NULL"),
                str(t.get("API_Brand") or "NULL"),
                str(t.get("API_Rating") or "NULL"),
                str(t.get("API_Match"))
            ]

            file.write("|".join(row) + "\n")

    print(f"Enriched data saved to {filename}")
