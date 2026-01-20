from utils.file_handler import (
    read_sales_file,
    parse_transactions,
    validate_and_filter
)

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    generate_sales_report
)

from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

def main():
    raw_data = read_sales_file("data/sales_data.txt")

    transactions = parse_transactions(raw_data)

    valid_transactions, invalid_count, summary = validate_and_filter(transactions)
    print(valid_transactions, invalid_count, summary)

    print("Total Revenue:\n" , calculate_total_revenue(valid_transactions))
    print("Region-wise Sales:\n", region_wise_sales(valid_transactions))
    print("Top Selling Products:\n", top_selling_products(valid_transactions))
    print("Customer Purchase Analysis:\n", customer_analysis(valid_transactions))
    print("Daily Sales Trend:\n", daily_sales_trend(valid_transactions))
    print("Peak Sales Day:\n", find_peak_sales_day(valid_transactions))
    print("Low Performing Products:\n", low_performing_products(valid_transactions))

    products = fetch_all_products()
    product_mapping = create_product_mapping(products)
    enriched_data = enrich_sales_data(valid_transactions, product_mapping)
    save_enriched_data(enriched_data)

    generate_sales_report(valid_transactions, enriched_data)

if __name__ == "__main__":
    main()
