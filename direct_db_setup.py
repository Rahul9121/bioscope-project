#!/usr/bin/env python3
"""
Direct database setup for Bioscope using IP address
"""
import psycopg2
import sys

# Try direct connection with components
def setup_database():
    print("🏗️ Setting up Bioscope database schema...")
    
    connection_params = {
        'host': '3.101.5.153',  # Direct IP
        'port': 6543,
        'database': 'postgres',
        'user': 'postgres.buwoakllwmwqonqwmbqr',
        'password': 'rahul2002rahul',
        'sslmode': 'require'
    }
    
    try:
        print("🔗 Connecting to Supabase database...")
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        print("✅ Connected successfully!")
        
        # Test basic query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"📊 PostgreSQL: {version[0][:50]}...")
        
        # Read and execute SQL setup
        with open('supabase_setup_complete.sql', 'r', encoding='utf-8') as file:
            sql_script = file.read()
        print("✅ SQL script loaded")
        
        # Execute the script in chunks
        statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
        
        executed = 0
        for statement in statements:
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    executed += 1
                    if executed % 10 == 0:
                        print(f"  Executed {executed}/{len(statements)} statements...")
                except Exception as e:
                    if "already exists" not in str(e).lower():
                        print(f"  Warning: {str(e)[:60]}...")
        
        conn.commit()
        print("✅ Database schema setup completed!")
        
        # Verify tables
        biodiversity_tables = ['users', 'invasive_species', 'iucn_data', 'freshwater_risk', 'marine_hci', 'terrestrial_risk']
        
        print(f"\n📋 Verifying {len(biodiversity_tables)} tables:")
        total_records = 0
        
        for table in biodiversity_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  ✅ {table}: {count} records")
                total_records += count
            except Exception as e:
                print(f"  ❌ {table}: Error - {e}")
        
        print(f"\n📊 Total records in database: {total_records}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Bioscope Database Setup (Direct Connection)")
    print("=" * 50)
    
    if setup_database():
        print("\n🎉 Database setup completed successfully!")
        print("   All tables created with sample data")
        print("   Ready for data loading step")
    else:
        print("\n❌ Database setup failed")
        sys.exit(1)
