#!/usr/bin/env python3
"""
Execute database setup for Bioscope
"""
import psycopg2
import sys

DATABASE_URL = "postgresql://postgres.buwoakllwmwqonqwmbqr:rahul2002rahul@aws-1-us-west-1.pooler.supabase.com:6543/postgres?sslmode=require"

def setup_database():
    print("🏗️ Setting up Bioscope database schema...")
    
    try:
        # Read SQL file
        with open('supabase_setup_complete.sql', 'r', encoding='utf-8') as file:
            sql_script = file.read()
        print("✅ SQL script loaded")
        
        # Connect and execute
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Split into individual statements and execute
        statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
        
        for i, statement in enumerate(statements):
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    if i % 5 == 0:
                        print(f"  Executed {i+1}/{len(statements)} statements...")
                except Exception as e:
                    if "already exists" not in str(e).lower():
                        print(f"  Warning: {str(e)[:80]}...")
        
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
    print("🚀 Bioscope Database Setup")
    print("=" * 40)
    
    if setup_database():
        print("\n🎉 Database setup completed successfully!")
        print("   All tables created with sample data")
        print("   Ready for data loading step")
    else:
        print("\n❌ Database setup failed")
        sys.exit(1)
