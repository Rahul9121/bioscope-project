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

# Load the computed freshwater risk data
df = pd.read_csv("terrestrial_risk_updated.csv")  # or the correct CSV filename


conn = connect_db()
cursor = conn.cursor()



# Clear previous records if needed

#cursor.execute("DELETE FROM terrestrial_risk;")
conn.commit()

# Insert data
# Corrected insert logic for 15 columns
for i, row in df.iterrows():
    values = tuple(row)
    if len(values) != 15:
        print(f"⚠️ Row {i} has {len(values)} values: {values}")
        continue

    cursor.execute("""
        INSERT INTO terrestrial_risk (
            x, y, terrestrial_hci, aggdp2010, ntlharm2020, popden2010,
            hmnlc2020, roadden, tt_cities_over_5k, tt_ports_large,
            mineden, weighted_risk, transformed_risk,
            normalized_risk, risk_level
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, values)



conn.commit()
print("✅ Data committed to database.")



cursor.close()
conn.close()

print("✅ terrestrial_risk table updated successfully.")
