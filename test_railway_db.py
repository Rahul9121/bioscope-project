#!/usr/bin/env python3
"""
Test Railway database connection with detailed error reporting
"""
import os
import psycopg2
import urllib.parse as urlparse

def test_railway_db_connection():
    """Test the exact database connection that Railway is using"""
    
    # Use the same DATABASE_URL as Railway
    database_url = "postgresql://postgres.fxxxwgomogyzafrvrjio:rahul2002rahul@aws-0-us-east-2.pooler.supabase.com:6543/postgres"
    
    print("🧪 Testing Railway Database Connection")
    print("=" * 50)
    print(f"DATABASE_URL: {database_url}")
    
    # Parse DATABASE_URL like the app does
    try:
        url = urlparse.urlparse(database_url)
        db_config = {
            'host': url.hostname,
            'user': url.username,
            'password': url.password,
            'dbname': url.path[1:],
            'port': url.port or 5432
        }
        
        print(f"Parsed connection details:")
        print(f"  Host: {db_config['host']}")
        print(f"  User: {db_config['user']}")
        print(f"  Database: {db_config['dbname']}")
        print(f"  Port: {db_config['port']}")
        print(f"  Password: {'***' if db_config['password'] else 'None'}")
        
    except Exception as e:
        print(f"❌ Error parsing DATABASE_URL: {e}")
        return False
    
    # Test 1: Basic connection without SSL
    print("\n🔗 Test 1: Basic connection (no SSL)...")
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Basic connection successful!")
        print(f"PostgreSQL version: {version[0]}")
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Basic connection failed: {e}")
        
    # Test 2: Connection with SSL required
    print("\n🔗 Test 2: Connection with SSL required...")
    try:
        db_config['sslmode'] = 'require'
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ SSL connection successful!")
        print(f"PostgreSQL version: {version[0]}")
        
        # Test if users table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'users'
            );
        """)
        users_table_exists = cursor.fetchone()[0]
        print(f"Users table exists: {'Yes' if users_table_exists else 'No'}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ SSL connection failed: {e}")
        
    # Test 3: Connection with different SSL settings
    print("\n🔗 Test 3: Connection with prefer SSL...")
    try:
        db_config['sslmode'] = 'prefer'
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Prefer SSL connection successful!")
        print(f"PostgreSQL version: {version[0]}")
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Prefer SSL connection failed: {e}")
    
    # Test 4: With URL parameter
    print("\n🔗 Test 4: Connection using URL with SSL parameter...")
    try:
        ssl_url = database_url + "?sslmode=require"
        conn = psycopg2.connect(ssl_url)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ URL with SSL parameter connection successful!")
        print(f"PostgreSQL version: {version[0]}")
        print(f"✅ This is the working configuration!")
        print(f"✅ Use this URL: {ssl_url}")
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ URL with SSL parameter failed: {e}")
    
    return False

if __name__ == "__main__":
    success = test_railway_db_connection()
    
    if success:
        print("\n🎉 Database connection test successful!")
        print("\nFor Railway deployment, make sure to use:")
        print("DATABASE_URL=postgresql://postgres.fxxxwgomogyzafrvrjio:rahul2002rahul@aws-0-us-east-2.pooler.supabase.com:6543/postgres?sslmode=require")
    else:
        print("\n💥 All database connection tests failed!")
        print("\nTroubleshooting steps:")
        print("1. Check if Supabase project is running")
        print("2. Verify database credentials")
        print("3. Check network connectivity")
        print("4. Ensure SSL is properly configured")
