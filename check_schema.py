#!/usr/bin/env python3
import os
import psycopg2

# Set the database URL
DATABASE_URL = 'postgresql://postgres.fxxxwgomogyzafrvrjio:rahul2002rahul@aws-0-us-east-2.pooler.supabase.com:6543/postgres?sslmode=require'

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    print('🔍 Checking iucn_data table schema...')
    cursor.execute("""
        SELECT column_name, data_type, is_nullable 
        FROM information_schema.columns 
        WHERE table_name = 'iucn_data' 
        ORDER BY ordinal_position;
    """)
    
    columns = cursor.fetchall()
    if columns:
        print('✅ iucn_data table columns:')
        for col in columns:
            print(f'  - {col[0]} ({col[1]}) nullable: {col[2]}')
    else:
        print('❌ iucn_data table not found')
    
    print('\n🔍 Checking if iucn_data table exists and has data...')
    cursor.execute('SELECT COUNT(*) FROM iucn_data;')
    count = cursor.fetchone()[0]
    print(f'✅ iucn_data table has {count} rows')
    
    if count > 0:
        print('\n📊 Sample data from iucn_data:')
        cursor.execute('SELECT * FROM iucn_data LIMIT 3;')
        samples = cursor.fetchall()
        for sample in samples:
            print(f'  {sample}')
    
    conn.close()
    print('\n✅ Database connection successful')
    
except Exception as e:
    print(f'❌ Database error: {e}')
