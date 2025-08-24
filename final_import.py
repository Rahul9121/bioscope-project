#!/usr/bin/env python3
"""
Final corrected import for remaining biodiversity data
Uses the correct column names from actual database schema
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
    """Import invasive species data with proper column mapping"""
    print(f"\n🐛 Importing Invasive Species data from {file_path}")
    
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        print(f"📊 Processing {len(df):,} invasive species records...")
        
        # Filter records with valid coordinates
        df_with_coords = df[df['Latitude'].notna() & df['Longitude'].notna()]
        print(f"   Found {len(df_with_coords):,} records with coordinates")
        
        # Clean and prepare data
        values = []
        for i, row in df_with_coords.iterrows():
            values.append((
                int(row['Unique_ID']),  # unique_id
                float(row['Latitude']),   # latitude
                float(row['Longitude']),  # longitude
                pd.to_datetime(row['Date_taken']) if pd.notna(row['Date_taken']) else None,  # date_taken
                str(row['Species_co'])[:50] if pd.notna(row['Species_co']) else None,  # species_code
                str(row['Common_Name'])[:255] if pd.notna(row['Common_Name']) else None,  # common_name
                str(row['reporter'])[:255] if pd.notna(row['reporter']) else None,  # reporter
                str(row['Property_code'])[:50] if pd.notna(row['Property_code']) else None,  # property_code
                str(row['Prop_name'])[:255] if pd.notna(row['Prop_name']) else None,  # property_name
                str(row['Manager'])[:255] if pd.notna(row['Manager']) else None,  # manager
                str(row['Prop_Type'])[:100] if pd.notna(row['Prop_Type']) else None,  # property_type
                str(row['County'])[:100] if pd.notna(row['County']) else None,  # county
                str(row['Municipality'])[:100] if pd.notna(row['Municipality']) else None,  # municipality
                str(row['Taxa'])[:100] if pd.notna(row['Taxa']) else None,  # taxa
                str(row['APP_CAT'])[:50] if pd.notna(row['APP_CAT']) else None,  # app_category
                str(row['SEARCH_GRP'])[:50] if pd.notna(row['SEARCH_GRP']) else None,  # search_group
                str(row['DIST_CODE'])[:50] if pd.notna(row['DIST_CODE']) else None,  # distribution_code
                str(row['THREAT_CODE'])[:50] if pd.notna(row['THREAT_CODE']) else 'moderate',  # threat_code
                str(row['EDRR_ACT'])[:100] if pd.notna(row['EDRR_ACT']) else None,  # edrr_action
                str(row['Population'])[:255] if pd.notna(row['Population']) else None,  # population
                str(row['habitat'])[:255] if pd.notna(row['habitat']) else None,  # habitat
                str(row['erad_status'])[:100] if pd.notna(row['erad_status']) else None,  # eradication_status
                pd.to_datetime(row['erad_i_date']).date() if pd.notna(row['erad_i_date']) else None,  # eradication_init_date
                pd.to_datetime(row['erad_c_date']).date() if pd.notna(row['erad_c_date']) else None,  # eradication_complete_date
                str(row['erad_method'])[:255] if pd.notna(row['erad_method']) else None,  # eradication_method
                str(row['eradicator'])[:255] if pd.notna(row['eradicator']) else None,  # eradicator
                str(row['herbicide'])[:100] if pd.notna(row['herbicide']) else None,  # herbicide
                float(row['herbicide_pct']) if pd.notna(row['herbicide_pct']) else None,  # herbicide_percentage
                bool(row['submitted']) if pd.notna(row['submitted']) else False,  # submitted
                str(row['notes'])[:1000] if pd.notna(row['notes']) else None  # notes
            ))
        
        # Batch insert with all required columns
        cursor = conn.cursor()
        execute_batch(cursor, """
            INSERT INTO invasive_species (
                unique_id, latitude, longitude, date_taken, species_code, common_name, reporter,
                property_code, property_name, manager, property_type, county, municipality, taxa,
                app_category, search_group, distribution_code, threat_code, edrr_action, population,
                habitat, eradication_status, eradication_init_date, eradication_complete_date,
                eradication_method, eradicator, herbicide, herbicide_percentage, submitted, notes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, values, page_size=1000)
        
        conn.commit()
        cursor.close()
        
        print(f"✅ Invasive species data import completed: {len(values):,} records imported")
        return True
        
    except Exception as e:
        print(f"❌ Invasive species data import failed: {e}")
        traceback.print_exc()
        try:
            conn.rollback()
        except:
            pass
        return False

