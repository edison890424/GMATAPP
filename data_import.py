import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

# Define the path for your SQLite database
database_path = './data/your_database.db'

# Create an engine that connects to the SQLite database
engine = create_engine(f'sqlite:///{database_path}')

# Read the Excel file
file_path = '~/Documents/GMAT阅读/开发/数据表导出/句子单词对应表.xlsx'
excel_data = pd.read_excel(file_path, sheet_name=0)  # Read the first sheet

# Display the first few rows to verify the data
print(excel_data.head())

# Import data into the database
table_name = '句子单词对应表'  # Replace with your actual table name
excel_data.to_sql(table_name, con=engine, if_exists='replace', index=False)

print(f"Data imported successfully into table '{table_name}'!")

