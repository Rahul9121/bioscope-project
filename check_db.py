import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cursor = conn.cursor()

print('🔍 Checking table structures...\n')

# Check invasive_species table
cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'invasive_species' ORDER BY ordinal_position;")
print('📊 Invasive Species Table Structure:')
for row in cursor.fetchall():
    print(f'  {row[0]}: {row[1]}')

# Get row counts for main tables
print('\n📈 Current Database Statistics:')
cursor.execute("SELECT COUNT(*) FROM marine_hci")
print(f'  Marine HCI: {cursor.fetchone()[0]:,} records')

cursor.execute("SELECT COUNT(*) FROM freshwater_risk") 
print(f'  Freshwater Risk: {cursor.fetchone()[0]:,} records')

cursor.execute("SELECT COUNT(*) FROM terrestrial_risk")
print(f'  Terrestrial Risk: {cursor.fetchone()[0]:,} records')

cursor.execute("SELECT COUNT(*) FROM invasive_species")
print(f'  Invasive Species: {cursor.fetchone()[0]:,} records')

cursor.execute("SELECT COUNT(*) FROM iucn_data")
print(f'  IUCN Data: {cursor.fetchone()[0]:,} records')

cursor.close()
conn.close()
print('\n✅ Database check completed!')
