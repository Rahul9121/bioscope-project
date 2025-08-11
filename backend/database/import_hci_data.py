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

# 🔹 Step 1: Create Tables (If Not Exists)
create_tables_query = """
CREATE TABLE IF NOT EXISTS freshwater_hci (
    id SERIAL PRIMARY KEY,
    x DOUBLE PRECISION,
    y DOUBLE PRECISION,
    freshwater_hci DOUBLE PRECISION,
    popden2010 DOUBLE PRECISION,
    maxRDD DOUBLE PRECISION,
    meanUSE DOUBLE PRECISION,
    maxDOF DOUBLE PRECISION,
    minCSI DOUBLE PRECISION,
    maxSED DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS marine_hci (
    id SERIAL PRIMARY KEY,
    x DOUBLE PRECISION,
    y DOUBLE PRECISION,
    marine_hci DOUBLE PRECISION,
    fishing_intensity1 DOUBLE PRECISION,
    fishing_intensity2 DOUBLE PRECISION,
    coastal_population_shadow DOUBLE PRECISION,
    marine_plastics DOUBLE PRECISION,
    shipping_density DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS terrestrial_hci (
    id SERIAL PRIMARY KEY,
    x DOUBLE PRECISION,
    y DOUBLE PRECISION,
    terrestrial_hci DOUBLE PRECISION,
    aggdp2010 DOUBLE PRECISION,
    ntlharm2020 DOUBLE PRECISION,
    popden2010 DOUBLE PRECISION,
    hmnlc2020 DOUBLE PRECISION,
    roadden DOUBLE PRECISION,
    tt_cities_over_5k DOUBLE PRECISION,
    tt_ports_large DOUBLE PRECISION,
    mineden DOUBLE PRECISION
);
"""
cur.execute(create_tables_query)
conn.commit()
print("✅ Tables created successfully!")

# 🔹 Step 2: Load CSV Data into Pandas DataFrames
csv_files = {
    "freshwater_hci": "freshwater_human_coexistence_nj.csv",
    "marine_hci": "marine_human_coexistence_nj.csv",
    "terrestrial_hci": "terrestrial_human_coexistence_nj.csv"
}

# 🔹 Step 3: Insert Data into PostgreSQL
for table_name, csv_path in csv_files.items():
    try:
        # Load CSV
        df = pd.read_csv(csv_path)

        # Rename columns to lowercase and replace spaces with underscores
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]

        # Insert into PostgreSQL
        df.to_sql(table_name, engine, if_exists='append', index=False)
        conn.commit()
        print(f"✅ Data successfully inserted into `{table_name}`")

    except Exception as e:
        print(f"❌ Error inserting `{table_name}`: {e}")

# 🔹 Close Connection
cur.close()
conn.close()
print("✅ PostgreSQL connection closed.")
