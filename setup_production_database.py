#!/usr/bin/env python3
"""
Production Database Setup Script for Bioscope App
This script will create tables and populate them with all your critical CSV data
"""

import os
import sys
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BioscoDatabaseSetup:
    def __init__(self, database_url):
        self.database_url = database_url
        self.engine = None
        self.base_dir = Path(__file__).parent / "backend" / "database"
        
    def connect(self):
        """Establish database connection"""
        try:
            self.engine = create_engine(self.database_url, echo=False)
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                logger.info("✅ Successfully connected to database")
                return True
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            return False
    
    def create_tables(self):
        """Create all necessary tables"""
        logger.info("🔧 Creating database tables...")
        
        try:
            with self.engine.connect() as conn:
                # Drop existing tables if they exist (for fresh setup)
                drop_queries = [
                    "DROP TABLE IF EXISTS users CASCADE;",
                    "DROP TABLE IF EXISTS invasive_species CASCADE;", 
                    "DROP TABLE IF EXISTS iucn_data CASCADE;",
                    "DROP TABLE IF EXISTS freshwater_risk CASCADE;",
                    "DROP TABLE IF EXISTS marine_hci CASCADE;",
                    "DROP TABLE IF EXISTS terrestrial_risk CASCADE;"
                ]
                
                for query in drop_queries:
                    conn.execute(text(query))
                
                # Create tables with proper schema
                table_queries = [
                    # Users table
                    """
                    CREATE TABLE users (
                        id SERIAL PRIMARY KEY,
                        hotel_name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        password_hash VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    """,
                    
                    # Invasive species table
                    """
                    CREATE TABLE invasive_species (
                        id SERIAL PRIMARY KEY,
                        latitude DECIMAL(10, 8),
                        longitude DECIMAL(11, 8),
                        common_name VARCHAR(255),
                        scientific_name VARCHAR(255),
                        threat_code VARCHAR(50) DEFAULT 'low'
                    );
                    """,
                    
                    # IUCN data table
                    """
                    CREATE TABLE iucn_data (
                        id SERIAL PRIMARY KEY,
                        latitude DECIMAL(10, 8),
                        longitude DECIMAL(11, 8),
                        species_name VARCHAR(255),
                        threat_status VARCHAR(100),
                        habitat VARCHAR(255)
                    );
                    """,
                    
                    # Freshwater risk table
                    """
                    CREATE TABLE freshwater_risk (
                        id SERIAL PRIMARY KEY,
                        x DECIMAL(11, 8),
                        y DECIMAL(10, 8),
                        freshwater_hci DECIMAL(10, 6) DEFAULT 0.0,
                        popden2010 DECIMAL(10, 6) DEFAULT 1.0,
                        maxrdd DECIMAL(10, 6) DEFAULT 1.0,
                        meanuse DECIMAL(10, 6) DEFAULT 1.0,
                        maxdof DECIMAL(10, 6) DEFAULT 1.0,
                        mincsi DECIMAL(10, 6) DEFAULT 1.0,
                        maxsed DECIMAL(10, 6) DEFAULT 1.0,
                        weighted_risk DECIMAL(10, 6) DEFAULT 0.0,
                        log_weighted_risk DECIMAL(10, 6) DEFAULT 0.0,
                        transformed_risk DECIMAL(10, 6) DEFAULT 0.0,
                        normalized_risk DECIMAL(5, 3),
                        risk_level VARCHAR(50) DEFAULT 'Low'
                    );
                    """,
                    
                    # Marine HCI table
                    """
                    CREATE TABLE marine_hci (
                        id SERIAL PRIMARY KEY,
                        x DECIMAL(11, 8),
                        y DECIMAL(10, 8),
                        marine_hci DECIMAL(5, 3) DEFAULT 0.0
                    );
                    """,
                    
                    # Terrestrial risk table
                    """
                    CREATE TABLE terrestrial_risk (
                        id SERIAL PRIMARY KEY,
                        x DECIMAL(11, 8),
                        y DECIMAL(10, 8),
                        terrestrial_hci DECIMAL(5, 3) DEFAULT 1.0,
                        aggdp2010 DECIMAL(10, 6) DEFAULT 1.0,
                        ntlharm2020 DECIMAL(10, 6) DEFAULT 1.0,
                        popden2010 DECIMAL(10, 6) DEFAULT 1.0,
                        hmnlc2020 DECIMAL(10, 6) DEFAULT 1.0,
                        roadden DECIMAL(10, 6) DEFAULT 1.0,
                        tt_cities_over_5k DECIMAL(10, 6) DEFAULT 1.0,
                        tt_ports_large DECIMAL(10, 6) DEFAULT 1.0,
                        mineden DECIMAL(10, 6) DEFAULT 1.0,
                        weighted_risk DECIMAL(10, 6) DEFAULT 0.0,
                        transformed_risk DECIMAL(10, 6) DEFAULT 0.0,
                        normalized_risk DECIMAL(5, 3),
                        risk_level VARCHAR(50) DEFAULT 'low'
                    );
                    """
                ]
                
                for query in table_queries:
                    conn.execute(text(query))
                
                conn.commit()
                logger.info("✅ All tables created successfully")
                
        except Exception as e:
            logger.error(f"❌ Failed to create tables: {e}")
            raise
    
    def load_csv_data(self, file_path, table_name, chunk_size=1000):
        """Load CSV data into database table"""
        try:
            if not os.path.exists(file_path):
                logger.warning(f"⚠️  File not found: {file_path}")
                return False
            
            logger.info(f"📊 Loading data from {file_path} into {table_name}")
            
            # Read CSV in chunks to handle large files
            chunk_count = 0
            total_rows = 0
            
            for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                chunk_count += 1
                
                # Clean the data
                chunk = chunk.replace([float('inf'), -float('inf')], None)
                chunk = chunk.fillna(value=pd.NA)
                
                # Load chunk to database
                try:
                    chunk.to_sql(table_name, self.engine, if_exists='append', 
                               index=False, method='multi')
                    rows_in_chunk = len(chunk)
                    total_rows += rows_in_chunk
                    logger.info(f"   Loaded chunk {chunk_count} ({rows_in_chunk} rows)")
                    
                except Exception as e:
                    logger.error(f"   Failed to load chunk {chunk_count}: {e}")
                    continue
            
            logger.info(f"✅ Successfully loaded {total_rows} rows into {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load {file_path}: {e}")
            return False
    
    def load_sample_iucn_data(self):
        """Load IUCN sample data"""
        iucn_file = self.base_dir / "sample_data" / "cleaned_IUCN_data_sample.csv"
        return self.load_csv_data(str(iucn_file), "iucn_data")
    
    def load_freshwater_data(self):
        """Load freshwater risk data"""
        fresh_file = self.base_dir / "freshwater_risk_updated.csv"
        return self.load_csv_data(str(fresh_file), "freshwater_risk")
    
    def load_terrestrial_data(self):
        """Load terrestrial risk data"""
        terr_file = self.base_dir / "terrestrial_risk_updated.csv"
        return self.load_csv_data(str(terr_file), "terrestrial_risk")
    
    def load_marine_data(self):
        """Load marine HCI data"""
        marine_file = self.base_dir / "marine_human_coexistence_nj.csv"
        return self.load_csv_data(str(marine_file), "marine_hci")
    
    def add_sample_invasive_species(self):
        """Add sample invasive species data"""
        logger.info("🌱 Adding sample invasive species data...")
        
        try:
            with self.engine.connect() as conn:
                invasive_data = [
                    (40.0583, -74.4057, 'Purple Loosestrife', 'Lythrum salicaria', 'high'),
                    (40.7128, -74.0060, 'Japanese Knotweed', 'Fallopia japonica', 'moderate'),
                    (40.2206, -74.7563, 'Autumn Olive', 'Elaeagnus umbellata', 'moderate'),
                    (39.7267, -75.2835, 'Multiflora Rose', 'Rosa multiflora', 'low'),
                    (40.9176, -74.1718, 'Norway Maple', 'Acer platanoides', 'low'),
                    (40.3573, -74.6692, 'Japanese Honeysuckle', 'Lonicera japonica', 'moderate'),
                    (40.5795, -74.1502, 'Oriental Bittersweet', 'Celastrus orbiculatus', 'high'),
                    (39.9612, -75.1652, 'Tree of Heaven', 'Ailanthus altissima', 'high'),
                ]
                
                query = """
                    INSERT INTO invasive_species (latitude, longitude, common_name, scientific_name, threat_code) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                
                conn.execute(text("""
                    INSERT INTO invasive_species (latitude, longitude, common_name, scientific_name, threat_code) 
                    VALUES 
                    (40.0583, -74.4057, 'Purple Loosestrife', 'Lythrum salicaria', 'high'),
                    (40.7128, -74.0060, 'Japanese Knotweed', 'Fallopia japonica', 'moderate'),
                    (40.2206, -74.7563, 'Autumn Olive', 'Elaeagnus umbellata', 'moderate'),
                    (39.7267, -75.2835, 'Multiflora Rose', 'Rosa multiflora', 'low'),
                    (40.9176, -74.1718, 'Norway Maple', 'Acer platanoides', 'low'),
                    (40.3573, -74.6692, 'Japanese Honeysuckle', 'Lonicera japonica', 'moderate'),
                    (40.5795, -74.1502, 'Oriental Bittersweet', 'Celastrus orbiculatus', 'high'),
                    (39.9612, -75.1652, 'Tree of Heaven', 'Ailanthus altissima', 'high')
                """))
                
                conn.commit()
                logger.info("✅ Sample invasive species data added")
                return True
                
        except Exception as e:
            logger.error(f"❌ Failed to add invasive species data: {e}")
            return False
    
    def create_indexes(self):
        """Create performance indexes"""
        logger.info("🔍 Creating database indexes...")
        
        try:
            with self.engine.connect() as conn:
                index_queries = [
                    "CREATE INDEX IF NOT EXISTS idx_invasive_species_location ON invasive_species(latitude, longitude);",
                    "CREATE INDEX IF NOT EXISTS idx_iucn_data_location ON iucn_data(latitude, longitude);",
                    "CREATE INDEX IF NOT EXISTS idx_freshwater_risk_location ON freshwater_risk(x, y);",
                    "CREATE INDEX IF NOT EXISTS idx_marine_hci_location ON marine_hci(x, y);",
                    "CREATE INDEX IF NOT EXISTS idx_terrestrial_risk_location ON terrestrial_risk(x, y);",
                    "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);"
                ]
                
                for query in index_queries:
                    conn.execute(text(query))
                
                conn.commit()
                logger.info("✅ Database indexes created")
                
        except Exception as e:
            logger.error(f"❌ Failed to create indexes: {e}")
    
    def verify_data(self):
        """Verify that data was loaded correctly"""
        logger.info("🔍 Verifying database data...")
        
        try:
            with self.engine.connect() as conn:
                tables = [
                    'users', 'invasive_species', 'iucn_data', 
                    'freshwater_risk', 'marine_hci', 'terrestrial_risk'
                ]
                
                for table in tables:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    logger.info(f"   {table}: {count:,} records")
                
                logger.info("✅ Database verification complete")
                return True
                
        except Exception as e:
            logger.error(f"❌ Database verification failed: {e}")
            return False
    
    def setup_complete_database(self):
        """Run complete database setup"""
        logger.info("🚀 Starting complete database setup...")
        
        if not self.connect():
            return False
        
        try:
            # Create tables
            self.create_tables()
            
            # Load all data
            logger.info("📊 Loading CSV data files...")
            self.load_sample_iucn_data()
            self.load_freshwater_data()
            self.load_terrestrial_data()
            self.load_marine_data()
            self.add_sample_invasive_species()
            
            # Create indexes
            self.create_indexes()
            
            # Verify data
            self.verify_data()
            
            logger.info("🎉 Database setup completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database setup failed: {e}")
            return False

def main():
    print("🔧 Bioscope Production Database Setup")
    print("=" * 50)
    
    # Get database URL from environment or prompt
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL is not properly configured!")
        print("Please update your .env file with your actual Supabase connection string.")
        print("Example: postgresql://postgres:yourpassword@db.yourref.supabase.co:5432/postgres")
        return False
    
    if 'pooler.supabase.com' not in database_url and 'supabase.co' not in database_url:
        print("❌ DATABASE_URL does not appear to be a Supabase connection string!")
        print(f"Current URL: {database_url}")
        return False
    
    # Initialize and run setup
    setup = BioscoDatabaseSetup(database_url)
    success = setup.setup_complete_database()
    
    if success:
        print("\n🎉 Database setup completed successfully!")
        print("✅ Your application should now work with all your critical data")
        print("✅ You can deploy and test your application")
    else:
        print("\n❌ Database setup failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
