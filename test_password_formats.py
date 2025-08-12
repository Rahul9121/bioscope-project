#!/usr/bin/env python3
"""
Test different password formats for Supabase connection
"""

import psycopg2
import urllib.parse as urlparse

# Test configurations
configs = [
    {
        "name": "Original password",
        "host": "aws-0-us-east-2.pooler.supabase.com",
        "user": "postgres.fxxxwgomogyzafrvrjio",
        "password": "rahul@9121",
        "port": 6543,
        "dbname": "postgres"
    },
    {
        "name": "URL encoded password",
        "host": "aws-0-us-east-2.pooler.supabase.com", 
        "user": "postgres.fxxxwgomogyzafrvrjio",
        "password": "rahul%40rahul@9121",
        "port": 6543,
        "dbname": "postgres"
    },
    {
        "name": "Simple postgres user",
        "host": "aws-0-us-east-2.pooler.supabase.com",
        "user": "postgres",
        "password": "rahul@9121",
        "port": 6543,
        "dbname": "postgres"
    }
]

def test_config(config):
    print(f"\n🧪 Testing: {config['name']}")
    print(f"   User: {config['user']}")
    print(f"   Host: {config['host']}:{config['port']}")
    
    try:
        conn = psycopg2.connect(**{k:v for k,v in config.items() if k != 'name'})
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"   ✅ SUCCESS! Connected!")
        print(f"   📊 Version: {version[0][:50]}...")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing different password formats...")
    
    for config in configs:
        if test_config(config):
            print(f"\n🎉 Found working configuration: {config['name']}")
            break
    else:
        print(f"\n❌ None of the configurations worked.")
        print("Please check your Supabase project settings or try resetting the password.")