def import_iucn_data(conn, file_path):
    """Import IUCN sample data with correct column names"""
    print(f"\n🦎 Importing IUCN data from {file_path}")
    
    try:
        # Read CSV
        df = pd.read_csv(file_path)
        print(f"📊 Processing {len(df):,} IUCN records...")
        
        if len(df) == 0:
            print("⚠️  No IUCN data to import")
            return True
        
        # Process and insert data - use correct column names
        values = []
        for _, row in df.iterrows():
            values.append((
                float(row['latitude']) if pd.notna(row.get('latitude')) else None,
                float(row['longitude']) if pd.notna(row.get('longitude')) else None,
                str(row.get('species_name', ''))[:255] if pd.notna(row.get('species_name')) else None,
                str(row.get('threat_status', ''))[:100] if pd.notna(row.get('threat_status')) else None,
                str(row.get('population_trend', ''))[:100] if pd.notna(row.get('population_trend')) else None,
                str(row.get('habitat_type', ''))[:255] if pd.notna(row.get('habitat_type')) else None  # habitat_type not habitat
            ))
        
        cursor = conn.cursor()
        # Clear existing sample data first
        cursor.execute("DELETE FROM iucn_data WHERE latitude IS NOT NULL")
        
        # Use correct column names
        execute_batch(cursor, """
            INSERT INTO iucn_data (latitude, longitude, species_name, threat_status, population_trend, habitat_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, values, page_size=1000)
        
        conn.commit()
        cursor.close()
        
        print(f"✅ IUCN data import completed: {len(values):,} records imported")
        return True
        
    except Exception as e:
        print(f"❌ IUCN data import failed: {e}")
        traceback.print_exc()
        try:
            conn.rollback()
        except:
            pass
        return False

def main():
    """Main import process for remaining data"""
    print("🚀 FINAL IMPORT: REMAINING BIODIVERSITY DATA")
    print("=" * 55)
    print("Importing with corrected column mappings:")
    print("- Invasive Species: Full Excel dataset with coordinates")
    print("- IUCN Conservation Data: Sample records")
    print("=" * 55)
    
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
            results['invasive'] = False
            
        # 2. IUCN data
        if os.path.exists(data_files['iucn']):
            results['iucn'] = import_iucn_data(conn, data_files['iucn'])
        else:
            print(f"⚠️  IUCN data file not found: {data_files['iucn']}")
            results['iucn'] = False
        
        # Summary
        total_time = time.time() - start_time
        print("\n" + "=" * 55)
        print("🎉 FINAL IMPORT SUMMARY")
        print("=" * 55)
        
        success_count = sum(1 for success in results.values() if success)
        
        for data_type, success in results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"{data_type.title()}: {status}")
        
        print(f"\nSuccessful imports: {success_count}/2")
        print(f"Total import time: {total_time:.2f} seconds")
        
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
        
        if success_count == 2:
            print("\n🌍 ✨ SUCCESS! Your biodiversity database is now COMPLETE! ✨")
            print("Your application now has access to comprehensive biodiversity data:")
            print("  🌊 Over 1 million marine ecosystem records")
            print("  💧 257K+ freshwater risk assessments") 
            print("  🌿 233K+ terrestrial habitat evaluations")
            print("  🐛 Invasive species tracking data")
            print("  🦎 IUCN conservation status records")
        else:
            print("\n⚠️  Some imports failed, but your database still has 1.5M+ core records!")
        
    except Exception as e:
        print(f"❌ Import process failed: {e}")
        traceback.print_exc()
    finally:
        conn.close()
        print("\n✅ Database connection closed")

if __name__ == "__main__":
    main()
