import pandas as pd
from sqlalchemy import create_engine

# Define the path for your SQLite database
database_path = './data/your_database.db'

# Create an engine that connects to the SQLite database
engine = create_engine(f'sqlite:///{database_path}')

# Read the Excel file
file_path = '~/Documents/GMAT阅读/开发/数据表导出/学生做题结果数据库.xlsx'
excel_data = pd.read_excel(file_path, sheet_name=0)  # Read the first sheet

# Display the first few rows to verify the data
print(excel_data.head())

# Preprocess timedelta columns
timedelta_columns = ['耗时', '倒计时', '暂停时间', '做题时间进度', '理论做题时间进度']  # Replace with your actual timedelta column names

def convert_timedelta(value):
    if pd.isnull(value):
        return None
    if isinstance(value, pd.Timedelta):
        return value.total_seconds()
    try:
        # Attempt to parse string as timedelta
        parsed_value = pd.to_timedelta(value)
        return parsed_value.total_seconds()
    except (ValueError, TypeError):
        return None

for col in timedelta_columns:
    if col in excel_data.columns:
        excel_data[col] = excel_data[col].apply(convert_timedelta)

# Import data into the database
table_name = '学生做题结果数据库'  # Replace with your actual table name
excel_data.to_sql(table_name, con=engine, if_exists='replace', index=False)

print(f"Data imported successfully into table '{table_name}'!")
