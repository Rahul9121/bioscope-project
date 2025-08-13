#!/usr/bin/env python3
import urllib.parse as urlparse
import os

# Test with your actual Supabase URL
database_url = "postgresql://postgres.fxxxwgomogyzafrvrjio:rahul2002rahul@aws-0-us-east-2.pooler.supabase.com:6543/postgres"

print("=== DATABASE_URL PARSING DEBUG ===")
print(f"Original URL: {database_url}")
print()

url = urlparse.urlparse(database_url)
db_config = {
    'host': url.hostname,
    'user': url.username,
    'password': url.password,
    'dbname': url.path[1:],
    'port': url.port or 5432
}

print("Parsed configuration:")
for key, value in db_config.items():
    if key == 'password':
        print(f"  {key}: {'*' * len(str(value))}")  # Hide password
    else:
        print(f"  {key}: {value}")

print()
print("SSL Configuration:")
if 'supabase.com' in db_config.get('host', ''):
    db_config['sslmode'] = 'require'
    print("  sslmode: require (added for Supabase)")
else:
    print("  sslmode: not set")

print()
print("Testing connection...")
try:
    import psycopg2
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"✅ Connection successful! PostgreSQL version: {version[0]}")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print(f"Error type: {type(e).__name__}")
