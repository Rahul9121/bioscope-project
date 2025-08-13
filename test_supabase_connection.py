#!/usr/bin/env python3
"""
Test Supabase Database Connection
This script tests if Railway can connect to your Supabase database
"""

import os
import psycopg2
import urllib.parse as urlparse
from dotenv import load_dotenv

def test_supabase_connection():
    print("🧪 Testing Supabase Database Connection")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in environment")
        return False
    
    print(f"🔗 Testing connection to: {database_url.split('@')[1] if '@' in database_url else 'unknown host'}")
    
    try:
        # Parse the database URL
        url = urlparse.urlparse(database_url)
        
        # Test connection with different configurations
        connection_configs = [
            {
                'name': 'Standard Connection',
                'config': {
                    'host': url.hostname,
                    'user': url.username,
                    'password': url.password,
                    'dbname': url.path[1:],
                    'port': url.port or 5432
                }
            },
            {
                'name': 'SSL Required Connection',
                'config': {
                    'host': url.hostname,
                    'user': url.username,
                    'password': url.password,
                    'dbname': url.path[1:],
                    'port': url.port or 5432,
                    'sslmode': 'require'
                }
            }
        ]
        
        for conn_test in connection_configs:
            print(f"\n🔍 Testing {conn_test['name']}...")
            try:
                conn = psycopg2.connect(**conn_test['config'])
                cursor = conn.cursor()
                
                # Test basic query
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                print(f"✅ Connected successfully!")
                print(f"📊 PostgreSQL version: {version[0][:50]}...")
                
                # Test users table
                cursor.execute("SELECT COUNT(*) FROM users;")
                user_count = cursor.fetchone()[0]
                print(f"👥 Users table has {user_count} records")
                
                # Test table schema
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'users'
                    ORDER BY ordinal_position;
                """)
                columns = cursor.fetchall()
                print(f"📋 Users table columns:")
                for col_name, col_type in columns:
                    print(f"   - {col_name}: {col_type}")
                
                cursor.close()
                conn.close()
                print(f"✅ {conn_test['name']} successful!")
                return True
                
            except psycopg2.OperationalError as e:
                print(f"❌ {conn_test['name']} failed: {e}")
                continue
            except Exception as e:
                print(f"❌ {conn_test['name']} failed with error: {e}")
                continue
        
        print("❌ All connection attempts failed")
        return False
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_supabase_connection()
    if success:
        print("\n🎉 Database connection successful! Your issue is likely with Railway environment variables.")
    else:
        print("\n💡 Database connection failed. Check your Supabase settings and network connectivity.")
