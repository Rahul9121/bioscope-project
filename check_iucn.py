import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cursor = conn.cursor()
cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'iucn_data' ORDER BY ordinal_position;")
print('IUCN table columns:')
for row in cursor.fetchall():
    print(f'  {row[0]}')
cursor.close()
conn.close()
