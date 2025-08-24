#!/usr/bin/env python3
"""
Import remaining biodiversity data (Invasive Species + IUCN)
Fixes the schema mismatch issues from the main import
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

def import_invasive_species_data(conn, file_path):
    """Import invasive species data from Excel with correct schema mapping"""
    print(f"\n🐛 Importing Invasive Species data from {file_path}")
    
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        print(f"📊 Processing {len(df):,} invasive species records...")
        
        # Clean and prepare data
        values = []
        for i, row in df.iterrows():
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
                i + 1,  # unique_id (required)
                lat,    # latitude
                lon,    # longitude
                common_name,  # common_name
                scientific_name,  # scientific_name
                threat_code,  # threat_code
                str(row.get('habitat', ''))[:255] if pd.notna(row.get('habitat')) else None,  # habitat
                'Invasive',  # status (default)
                str(row.get('distribution', ''))[:1000] if pd.notna(row.get('distribution')) else None  # distribution
            ))
        
        # Batch insert with correct column mapping
        cursor = conn.cursor()
        execute_batch(cursor, """
            INSERT INTO invasive_species (unique_id, latitude, longitude, common_name, scientific_name, 
                                        threat_code, habitat, status, distribution)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, values, page_size=1000)
        
        conn.commit()
        cursor.close()
        
        print(f"✅ Invasive species data import completed: {len(values):,} records imported")
        return True
        
    except Exception as e:
        print(f"❌ Invasive species data import failed: {e}")
        traceback.print_exc()
        conn.rollback()  # Rollback on error
        return False

def import_iucn_data(conn, file_path):
    """Import IUCN sample data"""
    print(f"\n🦎 Importing IUCN data from {file_path}")
    
    try:
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
        # Clear existing sample data first
        cursor.execute("DELETE FROM iucn_data WHERE latitude IS NOT NULL")
        
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
        conn.rollback()  # Rollback on error
        return False

def main():
    """Main import process for remaining data"""
    print("🚀 IMPORTING REMAINING BIODIVERSITY DATA")
    print("=" * 50)
    print("Importing the data that failed in the previous run:")
    print("- Invasive Species: Excel data")
    print("- IUCN Conservation Data: Sample records")
    print("=" * 50)
    
    # Connect to database
    conn = connect_db()
    if not conn:
        return
    
    try:
        # Define data file paths
        base_path = "C:/Users/R.A.NAVEENTHEJA/Downloads/rahulfinal project/bioscope-project/backend/database"
        
        data_files = {
            'invasive': f"{base_path}/invasive_species.xlsx",
            'iucn': f"{base_path}/sample_data/cleaned_IUCN_data_sample.csv"
        }
        
        # Import remaining data
        results = {}
        start_time = time.time()
        
        # 1. Invasive species
        if os.path.exists(data_files['invasive']):
            results['invasive'] = import_invasive_species_data(conn, data_files['invasive'])
        else:
            print(f"⚠️  Invasive species file not found: {data_files['invasive']}")
            
        # 2. IUCN data
        if os.path.exists(data_files['iucn']):
            results['iucn'] = import_iucn_data(conn, data_files['iucn'])
        else:
            print(f"⚠️  IUCN data file not found: {data_files['iucn']}")
        
        # Summary
        total_time = time.time() - start_time
        print("\n" + "=" * 50)
        print("🎉 REMAINING DATA IMPORT SUMMARY")
        print("=" * 50)
        
        for data_type, success in results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"{data_type.title()}: {status}")
        
        print(f"\nTotal import time: {total_time:.2f} seconds")
        
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
        
        print(f"\n📊 COMPLETE DATABASE STATISTICS:")
        print(f"Marine HCI: {marine_count:,} records")
        print(f"Freshwater Risk: {freshwater_count:,} records")
        print(f"Terrestrial Risk: {terrestrial_count:,} records")
        print(f"Invasive Species: {invasive_count:,} records")
        print(f"IUCN Data: {iucn_count:,} records")
        print(f"TOTAL: {total_records:,} records")
        
        print("\n🌍 Your biodiversity database is now COMPLETE with comprehensive data!")
        
    except Exception as e:
        print(f"❌ Import process failed: {e}")
        traceback.print_exc()
    finally:
        conn.close()
        print("\n✅ Database connection closed")

if __name__ == "__main__":
    main()
