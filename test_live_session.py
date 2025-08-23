#!/usr/bin/env python3
"""
Test live session authentication with your deployed app
"""

import requests
import json

def test_live_session():
    """Test session authentication with deployed app"""
    print("🔍 Testing Live Session Authentication")
    print("=" * 50)
    
    # Your live backend URL
    base_url = "https://bioscope-project-production.up.railway.app"
    
    # Create session for cookies
    session = requests.Session()
    
    # Test 1: Health check
    print("1️⃣ Testing health...")
    try:
        response = session.get(f"{base_url}/health")
        print(f"   Health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"   Health failed: {e}")
        return
    
    # Test 2: Session status before login
    print("\n2️⃣ Session status (before login)...")
    try:
        response = session.get(f"{base_url}/session-status")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print(f"   Cookies: {dict(session.cookies)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Login with your credentials
    print("\n3️⃣ Testing login...")
    login_data = {
        "email": "navenrambo@gmail.com",  # Your email from logs
        "password": input("Enter your password: ")
    }
    
    try:
        response = session.post(f"{base_url}/login", json=login_data)
        print(f"   Login Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print(f"   Cookies after login: {dict(session.cookies)}")
        
        if response.status_code != 200:
            print("   Login failed - cannot continue")
            return
            
    except Exception as e:
        print(f"   Login error: {e}")
        return
    
    # Test 4: Session status after login
    print("\n4️⃣ Session status (after login)...")
    try:
        response = session.get(f"{base_url}/session-status")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print(f"   Cookies: {dict(session.cookies)}")
        
        if response.status_code == 200 and response.json().get('active'):
            print("   ✅ Backend session is working!")
        else:
            print("   ❌ Backend session NOT working!")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Location view
    print("\n5️⃣ Testing location view...")
    try:
        response = session.get(f"{base_url}/locations/view")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            print("   ✅ Location access working!")
        else:
            print("   ❌ Location access failing!")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 6: Check specific cookie details
    print("\n6️⃣ Cookie analysis...")
    for cookie in session.cookies:
        print(f"   Cookie: {cookie.name}")
        print(f"   Value: {cookie.value[:20]}...")
        print(f"   Domain: {cookie.domain}")
        print(f"   Path: {cookie.path}")
        print(f"   Secure: {cookie.secure}")
        print(f"   HttpOnly: {getattr(cookie, '_rest', {}).get('HttpOnly', 'Unknown')}")
        print()

if __name__ == "__main__":
    test_live_session()
