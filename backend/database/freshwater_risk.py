import psycopg2
import pandas as pd

# Database Connection
db_host = 'localhost'
db_name = 'name'
db_user = 'user'      # Replace with your PostgreSQL username
db_password = 'password'

def connect_db():
    return psycopg2.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        dbname=db_name
    )

# Load the computed freshwater risk data
df = pd.read_csv("freshwater_risk_updated.csv")  # Make sure this file exists

# Insert into PostgreSQL
conn = connect_db()
cursor = conn.cursor()

# Clear old data (optional)
cursor.execute("DELETE FROM freshwater_risk;")

# Insert new data
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO freshwater_risk (x, y, normalized_risk, risk_level)
        VALUES (%s, %s, %s, %s)
        """,
        (row["x"], row["y"], row["normalized_risk"], row["risk_level"])
    )

conn.commit()
cursor.close()
conn.close()

print("✅ Freshwater risk data successfully inserted into PostgreSQL!")
