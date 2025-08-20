#!/usr/bin/env python3
"""
Monitor DNS propagation for Supabase database
"""

import socket
import time
import psycopg2
from datetime import datetime

def check_dns_and_connection():
    host = 'db.buwoakllwmwqonquwmbqr.supabase.co'
    connection_string = 'postgresql://postgres:rahul2002rahul@db.buwoakllwmwqonquwmbqr.supabase.co:5432/postgres'
    
    print(f"🕐 {datetime.now().strftime('%H:%M:%S')} - Checking DNS and connection...")
    
    # Test DNS resolution
    try:
        ip = socket.gethostbyname(host)
        print(f"✅ DNS resolved: {host} -> {ip}")
        
        # Test database connection
        try:
            conn = psycopg2.connect(connection_string)
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            cursor.close()
            conn.close()
            
            print("🎉 DATABASE CONNECTION SUCCESSFUL!")
            print(f"PostgreSQL version: {version[0][:50]}...")
            print("\n🚀 You can now run: py init_supabase_with_data.py")
            return True
            
        except Exception as e:
            print(f"⚠️ DNS works but database connection failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ DNS still not resolved: {e}")
        return False

def monitor_until_ready():
    print("🌐 Monitoring DNS propagation from India to US Supabase servers...")
    print("⏰ This typically takes 5-30 minutes for global propagation")
    print("Press Ctrl+C to stop monitoring\n")
    
    attempt = 1
    while True:
        try:
            print(f"Attempt {attempt}:")
            if check_dns_and_connection():
                break
            
            print("⏳ Waiting 60 seconds before next attempt...\n")
            time.sleep(60)
            attempt += 1
            
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
            break
        except Exception as e:
            print(f"❌ Error during monitoring: {e}")
            time.sleep(60)

if __name__ == "__main__":
    monitor_until_ready()
