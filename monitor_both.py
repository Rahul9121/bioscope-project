#!/usr/bin/env python3
"""
Monitor both local and Railway connectivity to Supabase
"""

import socket
import requests
import time
from datetime import datetime

def check_local_dns():
    """Check DNS resolution from local machine (India)"""
    try:
        ip = socket.gethostbyname('aws-1-us-west-1.pooler.supabase.com')
        return True, ip
    except:
        return False, None

def check_railway_backend():
    """Check Railway backend connectivity"""
    try:
        response = requests.get('https://bioscope-project-production.up.railway.app/db-status', timeout=10)
        if response.status_code == 200:
            data = response.json()
            return True, data.get('status') == 'connected'
        return False, False
    except:
        return False, False

def monitor_both():
    """Monitor both local and Railway connectivity"""
    print("🌐 Monitoring Global DNS Propagation")
    print("="*50)
    print("📍 Local: India → US Supabase")
    print("🚂 Railway: US Server → US Supabase")
    print("⏰ Expected: 5-30 minutes for global propagation")
    print()
    
    attempt = 1
    while True:
        try:
            print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - Attempt {attempt}")
            
            # Check local DNS (India)
            local_dns, ip = check_local_dns()
            print(f"📍 Local DNS (India): {'✅ Resolved' if local_dns else '❌ Not resolved'}")
            if ip:
                print(f"   IP: {ip}")
            
            # Check Railway backend
            railway_alive, railway_db = check_railway_backend()
            print(f"🚂 Railway Backend: {'✅ Running' if railway_alive else '❌ Issues'}")
            print(f"🗄️ Railway → Database: {'✅ Connected' if railway_db else '❌ DNS issue'}")
            
            # Success condition
            if local_dns and railway_db:
                print()
                print("🎉 SUCCESS! Both local and Railway can connect!")
                print("🚀 Ready to load biodiversity data!")
                print()
                print("Next steps:")
                print("1. Run: py init_supabase_with_data.py")
                print("2. Deploy frontend to Vercel")
                print("3. Test complete integration")
                break
            
            # Partial success
            elif railway_db:
                print("✅ Railway connection working! (but local DNS still propagating)")
                print("💡 You can deploy frontend now and test from US")
            elif local_dns:
                print("✅ Local DNS working! (Railway may be caching old DNS)")
                print("💡 Railway should connect within 5-10 minutes")
            
            print("⏳ Waiting 60 seconds...")
            print("-" * 50)
            time.sleep(60)
            attempt += 1
            
        except KeyboardInterrupt:
            print()
            print("🛑 Monitoring stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    monitor_both()
