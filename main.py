from utils.file_handler import (
    read_sales_file,
    parse_transactions,
    validate_and_filter
)

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis
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

if __name__ == "__main__":
    main()
