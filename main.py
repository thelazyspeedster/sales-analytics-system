from utils.file_handler import (
    read_sales_file,
    parse_transactions,
    validate_and_filter
)

def main():
    raw_data = read_sales_file("data/sales_data.txt")

    transactions = parse_transactions(raw_data)

    valid_transactions, invalid_count, summary = validate_and_filter(transactions)
    print(valid_transactions, invalid_count, summary)

if __name__ == "__main__":
    main()
