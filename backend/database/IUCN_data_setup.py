import pandas as pd
from sqlalchemy import create_engine
import psycopg2

# 🔹 Database credentials
db_host = 'localhost'
db_name = 'postgres'  # Change if needed
db_user = 'postgres'        # Replace with your PostgreSQL username
db_password = 'password.'  # Replace with your PostgreSQL password

# 🔹 PostgreSQL connection string
conn_str = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_engine(conn_str)

# 🔹 Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host
)
cur = conn.cursor()

# 🔹 Step 1: Create Table If It Does Not Exist
create_table_query = """
CREATE TABLE IF NOT EXISTS iucn_data (
    id SERIAL PRIMARY KEY,
    species_name TEXT,
    genus TEXT,
    family TEXT,
    threat_status TEXT,
    latitude FLOAT,
    longitude FLOAT,
    locality TEXT
);
"""
cur.execute(create_table_query)
conn.commit()
print("✅ Table 'iucn_data' created successfully!")

# 🔹 Step 2: Load the Cleaned CSV Data
csv_path = 'cleaned_IUCN_data.csv'  # Update with your actual file path
df = pd.read_csv(csv_path)

# 🔹 Rename columns to match PostgreSQL naming conventions
df.columns = [col.lower().replace(" ", "_") for col in df.columns]

# 🔹 Fix column names: Rename 'Endangered' to 'threat_status'
df.rename(columns={"endangered": "threat_status"}, inplace=True)

# 🔹 Step 3: Keep Only Columns That Exist in PostgreSQL
valid_columns = ["species_name", "genus", "family", "threat_status", "latitude", "longitude", "locality"]


# 🔹 Filter DataFrame to only include these columns
df = df[valid_columns]

# 🔹 Step 4: Insert Data into PostgreSQL
try:
    df.to_sql('iucn_data', engine, if_exists='append', index=False)
    conn.commit()  # ✅ Ensure changes are saved
    print("✅ Data successfully inserted and committed to PostgreSQL.")
except Exception as e:
    print(f"❌ Error: {e}")

# 🔹 Close Connection
cur.close()
conn.close()
print("✅ PostgreSQL connection closed.")
