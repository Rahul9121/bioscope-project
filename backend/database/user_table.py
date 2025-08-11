import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Database credentials
db_host = 'localhost'
db_name = 'postgres'  # Change if needed
db_user = 'postgres'        # Replace with your PostgreSQL username
db_password = 'password.'  # Replace with your PostgreSQL password

# PostgreSQL connection string
conn_str = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_engine(conn_str, echo=True)

# Base class for the ORM model
Base = declarative_base()

# Define the Users table model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

# Create the table in PostgreSQL
Base.metadata.create_all(engine)

print("Users table created successfully!")
