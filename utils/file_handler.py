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
