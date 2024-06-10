from sqlalchemy import create_engine, text

# Define the path for your SQLite database
database_path = './data/your_database.db'

# Create an engine that connects to the SQLite database
engine = create_engine(f'sqlite:///{database_path}')

# Name of the table to be deleted
table_name = '句子单词对应表'  # Replace with your actual table name

# Connect to the database and execute the DROP TABLE command
with engine.connect() as connection:
    connection.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
    print(f"Table '{table_name}' has been deleted successfully.")
