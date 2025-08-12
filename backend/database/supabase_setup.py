#!/usr/bin/env python3
"""
Database setup script for Supabase
This script will create tables and populate them with data from your CSV files
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
import sys

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Supabase connection string
# Replace this with your actual Supabase connection string
DATABASE_URL = "postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"

def setup_database():
    """Set up all tables and populate with data"""
    
    print("🔄 Connecting to Supabase database...")
    try:
        engine = create_engine(DATABASE_URL, echo=True)
        
        print("✅ Connected to database successfully!")
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print(f"✅ Database connection test: {result.fetchone()}")
        
        # Create tables
        print("🔄 Creating database tables...")
        create_all_tables(engine)
        
        # Populate with data
        print("🔄 Populating tables with sample data...")
        populate_sample_data(engine)
        
        print("🎉 Database setup complete!")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False
    
    return True

def create_all_tables(engine):
    """Create all required tables"""
    
    with engine.connect() as conn:
        # Users table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                hotel_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                password_hash VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Invasive species table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS invasive_species (
                id SERIAL PRIMARY KEY,
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                common_name VARCHAR(255),
                scientific_name VARCHAR(255),
                threat_code VARCHAR(50) DEFAULT 'low'
            )
        """))
        
        # IUCN data table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS iucn_data (
                id SERIAL PRIMARY KEY,
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                species_name VARCHAR(255),
                threat_status VARCHAR(100),
                habitat VARCHAR(255)
            )
        """))
        
        # Freshwater risk table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS freshwater_risk (
                id SERIAL PRIMARY KEY,
                x DECIMAL(11, 8),
                y DECIMAL(10, 8),
                normalized_risk DECIMAL(5, 3),
                risk_level VARCHAR(50) DEFAULT 'Low'
            )
        """))
        
        # Marine HCI table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS marine_hci (
                id SERIAL PRIMARY KEY,
                x DECIMAL(11, 8),
                y DECIMAL(10, 8),
                marine_hci DECIMAL(5, 3) DEFAULT 0.0
            )
        """))
        
        # Terrestrial risk table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS terrestrial_risk (
                id SERIAL PRIMARY KEY,
                x DECIMAL(11, 8),
                y DECIMAL(10, 8),
                normalized_risk DECIMAL(5, 3),
                risk_level VARCHAR(50) DEFAULT 'low'
            )
        """))
        
        conn.commit()
        print("✅ All tables created successfully!")

