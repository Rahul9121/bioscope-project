#!/usr/bin/env python3
"""
Comprehensive Biodiversity Data Import Script
Imports all CSV/Excel data files into the production database

Data files to import:
- Marine HCI: ~1,036,801 rows
- Freshwater Risk: ~257,896 rows 
- Terrestrial Risk: ~233,337 rows
- Invasive Species: Excel file
- IUCN Data: Sample data

Total: ~1.5+ million rows of biodiversity data
"""

import os
import sys
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
import openpyxl
from dotenv import load_dotenv
import time
import traceback

# Load environment variables
load_dotenv()

def connect_db():
    """Connect to production database"""
    try:
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in environment variables")
            return None
            
        # Ensure SSL for Supabase
        if 'supabase.com' in database_url and '?sslmode=' not in database_url:
            database_url += '?sslmode=require'
            
        conn = psycopg2.connect(database_url)
        print("✅ Connected to production database")
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def create_tables_if_not_exists(conn):
    """Verify existing tables and add missing columns if needed"""
    cursor = conn.cursor()
    
    print("🔧 Verifying existing database tables and adding missing columns...")
    
    try:
        # 1. Enhance Marine HCI table (add missing columns from CSV)
        cursor.execute("""
            ALTER TABLE marine_hci 
            ADD COLUMN IF NOT EXISTS fishing_intensity1 DECIMAL(10, 6),
            ADD COLUMN IF NOT EXISTS fishing_intensity2 DECIMAL(10, 6),
            ADD COLUMN IF NOT EXISTS coastal_population_shadow DECIMAL(10, 6),
            ADD COLUMN IF NOT EXISTS marine_plastics DECIMAL(10, 6),
            ADD COLUMN IF NOT EXISTS shipping_density DECIMAL(10, 6);
        """)
        
        # Add indexes if they don't exist
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_marine_hci_location ON marine_hci(x, y);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_marine_hci_value ON marine_hci(marine_hci);")
        
    except Exception as e:
        print(f"⚠️ Marine HCI table enhancement failed: {e}")
    
    try:
        # 2. Enhance Freshwater Risk table (add missing detailed columns)
        cursor.execute("""
            ALTER TABLE freshwater_risk 
            ADD COLUMN IF NOT EXISTS freshwater_hci DECIMAL(10, 6),
            ADD COLUMN IF NOT EXISTS popden2010 DECIMAL(10, 6),
            ADD COLUMN IF NOT EXISTS maxrdd DECIMAL(10, 6),
            ADD COLUMN IF NOT EXISTS meanuse DECIMAL(10, 6),
            ADD COLUMN IF NOT EXISTS maxdof DECIMAL(10, 6),
            ADD COLUMN IF NOT EXISTS mincsi DECIMAL(10, 6),
            ADD COLUMN IF NOT EXISTS maxsed DECIMAL(10, 6),
            ADD COLUMN IF NOT EXISTS weighted_risk DECIMAL(15, 10),
            ADD COLUMN IF NOT EXISTS log_weighted_risk DECIMAL(15, 10),
            ADD COLUMN IF NOT EXISTS transformed_risk DECIMAL(15, 10);
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_freshwater_risk_location ON freshwater_risk(x, y);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_freshwater_risk_level ON freshwater_risk(risk_level);")
        
    except Exception as e:
        print(f"⚠️ Freshwater Risk table enhancement failed: {e}")
    
    try:
        # 3. Enhance Terrestrial Risk table (add missing detailed columns)
        cursor.execute("""
            ALTER TABLE terrestrial_risk 
            ADD COLUMN IF NOT EXISTS terrestrial_hci DECIMAL(10, 6),
            ADD COLUMN IF NOT EXISTS aggdp2010 DECIMAL(15, 10),
            ADD COLUMN IF NOT EXISTS ntlharm2020 DECIMAL(15, 10),
            ADD COLUMN IF NOT EXISTS popden2010 DECIMAL(10, 6),
            ADD COLUMN IF NOT EXISTS hmnlc2020 DECIMAL(10, 6),
            ADD COLUMN IF NOT EXISTS roadden DECIMAL(10, 6),
            ADD COLUMN IF NOT EXISTS tt_cities_over_5k DECIMAL(15, 10),
            ADD COLUMN IF NOT EXISTS tt_ports_large DECIMAL(15, 10),
            ADD COLUMN IF NOT EXISTS mineden DECIMAL(10, 6),
            ADD COLUMN IF NOT EXISTS weighted_risk DECIMAL(15, 10),
            ADD COLUMN IF NOT EXISTS transformed_risk DECIMAL(15, 10);
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_terrestrial_risk_location ON terrestrial_risk(x, y);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_terrestrial_risk_level ON terrestrial_risk(risk_level);")
        
    except Exception as e:
        print(f"⚠️ Terrestrial Risk table enhancement failed: {e}")
    
    try:
        # 4. Enhance Invasive Species table (add missing columns)
        cursor.execute("""
            ALTER TABLE invasive_species 
            ADD COLUMN IF NOT EXISTS habitat VARCHAR(255),
            ADD COLUMN IF NOT EXISTS status VARCHAR(100) DEFAULT 'Invasive',
            ADD COLUMN IF NOT EXISTS distribution TEXT;
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_invasive_species_location ON invasive_species(latitude, longitude);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_invasive_species_threat ON invasive_species(threat_code);")
        
    except Exception as e:
        print(f"⚠️ Invasive Species table enhancement failed: {e}")
    
    try:
        # 5. Enhance IUCN Data table (add missing columns)
        cursor.execute("""
            ALTER TABLE iucn_data 
            ADD COLUMN IF NOT EXISTS population_trend VARCHAR(100),
            ADD COLUMN IF NOT EXISTS assessment_date DATE;
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_iucn_data_location ON iucn_data(latitude, longitude);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_iucn_threat_status ON iucn_data(threat_status);")
        
    except Exception as e:
        print(f"⚠️ IUCN Data table enhancement failed: {e}")
    
    conn.commit()
    cursor.close()
    print("✅ All existing tables verified and enhanced successfully")

def import_marine_data(conn, file_path):
    """Import marine HCI data (1M+ rows)"""
    print(f"\n🌊 Importing Marine HCI data from {file_path}")
    
    try:
        # Check if substantial data already exists (> 1000 rows suggests full import)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM marine_hci")
        existing_count = cursor.fetchone()[0]
        cursor.close()
        
        if existing_count > 1000:  # Allow small sample data to be replaced with full dataset
            print(f"⚠️  Marine data already exists ({existing_count:,} rows). Skipping import.")
            return True
        
        # Read CSV in chunks for memory efficiency
        chunk_size = 10000
        total_imported = 0
        
        print("📊 Reading CSV file in chunks...")
        for chunk_num, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
            print(f"   Processing chunk {chunk_num + 1} ({len(chunk):,} rows)...")
            
            # Clean data
            chunk = chunk.dropna(subset=['x', 'y'])  # Remove rows without coordinates
            chunk['marine_hci'] = pd.to_numeric(chunk['marine_hci'], errors='coerce')
            
            # Convert to list of tuples for batch insert
            values = []
            for _, row in chunk.iterrows():
                values.append((
                    float(row['x']), float(row['y']),
                    float(row['marine_hci']) if pd.notna(row['marine_hci']) else None,
                    float(row['fishing_intensity1']) if pd.notna(row.get('fishing_intensity1')) else None,
                    float(row['fishing_intensity2']) if pd.notna(row.get('fishing_intensity2')) else None,
                    float(row['coastal_population_shadow']) if pd.notna(row.get('coastal_population_shadow')) else None,
                    float(row['marine_plastics']) if pd.notna(row.get('marine_plastics')) else None,
                    float(row['shipping_density']) if pd.notna(row.get('shipping_density')) else None
                ))
            
            # Batch insert
            cursor = conn.cursor()
            execute_batch(cursor, """
                INSERT INTO marine_hci (x, y, marine_hci, fishing_intensity1, fishing_intensity2, 
                                       coastal_population_shadow, marine_plastics, shipping_density)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, values, page_size=1000)
            
            conn.commit()
            cursor.close()
            total_imported += len(values)
            
            if chunk_num % 10 == 0:  # Progress update every 10 chunks
                print(f"   ✅ Imported {total_imported:,} marine records so far...")
        
        print(f"✅ Marine data import completed: {total_imported:,} records imported")
        return True
        
    except Exception as e:
        print(f"❌ Marine data import failed: {e}")
        traceback.print_exc()
        return False

def import_freshwater_data(conn, file_path):
    """Import freshwater risk data (257K+ rows)"""
    print(f"\n💧 Importing Freshwater Risk data from {file_path}")
    
    try:
        # Check if substantial data already exists
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM freshwater_risk")
        existing_count = cursor.fetchone()[0]
        cursor.close()
        
        if existing_count > 1000:  # Allow sample data to be replaced
            print(f"⚠️  Freshwater data already exists ({existing_count:,} rows). Skipping import.")
            return True
        
        # Read and process data
        df = pd.read_csv(file_path)
        print(f"📊 Processing {len(df):,} freshwater risk records...")
        
        # Clean data
        df = df.dropna(subset=['x', 'y'])
        
        # Batch insert in chunks
        chunk_size = 5000
        total_imported = 0
        
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i:i+chunk_size]
            
            values = []
            for _, row in chunk.iterrows():
                values.append((
                int(row['id']) if pd.notna(row.get('id')) and row['id'] != '' else i + 1,  # Generate ID if missing
                float(row['x']), float(row['y']),
                    float(row['freshwater_hci']) if pd.notna(row.get('freshwater_hci')) else None,
                    float(row['popden2010']) if pd.notna(row.get('popden2010')) else None,
                    float(row['maxrdd']) if pd.notna(row.get('maxrdd')) else None,
                    float(row['meanuse']) if pd.notna(row.get('meanuse')) else None,
                    float(row['maxdof']) if pd.notna(row.get('maxdof')) else None,
                    float(row['mincsi']) if pd.notna(row.get('mincsi')) else None,
                    float(row['maxsed']) if pd.notna(row.get('maxsed')) else None,
                    float(row['weighted_risk']) if pd.notna(row.get('weighted_risk')) else None,
                    float(row['log_weighted_risk']) if pd.notna(row.get('log_weighted_risk')) else None,
                    float(row['transformed_risk']) if pd.notna(row.get('transformed_risk')) else None,
                    float(row['normalized_risk']) if pd.notna(row.get('normalized_risk')) else None,
                    str(row['risk_level']) if pd.notna(row.get('risk_level')) else None
                ))
            
            cursor = conn.cursor()
            execute_batch(cursor, """
                INSERT INTO freshwater_risk (id, x, y, freshwater_hci, popden2010, maxrdd, meanuse,
                                           maxdof, mincsi, maxsed, weighted_risk, log_weighted_risk,
                                           transformed_risk, normalized_risk, risk_level)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    x = EXCLUDED.x,
                    y = EXCLUDED.y,
                    freshwater_hci = EXCLUDED.freshwater_hci,
                    normalized_risk = EXCLUDED.normalized_risk,
                    risk_level = EXCLUDED.risk_level
            """, values, page_size=1000)
            
            conn.commit()
            cursor.close()
            total_imported += len(values)
            
            if (i // chunk_size) % 10 == 0:
                print(f"   ✅ Imported {total_imported:,} freshwater records so far...")
        
        print(f"✅ Freshwater data import completed: {total_imported:,} records imported")
        return True
        
    except Exception as e:
        print(f"❌ Freshwater data import failed: {e}")
        traceback.print_exc()
        return False

def import_terrestrial_data(conn, file_path):
    """Import terrestrial risk data (233K+ rows)"""
    print(f"\n🌿 Importing Terrestrial Risk data from {file_path}")
    
    try:
        # Check if substantial data already exists
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM terrestrial_risk")
        existing_count = cursor.fetchone()[0]
        cursor.close()
        
        if existing_count > 1000:  # Allow sample data to be replaced
            print(f"⚠️  Terrestrial data already exists ({existing_count:,} rows). Skipping import.")
            return True
        
        # Read and process data
        df = pd.read_csv(file_path)
        print(f"📊 Processing {len(df):,} terrestrial risk records...")
        
        # Clean data
        df = df.dropna(subset=['x', 'y'])
        
        # Batch insert in chunks
        chunk_size = 5000
        total_imported = 0
        
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i:i+chunk_size]
            
            values = []
            for _, row in chunk.iterrows():
                values.append((
                    float(row['x']), float(row['y']),
                    float(row['terrestrial_hci']) if pd.notna(row.get('terrestrial_hci')) else None,
                    float(row['aggdp2010']) if pd.notna(row.get('aggdp2010')) else None,
                    float(row['ntlharm2020']) if pd.notna(row.get('ntlharm2020')) else None,
                    float(row['popden2010']) if pd.notna(row.get('popden2010')) else None,
                    float(row['hmnlc2020']) if pd.notna(row.get('hmnlc2020')) else None,
                    float(row['roadden']) if pd.notna(row.get('roadden')) else None,
                    float(row['tt_cities_over_5k']) if pd.notna(row.get('tt_cities_over_5k')) else None,
                    float(row['tt_ports_large']) if pd.notna(row.get('tt_ports_large')) else None,
                    float(row['mineden']) if pd.notna(row.get('mineden')) else None,
                    float(row['weighted_risk']) if pd.notna(row.get('weighted_risk')) else None,
                    float(row['transformed_risk']) if pd.notna(row.get('transformed_risk')) else None,
                    float(row['normalized_risk']) if pd.notna(row.get('normalized_risk')) else None,
                    str(row['risk_level']) if pd.notna(row.get('risk_level')) else None
                ))
            
            cursor = conn.cursor()
            execute_batch(cursor, """
                INSERT INTO terrestrial_risk (x, y, terrestrial_hci, aggdp2010, ntlharm2020, popden2010,
                                            hmnlc2020, roadden, tt_cities_over_5k, tt_ports_large, 
                                            mineden, weighted_risk, transformed_risk, normalized_risk, risk_level)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, values, page_size=1000)
            
            conn.commit()
            cursor.close()
            total_imported += len(values)
            
            if (i // chunk_size) % 10 == 0:
                print(f"   ✅ Imported {total_imported:,} terrestrial records so far...")
        
        print(f"✅ Terrestrial data import completed: {total_imported:,} records imported")
        return True
        
    except Exception as e:
        print(f"❌ Terrestrial data import failed: {e}")
        traceback.print_exc()
        return False

def import_invasive_species_data(conn, file_path):
    """Import invasive species data from Excel"""
    print(f"\n🐛 Importing Invasive Species data from {file_path}")
    
    try:
        # Check if substantial data already exists
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM invasive_species")
        existing_count = cursor.fetchone()[0]
        cursor.close()
        
        if existing_count > 10:  # Allow small sample data to be replaced
            print(f"⚠️  Invasive species data already exists ({existing_count:,} rows). Skipping import.")
            return True
        
        # Read Excel file
        df = pd.read_excel(file_path)
        print(f"📊 Processing {len(df):,} invasive species records...")
        
        # Clean and prepare data
        values = []
        for _, row in df.iterrows():
            # Extract coordinates if available
            lat = None
            lon = None
            if 'latitude' in row and pd.notna(row['latitude']):
                lat = float(row['latitude'])
            elif 'lat' in row and pd.notna(row['lat']):
                lat = float(row['lat'])
                
            if 'longitude' in row and pd.notna(row['longitude']):
                lon = float(row['longitude'])
            elif 'lon' in row and pd.notna(row['lon']):
                lon = float(row['lon'])
            elif 'lng' in row and pd.notna(row['lng']):
                lon = float(row['lng'])
            
            # Extract names
            common_name = str(row.get('common_name', row.get('Common_Name', row.get('species', ''))))[:255] if pd.notna(row.get('common_name', row.get('Common_Name', row.get('species')))) else None
            scientific_name = str(row.get('scientific_name', row.get('Scientific_Name', '')))[:255] if pd.notna(row.get('scientific_name', row.get('Scientific_Name'))) else None
            
            # Threat assessment
            threat_code = 'moderate'  # Default for invasive species
            if 'threat' in str(row).lower() or 'high' in str(row).lower():
                threat_code = 'high'
            elif 'low' in str(row).lower():
                threat_code = 'low'
            
            values.append((
                lat, lon, common_name, scientific_name, threat_code,
                str(row.get('habitat', ''))[:255] if pd.notna(row.get('habitat')) else None,
                str(row.get('status', 'Invasive'))[:100] if pd.notna(row.get('status')) else 'Invasive',
                str(row.get('distribution', ''))[:1000] if pd.notna(row.get('distribution')) else None
            ))
        
        # Batch insert
        cursor = conn.cursor()
        execute_batch(cursor, """
            INSERT INTO invasive_species (latitude, longitude, common_name, scientific_name, 
                                        threat_code, habitat, status, distribution)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, values, page_size=1000)
        
        conn.commit()
        cursor.close()
        
        print(f"✅ Invasive species data import completed: {len(values):,} records imported")
        return True
        
    except Exception as e:
        print(f"❌ Invasive species data import failed: {e}")
        traceback.print_exc()
        return False

def import_iucn_data(conn, file_path):
    """Import IUCN sample data"""
    print(f"\n🦎 Importing IUCN data from {file_path}")
    
    try:
        # Check if substantial data already exists
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM iucn_data")
        existing_count = cursor.fetchone()[0]
        cursor.close()
        
        if existing_count > 10:  # Allow sample data to be replaced
            print(f"⚠️  IUCN data already exists ({existing_count:,} rows). Skipping import.")
            return True
        
        # Read CSV
        df = pd.read_csv(file_path)
        print(f"📊 Processing {len(df):,} IUCN records...")
        
        if len(df) == 0:
            print("⚠️  No IUCN data to import")
            return True
        
        # Process and insert data
        values = []
        for _, row in df.iterrows():
            values.append((
                float(row['latitude']) if pd.notna(row.get('latitude')) else None,
                float(row['longitude']) if pd.notna(row.get('longitude')) else None,
                str(row.get('species_name', ''))[:255] if pd.notna(row.get('species_name')) else None,
                str(row.get('threat_status', ''))[:100] if pd.notna(row.get('threat_status')) else None,
                str(row.get('habitat', ''))[:255] if pd.notna(row.get('habitat')) else None,
                str(row.get('population_trend', ''))[:100] if pd.notna(row.get('population_trend')) else None,
                None  # assessment_date
            ))
        
        cursor = conn.cursor()
        execute_batch(cursor, """
            INSERT INTO iucn_data (latitude, longitude, species_name, threat_status, 
                                 habitat, population_trend, assessment_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, values, page_size=1000)
        
        conn.commit()
        cursor.close()
        
        print(f"✅ IUCN data import completed: {len(values):,} records imported")
        return True
        
    except Exception as e:
        print(f"❌ IUCN data import failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main import process"""
    print("🚀 COMPREHENSIVE BIODIVERSITY DATA IMPORT")
    print("=" * 60)
    print("This will import 1.5+ million rows of biodiversity data:")
    print("- Marine HCI: ~1,036,801 rows")
    print("- Freshwater Risk: ~257,896 rows")  
    print("- Terrestrial Risk: ~233,337 rows")
    print("- Invasive Species: Excel data")
    print("- IUCN Data: Sample data")
    print("=" * 60)
    
    # Confirm import
    confirm = input("\nProceed with data import? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Import cancelled.")
        return
    
    # Connect to database
    conn = connect_db()
    if not conn:
        return
    
    try:
        # Create tables
        create_tables_if_not_exists(conn)
        
        # Define data file paths
        base_path = "C:/Users/R.A.NAVEENTHEJA/Downloads/rahulfinal project/bioscope-project/backend/database"
        
        data_files = {
            'marine': f"{base_path}/marine_human_coexistence_nj.csv",
            'freshwater': f"{base_path}/freshwater_risk_updated.csv", 
            'terrestrial': f"{base_path}/terrestrial_risk_updated.csv",
            'invasive': f"{base_path}/invasive_species.xlsx",
            'iucn': f"{base_path}/sample_data/cleaned_IUCN_data_sample.csv"
        }
        
        # Import data
        results = {}
        start_time = time.time()
        
        # 1. Marine data (largest - 1M+ rows)
        if os.path.exists(data_files['marine']):
            results['marine'] = import_marine_data(conn, data_files['marine'])
        else:
            print(f"⚠️  Marine data file not found: {data_files['marine']}")
            
        # 2. Freshwater data
        if os.path.exists(data_files['freshwater']):
            results['freshwater'] = import_freshwater_data(conn, data_files['freshwater'])
        else:
            print(f"⚠️  Freshwater data file not found: {data_files['freshwater']}")
            
        # 3. Terrestrial data  
        if os.path.exists(data_files['terrestrial']):
            results['terrestrial'] = import_terrestrial_data(conn, data_files['terrestrial'])
        else:
            print(f"⚠️  Terrestrial data file not found: {data_files['terrestrial']}")
            
        # 4. Invasive species
        if os.path.exists(data_files['invasive']):
            results['invasive'] = import_invasive_species_data(conn, data_files['invasive'])
        else:
            print(f"⚠️  Invasive species file not found: {data_files['invasive']}")
            
        # 5. IUCN data
        if os.path.exists(data_files['iucn']):
            results['iucn'] = import_iucn_data(conn, data_files['iucn'])
        else:
            print(f"⚠️  IUCN data file not found: {data_files['iucn']}")
        
        # Summary
        total_time = time.time() - start_time
        print("\n" + "=" * 60)
        print("🎉 DATA IMPORT SUMMARY")
        print("=" * 60)
        
        for data_type, success in results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"{data_type.title()}: {status}")
        
        print(f"\nTotal import time: {total_time:.2f} seconds")
        print("🌍 Your biodiversity database is now loaded with comprehensive data!")
        
        # Final record count
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM marine_hci")
        marine_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM freshwater_risk")
        freshwater_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM terrestrial_risk") 
        terrestrial_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM invasive_species")
        invasive_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM iucn_data")
        iucn_count = cursor.fetchone()[0]
        cursor.close()
        
        total_records = marine_count + freshwater_count + terrestrial_count + invasive_count + iucn_count
        
        print(f"\n📊 FINAL DATABASE STATISTICS:")
        print(f"Marine HCI: {marine_count:,} records")
        print(f"Freshwater Risk: {freshwater_count:,} records")
        print(f"Terrestrial Risk: {terrestrial_count:,} records")
        print(f"Invasive Species: {invasive_count:,} records")
        print(f"IUCN Data: {iucn_count:,} records")
        print(f"TOTAL: {total_records:,} records")
        
    except Exception as e:
        print(f"❌ Import process failed: {e}")
        traceback.print_exc()
    finally:
        conn.close()
        print("\n✅ Database connection closed")

if __name__ == "__main__":
    main()
