from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the path for your SQLite database
database_path = './data/your_database.db'

# Create an engine that connects to the SQLite database
engine = create_engine(f'sqlite:///{database_path}', echo=True)

# Create a declarative base class
Base = declarative_base()


# Define a model for each table in your database
class YourTableName(Base):
    __tablename__ = 'your_table_name'

    id = Column(Integer, primary_key=True, autoincrement=True)
    column1 = Column(Integer)  # Replace with your actual column names and types
    column2 = Column(String)
    column3 = Column(Float)

    # Add other columns as needed

    def __repr__(self):
        return f"<YourTableName(id={self.id}, column1={self.column1}, column2={self.column2}, column3={self.column3})>"


# Add more models for other tables in your database as needed

# Create all tables in the database (this does not delete existing tables)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Example of how to add a new record
new_record = YourTableName(column1=123, column2='Example', column3=45.67)
session.add(new_record)
session.commit()

# Query the database
records = session.query(YourTableName).all()
for record in records:
    print(record)
