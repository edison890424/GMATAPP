import pandas as pd
from sqlalchemy import create_engine

# Define the path for your SQLite database
database_path = './data/your_database.db'

# Create an engine that connects to the SQLite database
engine = create_engine(f'sqlite:///{database_path}')

# Read the Excel file again for comparison
file_path = '~/Documents/GMAT阅读/开发/数据表导出/题目数据库.xlsx'
excel_data = pd.read_excel(file_path, sheet_name=0)  # Read the first sheet

# Fetch data from the database
table_name = '题目数据库'  # Replace with your actual table name
db_data = pd.read_sql_table(table_name, con=engine)

# Compare the number of records
excel_record_count = len(excel_data)
db_record_count = len(db_data)

print(f"Excel record count: {excel_record_count}")
print(f"Database record count: {db_record_count}")

if excel_record_count == db_record_count:
    print("Record counts match!")
else:
    print("Record counts do not match!")

# Spot-check sample records
sample_size = 5
excel_sample = excel_data.sample(sample_size)
db_sample = db_data.sample(sample_size)

print("\nExcel sample records:")
print(excel_sample)

print("\nDatabase sample records:")
print(db_sample)

# Automated check for data integrity
mismatched_rows = (excel_data != db_data).sum().sum()
if mismatched_rows == 0:
    print("All data matches between Excel and database!")
else:
    print(f"Found {mismatched_rows} mismatched data points between Excel and database.")
