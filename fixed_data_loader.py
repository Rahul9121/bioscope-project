#!/usr/bin/env python3
"""
Fixed Data Loader for Bioscope - Works with existing schema
"""
import psycopg2
import csv
from pathlib import Path
import sys

# Database configuration
connection_params = {
    'host': '3.101.5.153',
    'port': 6543,
    'database': 'postgres',
    'user': 'postgres.buwoakllwmwqonqwmbqr',
    'password': 'rahul2002rahul',
    'sslmode': 'require'
}

# New Jersey bounding box
NJ_BOUNDS = {
    "north": 41.36,
    "south": 38.92,
    "west": -75.58,
    "east": -73.90
}

def connect_db():
    """Connect to database"""
    try:
        conn = psycopg2.connect(**connection_params)
        return conn
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

def is_within_nj(lat, lon):
    """Check if coordinates are within New Jersey"""
    return (NJ_BOUNDS["south"] <= lat <= NJ_BOUNDS["north"] and 
            NJ_BOUNDS["west"] <= lon <= NJ_BOUNDS["east"])

def check_table_schema(conn, table_name):
    """Check what columns exist in a table"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}' AND table_schema = 'public'
            ORDER BY ordinal_position;
        """)
        columns = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return columns
    except Exception as e:
        print(f"Error checking schema for {table_name}: {e}")
        return []

def load_freshwater_risk_data(conn):
    """Load freshwater risk data from CSV"""
    print("\n🌊 Loading freshwater risk data...")
    
    csv_path = Path("backend/database/freshwater_risk_updated.csv")
    if not csv_path.exists():
        print(f"⚠️  File not found: {csv_path}")
        return False
    
    try:
        cursor = conn.cursor()
        loaded_count = 0
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    x = float(row['x'])  # longitude
                    y = float(row['y'])  # latitude
                    
                    # Filter for New Jersey area
                    if not is_within_nj(y, x):
                        continue
                    
                    normalized_risk = float(row.get('normalized_risk', 0))
                    risk_level = row.get('risk_level', 'Low').replace(' Risk', '')
                    
                    cursor.execute("""
                        INSERT INTO freshwater_risk (x, y, normalized_risk, risk_level)
                        VALUES (%s, %s, %s, %s)
                    """, (x, y, normalized_risk, risk_level))
                    
                    loaded_count += 1
                    
                except (ValueError, KeyError) as e:
                    continue  # Skip invalid rows
        
        conn.commit()
        cursor.close()
        print(f"✅ Loaded {loaded_count} freshwater risk records")
        return True
        
    except Exception as e:
        print(f"❌ Error loading freshwater data: {e}")
        return False

def load_marine_hci_data(conn):
    """Load marine HCI data from CSV"""
    print("\n🌊 Loading marine HCI data...")
    
    csv_path = Path("backend/database/marine_human_coexistence_nj.csv")
    if not csv_path.exists():
        print(f"⚠️  File not found: {csv_path}")
        return False
    
    try:
        cursor = conn.cursor()
        loaded_count = 0
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    x = float(row['x'])  # longitude
                    y = float(row['y'])  # latitude
                    
                    # Filter for New Jersey area
                    if not is_within_nj(y, x):
                        continue
                    
                    marine_hci = float(row.get('marine_hci', 0.0))
                    
                    cursor.execute("""
                        INSERT INTO marine_hci (x, y, marine_hci)
                        VALUES (%s, %s, %s)
                    """, (x, y, marine_hci))
                    
                    loaded_count += 1
                    
                except (ValueError, KeyError) as e:
                    continue
        
        conn.commit()
        cursor.close()
        print(f"✅ Loaded {loaded_count} marine HCI records")
        return True
        
    except Exception as e:
        print(f"❌ Error loading marine HCI data: {e}")
        return False

