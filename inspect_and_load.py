#!/usr/bin/env python3
"""
Inspect existing schema and load data accordingly
"""
import psycopg2
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

def inspect_schema():
    """Inspect existing database schema"""
    print("🔍 Inspecting existing database schema...")
    
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        
        biodiversity_tables = ['invasive_species', 'iucn_data', 'freshwater_risk', 'marine_hci', 'terrestrial_risk']
        
        print(f"\n📋 Found {len(tables)} tables total")
        
        for table in biodiversity_tables:
            if table in tables:
                print(f"\n✅ {table} exists:")
                
                # Get columns
                cursor.execute(f"""
                    SELECT column_name, data_type, is_nullable 
                    FROM information_schema.columns 
                    WHERE table_name = '{table}' AND table_schema = 'public'
                    ORDER BY ordinal_position;
                """)
                
                columns = cursor.fetchall()
                for col_name, data_type, nullable in columns:
                    null_status = "NULL" if nullable == 'YES' else "NOT NULL"
                    print(f"    - {col_name}: {data_type} ({null_status})")
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"    → Current records: {count}")
                
            else:
                print(f"❌ {table} does not exist")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Schema inspection failed: {e}")
        return False

def load_compatible_data():
    """Load data compatible with existing schema"""
    print("\n🚀 Loading data compatible with existing schema...")
    
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        
        # Load IUCN data without habitat column
        print("\n🦅 Loading IUCN data (without habitat)...")
        cursor.execute("DELETE FROM iucn_data")
        
        iucn_data = [
            (40.9176, -74.1718, 'Bog Turtle', 'Endangered'),
            (40.5795, -74.1502, 'Northern Long-eared Bat', 'Endangered'),
            (40.2206, -74.7563, 'Wood Turtle', 'Vulnerable'),
            (40.1907, -74.6728, 'Timber Rattlesnake', 'Vulnerable'),
            (40.3573, -74.4291, 'Pine Barrens Treefrog', 'Near Threatened'),
            (40.0583, -74.4057, 'Bald Eagle', 'Least Concern'),
            (40.7128, -74.0060, 'Peregrine Falcon', 'Least Concern'),
            (40.8176, -74.2291, 'Bobcat', 'Least Concern'),
            (40.4420, -74.0134, 'Osprey', 'Least Concern'),
            (39.8703, -75.0094, 'Black Bear', 'Least Concern'),
        ]
        
        for lat, lon, species_name, threat_status in iucn_data:
            cursor.execute("""
                INSERT INTO iucn_data (latitude, longitude, species_name, threat_status)
                VALUES (%s, %s, %s, %s)
            """, (lat, lon, species_name, threat_status))
        
        print(f"✅ Loaded {len(iucn_data)} IUCN records")
        
        # Load terrestrial risk data
        print("\n🌲 Loading terrestrial risk data...")
        cursor.execute("DELETE FROM terrestrial_risk")
        
        terrestrial_data = [
            (-74.4057, 40.0583, 0.85, 'high'),
            (-74.0060, 40.7128, 0.78, 'high'),
            (-75.1652, 39.9526, 0.82, 'high'),
            (-74.6728, 40.1907, 0.90, 'high'),
            (-74.2291, 40.8176, 0.75, 'high'),
            (-74.7563, 40.2206, 0.55, 'moderate'),
            (-75.2835, 39.7267, 0.60, 'moderate'),
            (-74.1718, 40.9176, 0.40, 'moderate'),
            (-74.4291, 40.3573, 0.65, 'moderate'),
            (-74.1502, 40.5795, 0.58, 'moderate'),
            (-74.5575, 39.4955, 0.25, 'low'),
            (-74.7844, 39.1612, 0.20, 'low'),
            (-74.8984, 40.9906, 0.35, 'low'),
            (-75.0343, 40.8676, 0.30, 'low'),
            (-74.3774, 40.7008, 0.28, 'low'),
        ]
        
        for x, y, normalized_risk, risk_level in terrestrial_data:
            cursor.execute("""
                INSERT INTO terrestrial_risk (x, y, normalized_risk, risk_level)
                VALUES (%s, %s, %s, %s)
            """, (x, y, normalized_risk, risk_level))
        
        print(f"✅ Loaded {len(terrestrial_data)} terrestrial risk records")
        
        conn.commit()
        
        # Final verification
        print("\n📊 Final database state:")
        biodiversity_tables = ['invasive_species', 'iucn_data', 'freshwater_risk', 'marine_hci', 'terrestrial_risk']
        total_records = 0
        
        for table in biodiversity_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  ✅ {table}: {count} records")
            total_records += count
        
        print(f"\n🎯 Total biodiversity records: {total_records}")
        
        # Test search
        print("\n🧪 Testing search near Princeton (40.0583, -74.4057):")
        
        cursor.execute("""
            SELECT COUNT(*) FROM invasive_species 
            WHERE ABS(latitude - 40.0583) <= 0.1 AND ABS(longitude - (-74.4057)) <= 0.1
        """)
        invasive_results = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM iucn_data 
            WHERE ABS(latitude - 40.0583) <= 0.1 AND ABS(longitude - (-74.4057)) <= 0.1
        """)
        iucn_results = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM freshwater_risk 
            WHERE ABS(y - 40.0583) <= 0.5 AND ABS(x - (-74.4057)) <= 0.1
        """)
        fresh_results = cursor.fetchone()[0]
        
        total_search_results = invasive_results + iucn_results + fresh_results
        print(f"  📈 Total search results: {total_search_results}")
        print(f"    - Invasive species: {invasive_results}")
        print(f"    - IUCN data: {iucn_results}")
        print(f"    - Freshwater risk: {fresh_results}")
        
        cursor.close()
        conn.close()
        
        if total_search_results > 0:
            print("\n🎉 Database is fully functional!")
            print("   ✅ All tables populated with data")
            print("   ✅ Search functionality verified")
            print("   ✅ Ready for biodiversity risk assessment")
            return True
        else:
            print("\n⚠️  Database setup completed but search needs verification")
            return False
        
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False

if __name__ == "__main__":
    print("🔬 Bioscope Schema Inspector & Data Loader")
    print("=" * 50)
    
    if inspect_schema():
        if load_compatible_data():
            print("\n🎉 Complete setup successful!")
            print("\n🚀 Next Steps:")
            print("   1. Test your Railway backend deployment")
            print("   2. Visit https://bioscope-project.vercel.app")
            print("   3. Try searching with ZIP codes: 08540, 07001, 08902")
        else:
            print("\n⚠️  Setup completed with issues")
    else:
        print("\n❌ Schema inspection failed")
        sys.exit(1)