def populate_sample_data(engine):
    """Populate tables with actual data from CSV files"""
    
    base_dir = os.path.dirname(__file__)
    
    try:
        # Load IUCN sample data
        print("📊 Loading IUCN data...")
        iucn_file = os.path.join(base_dir, 'sample_data', 'cleaned_IUCN_data_sample.csv')
        if os.path.exists(iucn_file):
            iucn_df = pd.read_csv(iucn_file)
            print(f"   Found {len(iucn_df)} IUCN records")
            
            # Insert IUCN data
            iucn_records = []
            for _, row in iucn_df.iterrows():
                iucn_records.append({
                    'lat': float(row.get('latitude', 0)) if pd.notna(row.get('latitude')) else 0,
                    'lon': float(row.get('longitude', 0)) if pd.notna(row.get('longitude')) else 0,
                    'species': str(row.get('species_name', '')) if pd.notna(row.get('species_name')) else '',
                    'status': str(row.get('threat_status', 'Unknown')) if pd.notna(row.get('threat_status')) else 'Unknown',
                    'habitat': str(row.get('habitat', '')) if pd.notna(row.get('habitat')) else ''
                })
            
            with engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO iucn_data (latitude, longitude, species_name, threat_status, habitat) 
                    VALUES (:lat, :lon, :species, :status, :habitat)
                """), iucn_records[:500])  # Limit to first 500 records
                conn.commit()
            print("✅ IUCN data loaded successfully!")
    
        # Load freshwater risk data
        print("📊 Loading freshwater risk data...")
        freshwater_file = os.path.join(base_dir, 'freshwater_risk_updated.csv')
        if os.path.exists(freshwater_file):
            fresh_df = pd.read_csv(freshwater_file)
            print(f"   Found {len(fresh_df)} freshwater records")
            
            fresh_records = []
            for _, row in fresh_df.iterrows():
                fresh_records.append({
                    'x': float(row.get('x', 0)) if pd.notna(row.get('x')) else 0,
                    'y': float(row.get('y', 0)) if pd.notna(row.get('y')) else 0,
                    'risk': float(row.get('normalized_risk', 0)) if pd.notna(row.get('normalized_risk')) else 0,
                    'level': str(row.get('risk_level', 'Low')) if pd.notna(row.get('risk_level')) else 'Low'
                })
            
            with engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO freshwater_risk (x, y, normalized_risk, risk_level) 
                    VALUES (:x, :y, :risk, :level)
                """), fresh_records[:1000])  # Limit to first 1000 records
                conn.commit()
            print("✅ Freshwater risk data loaded successfully!")
    
        # Load marine HCI data
        print("📊 Loading marine HCI data...")
        marine_file = os.path.join(base_dir, 'marine_human_coexistence_nj.csv')
        if os.path.exists(marine_file):
            marine_df = pd.read_csv(marine_file)
            print(f"   Found {len(marine_df)} marine records")
            
            marine_records = []
            for _, row in marine_df.iterrows():
                marine_records.append({
                    'x': float(row.get('x', 0)) if pd.notna(row.get('x')) else 0,
                    'y': float(row.get('y', 0)) if pd.notna(row.get('y')) else 0,
                    'hci': float(row.get('marine_hci', 0)) if pd.notna(row.get('marine_hci')) else 0
                })
            
            with engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO marine_hci (x, y, marine_hci) 
                    VALUES (:x, :y, :hci)
                """), marine_records[:1000])  # Limit to first 1000 records
                conn.commit()
            print("✅ Marine HCI data loaded successfully!")
    
        # Load terrestrial risk data
        print("📊 Loading terrestrial risk data...")
        terrestrial_file = os.path.join(base_dir, 'terrestrial_risk_updated.csv')
        if os.path.exists(terrestrial_file):
            terr_df = pd.read_csv(terrestrial_file)
            print(f"   Found {len(terr_df)} terrestrial records")
            
            terr_records = []
            for _, row in terr_df.iterrows():
                terr_records.append({
                    'x': float(row.get('x', 0)) if pd.notna(row.get('x')) else 0,
                    'y': float(row.get('y', 0)) if pd.notna(row.get('y')) else 0,
                    'risk': float(row.get('normalized_risk', 0)) if pd.notna(row.get('normalized_risk')) else 0,
                    'level': str(row.get('risk_level', 'low')) if pd.notna(row.get('risk_level')) else 'low'
                })
            
            with engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO terrestrial_risk (x, y, normalized_risk, risk_level) 
                    VALUES (:x, :y, :risk, :level)
                """), terr_records[:1000])  # Limit to first 1000 records
                conn.commit()
            print("✅ Terrestrial risk data loaded successfully!")
    
        # Add some sample invasive species data
        print("📊 Adding sample invasive species data...")
        invasive_data = [
            (40.0583, -74.4057, 'Purple Loosestrife', 'Lythrum salicaria', 'high'),
            (40.7128, -74.0060, 'Japanese Knotweed', 'Fallopia japonica', 'moderate'),
            (40.2206, -74.7563, 'Autumn Olive', 'Elaeagnus umbellata', 'moderate'),
            (39.7267, -75.2835, 'Multiflora Rose', 'Rosa multiflora', 'low'),
            (40.9176, -74.1718, 'Norway Maple', 'Acer platanoides', 'low'),
        ]
        
        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO invasive_species (latitude, longitude, common_name, scientific_name, threat_code) 
                VALUES (:lat, :lon, :common, :sci, :threat)
            """), [{"lat": d[0], "lon": d[1], "common": d[2], "sci": d[3], "threat": d[4]} for d in invasive_data])
            conn.commit()
        print("✅ Invasive species data loaded successfully!")
        
    except Exception as e:
        print(f"❌ Error loading CSV data: {e}")
        print("ℹ️  Falling back to basic sample data...")
        
        # Fallback sample data if CSV files can't be loaded
        with engine.connect() as conn:
            # Basic sample data as fallback
            conn.execute(text("""
                INSERT INTO iucn_data (latitude, longitude, species_name, threat_status) VALUES
                (40.0583, -74.4057, 'Bald Eagle', 'Least Concern'),
                (40.7128, -74.0060, 'Peregrine Falcon', 'Least Concern'),
                (40.2206, -74.7563, 'Wood Turtle', 'Vulnerable')
            """))
            
            conn.execute(text("""
                INSERT INTO freshwater_risk (x, y, normalized_risk, risk_level) VALUES
                (-74.4057, 40.0583, 0.75, 'High'),
                (-74.0060, 40.7128, 0.45, 'Moderate'),
                (-74.7563, 40.2206, 0.25, 'Low')
            """))
            
            conn.execute(text("""
                INSERT INTO marine_hci (x, y, marine_hci) VALUES
                (-74.4057, 40.0583, 0.80),
                (-74.0060, 40.7128, 0.65),
                (-74.7563, 40.2206, 0.45)
            """))
            
            conn.execute(text("""
                INSERT INTO terrestrial_risk (x, y, normalized_risk, risk_level) VALUES
                (-74.4057, 40.0583, 0.85, 'high'),
                (-74.0060, 40.7128, 0.55, 'moderate'),
                (-74.7563, 40.2206, 0.25, 'low')
            """))
            
            conn.commit()
        print("✅ Fallback sample data loaded successfully!")

if __name__ == "__main__":
    print("🔧 Bioscope Database Setup for Supabase")
    print("=" * 50)
    
    # Check if DATABASE_URL is properly set
    if "[YOUR-PASSWORD]" in DATABASE_URL or "[PROJECT-REF]" in DATABASE_URL:
        print("❌ Please update the DATABASE_URL with your actual Supabase connection string!")
        print("   Update line 12 in this file with your Supabase connection string from Step 1.3")
        exit(1)
    
    success = setup_database()
    
    if success:
        print("\n🎉 Database setup completed successfully!")
        print("✅ Your Supabase database is now populated with sample data")
        print("✅ You can now test your application")
    else:
        print("\n❌ Database setup failed. Please check the error messages above.")
