#!/usr/bin/env python3
import os
import psycopg2
import urllib.parse as urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test database connection with detailed error reporting"""
    
    # Print environment variables (without showing sensitive info)
    database_url = os.getenv('DATABASE_URL')
    print("🔍 Checking environment variables:")
    print(f"DATABASE_URL exists: {'Yes' if database_url else 'No'}")
    
    if database_url:
        # Parse DATABASE_URL
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
    else:
        # Use individual environment variables
        db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'password'),
            'dbname': os.getenv('DB_NAME', 'postgres'),
            'port': int(os.getenv('DB_PORT', 5432))
        }
        
        print("Using individual environment variables:")
        print(f"  DB_HOST: {db_config['host']}")
        print(f"  DB_USER: {db_config['user']}")
        print(f"  DB_NAME: {db_config['dbname']}")
        print(f"  DB_PORT: {db_config['port']}")
        print(f"  DB_PASSWORD: {'***' if db_config['password'] != 'password' else 'default'}")
    
    # Test connection
    print("\n🔗 Testing database connection...")
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Connection successful!")
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
        
        if not users_table_exists:
            print("❌ Users table missing! Creating it...")
            cursor.execute("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    hotel_name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            print("✅ Users table created successfully!")
        
        # Test other required tables
        required_tables = ['invasive_species', 'iucn_data', 'freshwater_risk', 'marine_hci', 'terrestrial_risk']
        for table in required_tables:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """, (table,))
            exists = cursor.fetchone()[0]
            print(f"{table} table exists: {'Yes' if exists else 'No'}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Operational Error (connection/authentication): {e}")
        return False
    except psycopg2.DatabaseError as e:
        print(f"❌ Database Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Database Connection Test")
    print("=" * 50)
    
    success = test_database_connection()
    
    if success:
        print("\n🎉 Database connection test completed successfully!")
    else:
        print("\n💥 Database connection test failed!")
        print("\nTroubleshooting steps:")
        print("1. Check if DATABASE_URL environment variable is set correctly")
        print("2. Verify database credentials")
        print("3. Ensure database server is running and accessible")
        print("4. Check network connectivity to database host")
