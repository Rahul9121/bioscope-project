#!/usr/bin/env python3
"""
Quick test to verify zip code validation is fixed
"""
import requests
import time

BASE_URL = "http://localhost:5000"

def quick_test():
    print("🧪 Quick Zip Code Validation Test")
    print("=" * 40)
    
    session = requests.Session()
    
    # Register and login
    timestamp = int(time.time())
    test_user = {
        "hotel_name": f"Quick Test {timestamp}",
        "email": f"quick{timestamp}@example.com", 
        "password": "testpass123"
    }
    
    print("1. Registering user...")
    try:
        response = session.post(f"{BASE_URL}/register", json=test_user)
        print(f"   Registration: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("2. Logging in...")
    try:
        response = session.post(f"{BASE_URL}/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        print(f"   Login: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("3. Testing ADD location with 08608 zip...")
    test_location = {
        "hotel_name": test_user["hotel_name"],
        "street_address": "123 Test St",
        "city": "Trenton", 
        "zip_code": "08608"
    }
    
    try:
        response = session.post(f"{BASE_URL}/locations/add", json=test_location)
        print(f"   Add location: {response.status_code}")
        
        if response.status_code == 201:
            print("   ✅ SUCCESS! Zip code validation is fixed!")
            return True
        else:
            print(f"   ❌ Failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    quick_test()
