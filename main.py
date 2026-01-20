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
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # [1/10] Read sales data
        print("\n[1/10] Reading sales data...")
        raw_data = read_sales_file("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_data) - 1} transactions")

        # [2/10] Parse data
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_data)
        print(f"✓ Parsed {len(transactions)} records")

        # [3/10] Show filter options and [4/10] Validate transactions
        valid_transactions, invalid_count, summary = validate_and_filter(transactions)
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")

        # [5/10] Perform analyses
        print("\n[5/10] Analyzing sales data...")
        print("Total Revenue:\n" , calculate_total_revenue(valid_transactions))
        print("Region-wise Sales:\n", region_wise_sales(valid_transactions))
        print("Top Selling Products:\n", top_selling_products(valid_transactions))
        print("Customer Purchase Analysis:\n", customer_analysis(valid_transactions))
        print("Daily Sales Trend:\n", daily_sales_trend(valid_transactions))
        print("Peak Sales Day:\n", find_peak_sales_day(valid_transactions))
        print("Low Performing Products:\n", low_performing_products(valid_transactions))
        print("✓ Analysis complete")

        # [6/10] Fetch API products
        print("\n[6/10] Fetching product data from API...")
        products = fetch_all_products()
        print(f"✓ Fetched {len(products)} products")

        # [7/10] Enrich data
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(products)
        enriched_data = enrich_sales_data(valid_transactions, product_mapping)

        enriched_count = sum(1 for t in enriched_data if t["API_Match"])
        success_rate = (enriched_count / len(enriched_data)) * 100 if enriched_data else 0
        print(f"✓ Enriched {enriched_count}/{len(enriched_data)} transactions ({success_rate:.1f}%)")

        # [8/10] Save enriched data
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_data)
        print("✓ Saved to: data/enriched_sales_data.txt")

        # [9/10] Generate report
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_data)
        print("✓ Report saved to: output/sales_report.txt")

        # [10/10] Done
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n❌ An error occurred during execution.")
        print(f"Details: {e}")
        print("Please check input files, API availability, or configuration.")

if __name__ == "__main__":
    main()
