
import pandas as pd
from sqlalchemy import create_engine

# Database credentials
db_host = 'localhost'
db_name = 'postgres'  # Change if needed
db_user = 'postgres'        # Replace with your PostgreSQL username
db_password = 'password.'  # Replace with your PostgreSQL password

# PostgreSQL connection string
conn_str = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_engine(conn_str)

# Load the data
excel_path = 'invasive_species.xlsx'  # Path to the Excel file
df = pd.read_excel(excel_path)

# Rename columns to match PostgreSQL conventions (lowercase, no spaces)
df.columns = [col.lower().replace(" ", "_") for col in df.columns]

# Insert data into PostgreSQL
try:
    df.to_sql('invasive_species', engine, if_exists='replace', index=False)
    print("Data successfully inserted into PostgreSQL.")
except Exception as e:
    print(f"Error: {e}")
