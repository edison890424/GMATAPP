from sqlalchemy import create_engine, text

# Define the path for your SQLite database
database_path = './data/your_database.db'

# Create an engine that connects to the SQLite database
engine = create_engine(f'sqlite:///{database_path}')

# Define the table name
table_name = 'your_table_name'

# Define the columns to be modified and their new types
columns_to_modify = {
    'old_column1': 'new_column1 INTEGER',
    'old_column2': 'new_column2 INTEGER'
}

# Connect to the database
with engine.connect() as connection:
    # Step 1: Add new columns with the desired data types
    for old_col, new_col_def in columns_to_modify.items():
        connection.execute(text(f'''
            ALTER TABLE {table_name}
            ADD COLUMN {new_col_def}
        '''))

    # Step 2: Copy data from old columns to new columns
    for old_col, new_col_def in columns_to_modify.items():
        new_col = new_col_def.split()[0]
        connection.execute(text(f'''
            UPDATE {table_name}
            SET {new_col} = CAST({old_col} AS INTEGER)
        '''))

    # Get the list of all columns
    result = connection.execute(text(f'PRAGMA table_info({table_name})'))
    columns_info = result.fetchall()

    # Step 3: Prepare columns for the new table
    all_columns = [col[1] for col in columns_info]
    new_columns = [col for col in all_columns if col not in columns_to_modify] + [col.split()[0] for col in columns_to_modify.values()]

    # Create a temporary table with the desired structure
    connection.execute(text(f'''
        CREATE TABLE {table_name}_temp AS SELECT {', '.join(new_columns)} FROM {table_name}
    '''))

    # Drop the old table
    connection.execute(text(f'DROP TABLE {table_name}'))

    # Rename the temporary table to the original table name
    connection.execute(text(f'ALTER TABLE {table_name}_temp RENAME TO {table_name}'))

    print("Column types changed and table updated successfully.")
