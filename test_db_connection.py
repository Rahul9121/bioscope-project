#!/usr/bin/env python3
"""
Quick Database Connection Test
Test your database connection before running the full setup
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2
import urllib.parse as urlparse

def load_env():
    """Load environment variables from .env file"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(env_path)
    print(f"📁 Loading environment from: {env_path}")

def test_connection():
    """Test database connection"""
    print("🔍 Testing database connection...")
    
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        return False
    
    if '[YOUR-' in database_url:
        print("❌ DATABASE_URL contains placeholder values")
        print("Please update your .env file with actual Supabase credentials")
        return False
    
    print(f"🔗 Using database URL: {database_url.replace('://postgres:', '://postgres:***@')}")
    
    try:
        # Parse database URL
        url = urlparse.urlparse(database_url)
        
        # URL decode the password
        password = urlparse.unquote(url.password) if url.password else None
        
        print(f"Parsed details:")
        print(f"  Host: {url.hostname}")
        print(f"  User: {url.username}")
        print(f"  Database: {url.path[1:]}")
        print(f"  Port: {url.port or 5432}")
        
        # Test connection
        conn = psycopg2.connect(
            host=url.hostname,
            user=url.username,
            password=password,
            dbname=url.path[1:],
            port=url.port or 5432
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ Connected successfully!")
        print(f"📊 Database version: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def main():
    print("🧪 Database Connection Test")
    print("=" * 40)
    
    # Load environment variables
    load_env()
    
    # Test connection
    if test_connection():
        print("\n✅ Database connection successful!")
        print("You can now run: python setup_production_database.py")
        return True
    else:
        print("\n❌ Database connection failed!")
        print("Please check your .env file and database credentials")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
