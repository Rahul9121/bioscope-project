#!/usr/bin/env python3
"""
Test transaction pooler connection from Supabase
"""

import psycopg2

# From your screenshot: Transaction pooler
config = {
    "host": "aws-0-us-east-2.pooler.supabase.com",
    "port": 6543,
    "user": "postgres.fxxxwgomogyzafrvrjio", 
    "password": "rahul@9121",
    "dbname": "postgres"
}

print("🧪 Testing transaction pooler connection...")
print(f"Host: {config['host']}:{config['port']}")
print(f"User: {config['user']}")
print(f"Database: {config['dbname']}")

try:
    # Test with different connection modes
    for mode in ["", "?sslmode=require", "?sslmode=prefer"]:
        print(f"\n🔍 Testing with SSL mode: {mode or 'default'}")
        
        try:
            if mode:
                conn = psycopg2.connect(
                    host=config['host'],
                    port=config['port'], 
                    user=config['user'],
                    password=config['password'],
                    dbname=config['dbname'],
                    sslmode=mode.split('=')[1]
                )
            else:
                conn = psycopg2.connect(**config)
            
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"   ✅ SUCCESS! Connected with {mode or 'default'}")
            print(f"   📊 Version: {version[0][:50]}...")
            cursor.close()
            conn.close()
            print(f"\n🎉 Working configuration found!")
            break
            
        except Exception as e:
            print(f"   ❌ Failed with {mode or 'default'}: {e}")
            continue
    else:
        print(f"\n❌ All connection attempts failed.")
        print("The password might be incorrect or the project might be paused.")
        
except Exception as e:
    print(f"❌ Unexpected error: {e}")

print("\n💡 Suggestions:")
print("1. Check if your Supabase project is active (not paused)")
print("2. Try resetting your database password in Supabase dashboard")
print("3. Use a simpler password without special characters")
print("4. Verify the project reference ID is correct")
