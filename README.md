# sales-analytics-system

📊 Sales Analytics System

A Python-based Sales Analytics System that processes messy sales transaction data, performs comprehensive analysis, integrates external product data via API, and generates detailed business reports.

📁 Project Structure
sales-analytics-system/
│
├── main.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── sales_data.txt
│   └── enriched_sales_data.txt (generated at runtime)
│
├── output/
│   └── sales_report.txt (generated at runtime)
│
└── utils/
    ├── file_handler.py
    ├── data_processor.py
    └── api_handler.py

⚙️ Prerequisites
    - Python 3.8 or above
    - Internet connection (required for API integration)
    - pip package manager

🧪 Setup Instructions
1️⃣ Clone the Repository
git clone <your-github-repo-url>
cd sales-analytics-system

2️⃣ Create Virtual Environment
python -m venv .venv

Activate the environment:

Windows
.venv\Scripts\activate

Mac/Linux
source .venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

Note: The only external dependency is requests.

▶️ How to Run the Project

From the root directory, run:
python main.py


🧠 What Happens When You Run It
The system executes the following steps sequentially:

Reads raw sales data from data/sales_data.txt

Parses and cleans data

    Removes invalid records
    Fixes numeric formatting issues
    Cleans product names

Validates transactions

    Transaction, Product, and Customer ID checks
    Quantity and price validation
    Optional region and amount filtering (interactive)

Performs sales analytics

    Total revenue
    Region-wise sales
    Top-selling products
    Customer purchase analysis
    Daily sales trends
    Peak sales day
    Low-performing products

Fetches product data from external API

Enriches transactions with API data

Saves enriched data to data/enriched_sales_data.txt

Generates a detailed report at:

output/sales_report.txt


📄 Output Files
File	                        Description
data/enriched_sales_data.txt	Sales data enriched with API product info
output/sales_report.txt	        Comprehensive sales analytics report


🌐 External API Used

DummyJSON Products API
Endpoint: https://dummyjson.com/products

Used to enrich sales data with:

    Product category
    Brand
    Rating


🛑 Error Handling

Graceful handling of:

    Missing or malformed data
    Invalid numeric values
    API failures

Clear console messages for debugging and tracking execution progress


🧹 Ignored Files (.gitignore)

    Python cache files
    Virtual environment
    Generated enriched data
    User-specific output files


✨ Key Features

    Modular, readable Python code
    Robust data validation and cleaning
    Interactive filtering
    Business-focused analytics
    External API integration
    Professional report generation

👤 Author

Shreya K S
Sales Analytics System – Python Programming Assignment