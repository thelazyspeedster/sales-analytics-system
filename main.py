from utils.file_handler import read_sales_file

def main():
    raw_data = read_sales_file("data/sales_data.txt")
    print(raw_data)    

if __name__ == "__main__":
    main()