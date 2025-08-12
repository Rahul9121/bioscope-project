#!/usr/bin/env python3
"""
Check database status and what data was loaded
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

def check_database():
    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url, echo=False)
    
    print("🔍 Database Status Check")
    print("=" * 40)
    
    try:
        with engine.connect() as conn:
            tables = [
                'users', 'invasive_species', 'iucn_data', 
                'freshwater_risk', 'marine_hci', 'terrestrial_risk'
            ]
            
            for table in tables:
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    print(f"✅ {table}: {count:,} records")
                except Exception as e:
                    print(f"❌ {table}: Error - {e}")
            
            print("\n🎉 Database verification complete!")
            
            # Check sample data
            print("\n📊 Sample data from largest tables:")
            
            # Show freshwater sample
            try:
                result = conn.execute(text("SELECT x, y, risk_level, normalized_risk FROM freshwater_risk LIMIT 5"))
                print("\n🌊 Freshwater Risk (first 5 rows):")
                for row in result:
                    print(f"  {row[0]}, {row[1]}: {row[2]} (risk: {row[3]})")
            except Exception as e:
                print(f"❌ Freshwater sample error: {e}")
            
            # Show terrestrial sample  
            try:
                result = conn.execute(text("SELECT x, y, risk_level, normalized_risk FROM terrestrial_risk LIMIT 5"))
                print("\n🏔️  Terrestrial Risk (first 5 rows):")
                for row in result:
                    print(f"  {row[0]}, {row[1]}: {row[2]} (risk: {row[3]})")
            except Exception as e:
                print(f"❌ Terrestrial sample error: {e}")
                
    except Exception as e:
        print(f"❌ Database check failed: {e}")

if __name__ == "__main__":
    check_database()
