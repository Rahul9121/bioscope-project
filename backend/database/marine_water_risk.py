import pandas as pd
import psycopg2

# Database Connection
db_host = 'localhost'
db_name = 'postgres'  # Change if needed
db_user = 'postgres'        # Replace with your PostgreSQL username
db_password = 'password.'  # Replace with your PostgreSQL password

def connect_db():
    return psycopg2.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        dbname=db_name
    )

# Load the computed marine risk data
df = pd.read_csv("marine_risk_updated-2.csv")  # or the correct CSV filename

conn = connect_db()
cursor = conn.cursor()

# Clear previous records if needed
# Uncomment if you want to wipe old records first
# cursor.execute("DELETE FROM marine_risk;")
conn.commit()

# Insert data
for i, row in df.iterrows():
    values = tuple(row)
    if len(values) != 7:
        print(f"⚠️ Row {i} has {len(values)} values: {values}")
        continue

    cursor.execute("""
        INSERT INTO marine_risk (
            latitude, longitude, marine_hci, weighted_risk,
            transformed_risk, normalized_risk, risk_level
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, values)

conn.commit()
print("✅ Data committed to database.")

cursor.close()
conn.close()

print("✅ marine_risk table updated successfully.")