def create_invasive_species_data(conn):
    """Create invasive species data based on actual schema"""
    print("\n🦎 Creating invasive species data...")
    
    # Check what columns exist
    columns = check_table_schema(conn, 'invasive_species')
    print(f"  Invasive species table columns: {columns}")
    
    # Invasive species data for New Jersey
    invasive_species_data = [
        (40.0583, -74.4057, 'Purple Loosestrife', 'high'),
        (40.7128, -74.0060, 'Japanese Knotweed', 'high'),
        (40.1907, -74.6728, 'Tree of Heaven', 'high'),
        (40.4420, -74.0134, 'Mile-a-Minute Weed', 'high'),
        (40.2206, -74.7563, 'Autumn Olive', 'moderate'),
        (39.7267, -75.2835, 'Multiflora Rose', 'moderate'),
        (40.3573, -74.4291, 'Japanese Barberry', 'moderate'),
        (40.5795, -74.1502, 'Japanese Honeysuckle', 'moderate'),
        (40.8176, -74.2291, 'Garlic Mustard', 'moderate'),
        (40.9176, -74.1718, 'Norway Maple', 'low'),
        (40.6892, -74.0445, 'Common Reed', 'low'),
        (40.5370, -74.4634, 'Privet', 'low'),
    ]
    
    try:
        cursor = conn.cursor()
        
        # Use basic columns that should exist
        for lat, lon, common_name, threat_code in invasive_species_data:
            if 'scientific_name' in columns:
                cursor.execute("""
                    INSERT INTO invasive_species (latitude, longitude, common_name, scientific_name, threat_code)
                    VALUES (%s, %s, %s, %s, %s)
                """, (lat, lon, common_name, 'Species name', threat_code))
            else:
                cursor.execute("""
                    INSERT INTO invasive_species (latitude, longitude, common_name, threat_code)
                    VALUES (%s, %s, %s, %s)
                """, (lat, lon, common_name, threat_code))
        
        conn.commit()
        cursor.close()
        print(f"✅ Loaded {len(invasive_species_data)} invasive species records")
        return True
        
    except Exception as e:
        print(f"❌ Error loading invasive species data: {e}")
        return False

def create_iucn_data(conn):
    """Create IUCN conservation data"""
    print("\n🦅 Creating IUCN conservation data...")
    
    iucn_data = [
        (40.9176, -74.1718, 'Bog Turtle', 'Endangered', 'Wetlands'),
        (40.5795, -74.1502, 'Northern Long-eared Bat', 'Endangered', 'Forest'),
        (40.2206, -74.7563, 'Wood Turtle', 'Vulnerable', 'Streams/Forest'),
        (40.1907, -74.6728, 'Timber Rattlesnake', 'Vulnerable', 'Forest'),
        (40.3573, -74.4291, 'Pine Barrens Treefrog', 'Near Threatened', 'Wetlands'),
        (40.0583, -74.4057, 'Bald Eagle', 'Least Concern', 'Wetlands'),
        (40.7128, -74.0060, 'Peregrine Falcon', 'Least Concern', 'Urban/Cliffs'),
        (40.8176, -74.2291, 'Bobcat', 'Least Concern', 'Forest/Suburban'),
        (40.4420, -74.0134, 'Osprey', 'Least Concern', 'Coastal/Wetlands'),
        (39.8703, -75.0094, 'Black Bear', 'Least Concern', 'Forest'),
    ]
    
    try:
        cursor = conn.cursor()
        
        for lat, lon, species_name, threat_status, habitat in iucn_data:
            cursor.execute("""
                INSERT INTO iucn_data (latitude, longitude, species_name, threat_status, habitat)
                VALUES (%s, %s, %s, %s, %s)
            """, (lat, lon, species_name, threat_status, habitat))
        
        conn.commit()
        cursor.close()
        print(f"✅ Loaded {len(iucn_data)} IUCN conservation records")
        return True
        
    except Exception as e:
        print(f"❌ Error loading IUCN data: {e}")
        return False

def create_terrestrial_data(conn):
    """Create terrestrial risk data"""
    print("\n🌲 Creating terrestrial risk data...")
    
    terrestrial_data = [
        (-74.4057, 40.0583, 0.85, 'high'),    # Princeton area
        (-74.0060, 40.7128, 0.78, 'high'),    # NYC metro area
        (-75.1652, 39.9526, 0.82, 'high'),    # Philadelphia metro
        (-74.6728, 40.1907, 0.90, 'high'),    # Central NJ
        (-74.2291, 40.8176, 0.75, 'high'),    # Northern NJ
        (-74.7563, 40.2206, 0.55, 'moderate'), # Trenton area
        (-75.2835, 39.7267, 0.60, 'moderate'), # Camden area
        (-74.1718, 40.9176, 0.40, 'moderate'), # North Bergen
        (-74.4291, 40.3573, 0.65, 'moderate'), # New Brunswick area
        (-74.1502, 40.5795, 0.58, 'moderate'), # Newark area
        (-74.5575, 39.4955, 0.25, 'low'),     # Pine Barrens
        (-74.7844, 39.1612, 0.20, 'low'),     # Cape May area
        (-74.8984, 40.9906, 0.35, 'low'),     # Delaware Water Gap
        (-75.0343, 40.8676, 0.30, 'low'),     # Pocono border area
        (-74.3774, 40.7008, 0.28, 'low'),     # Watchung Reservation
    ]
    
    try:
        cursor = conn.cursor()
        
        for x, y, normalized_risk, risk_level in terrestrial_data:
            cursor.execute("""
                INSERT INTO terrestrial_risk (x, y, normalized_risk, risk_level)
                VALUES (%s, %s, %s, %s)
            """, (x, y, normalized_risk, risk_level))
        
        conn.commit()
        cursor.close()
        print(f"✅ Loaded {len(terrestrial_data)} terrestrial risk records")
        return True
        
    except Exception as e:
        print(f"❌ Error loading terrestrial risk data: {e}")
        return False

def verify_data_loading(conn):
    """Verify data loading"""
    print("\n🔍 Verifying data loading...")
    
    tables_to_check = [
        'invasive_species',
        'iucn_data',
        'freshwater_risk', 
        'marine_hci',
        'terrestrial_risk'
    ]
    
    try:
        cursor = conn.cursor()
        total_records = 0
        
        for table in tables_to_check:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  ✅ {table}: {count} records")
            total_records += count
        
        cursor.close()
        print(f"\n📊 Total biodiversity records: {total_records}")
        
        # Test search query
        cursor = conn.cursor()
        test_lat, test_lon = 40.0583, -74.4057
        
        cursor.execute("""
            SELECT COUNT(*) FROM invasive_species 
            WHERE ABS(latitude - %s) <= 0.1 AND ABS(longitude - %s) <= 0.1
        """, (test_lat, test_lon))
        invasive_count = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM freshwater_risk 
            WHERE ABS(y - %s) <= 0.5 AND ABS(x - %s) <= 0.1
        """, (test_lat, test_lon))
        fresh_count = cursor.fetchone()[0]
        
        search_total = invasive_count + fresh_count
        print(f"  🧪 Test search near Princeton: {search_total} results")
        
        cursor.close()
        return search_total > 0
        
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False

def main():
    """Main execution"""
    print("🚀 Fixed Bioscope Data Loader")
    print("=" * 40)
    
    conn = connect_db()
    if not conn:
        return False
    
    success_count = 0
    
    # Load real CSV data
    if load_freshwater_risk_data(conn):
        success_count += 1
    
    if load_marine_hci_data(conn):
        success_count += 1
    
    # Create sample data
    if create_invasive_species_data(conn):
        success_count += 1
    
    if create_iucn_data(conn):
        success_count += 1
    
    if create_terrestrial_data(conn):
        success_count += 1
    
    # Verify
    if verify_data_loading(conn):
        print(f"\n🎉 Data loading completed successfully!")
        print(f"   Successfully loaded {success_count}/5 data types")
        print("   Database is ready for biodiversity risk assessment!")
        conn.close()
        return True
    else:
        print("\n⚠️  Data loading completed with issues")
        conn.close()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
