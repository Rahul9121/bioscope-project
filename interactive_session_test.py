#!/usr/bin/env python3
"""
Interactive Session Authentication Test
Tests the fixed session-based authentication with real user credentials
"""

import requests
import json
import sys
import getpass

def test_session_auth_interactive():
    """Interactive test of session-based authentication"""
    print("🔍 INTERACTIVE Session Authentication Test")
    print("=" * 60)
    print("This test will verify that session cookies work properly.")
    print("You'll need valid login credentials to complete the test.")
    print()
    
    # Get base URL
    base_url = input("Enter backend URL (default: http://localhost:5000): ").strip()
    if not base_url:
        base_url = "http://localhost:5000"
    
    print(f"🌐 Testing against: {base_url}")
    
    # Create session object to maintain cookies
    session = requests.Session()
    
    # Test 1: Health check
    print("\n1️⃣ Testing health endpoint...")
    try:
        response = session.get(f"{base_url}/health")
        if response.status_code == 200:
            print("   ✅ Backend is running")
        else:
            print(f"   ❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to backend: {e}")
        return False
    
    # Test 2: Session status before login
    print("\n2️⃣ Testing session status (before login)...")
    try:
        response = session.get(f"{base_url}/session-status")
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Correctly shows no active session")
        else:
            data = response.json()
            active = data.get('active', False)
            if not active:
                print("   ✅ Correctly shows inactive session")
            else:
                print("   ⚠️ Unexpected: session appears active before login")
    except Exception as e:
        print(f"   ❌ Session status check failed: {e}")
    
    # Test 3: Location access before login
    print("\n3️⃣ Testing location access (before login)...")
    try:
        response = session.get(f"{base_url}/locations/view")
        if response.status_code == 401:
            print("   ✅ Correctly blocked unauthenticated access")
        else:
            print(f"   ⚠️ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Location access test failed: {e}")
    
    # Test 4: Login
    print("\n4️⃣ Testing login...")
    print("Enter your login credentials:")
    email = input("Email: ").strip()
    password = getpass.getpass("Password: ")
    
    if not email or not password:
        print("   ❌ Email and password are required")
        return False
    
    login_data = {"email": email, "password": password}
    
    try:
        response = session.post(
            f"{base_url}/login",
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Login successful!")
            user_data = response.json().get('user', {})
            print(f"   Logged in as: {user_data.get('email', 'Unknown')}")
            
            # Show session cookies
            cookies = dict(session.cookies)
            if cookies:
                print(f"   Session cookies: {list(cookies.keys())}")
            else:
                print("   ⚠️ No session cookies received")
            
        else:
            error_msg = response.json().get('error', 'Unknown error')
            print(f"   ❌ Login failed: {error_msg}")
            return False
            
    except Exception as e:
        print(f"   ❌ Login request failed: {e}")
        return False
    
    # Test 5: Session status after login
    print("\n5️⃣ Testing session status (after login)...")
    try:
        response = session.get(f"{base_url}/session-status")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('active'):
                print("   ✅ Session is active after login!")
                debug_info = data.get('debug', {})
                print(f"   User ID: {debug_info.get('user_id')}")
                print(f"   Email: {debug_info.get('email')}")
            else:
                print("   ❌ Session not active despite successful login")
                return False
        else:
            print("   ❌ Session status check failed after login")
            return False
            
    except Exception as e:
        print(f"   ❌ Session status check failed: {e}")
        return False
    
    # Test 6: Location access after login
    print("\n6️⃣ Testing location access (after login)...")
    try:
        response = session.get(f"{base_url}/locations/view")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Location access successful!")
            locations = response.json().get('locations', [])
            print(f"   Found {len(locations)} locations")
        else:
            error_msg = response.json().get('error', 'Unknown error')
            print(f"   ❌ Location access failed: {error_msg}")
            return False
            
    except Exception as e:
        print(f"   ❌ Location access test failed: {e}")
        return False
    
    # Test 7: Add location (optional)
    test_add = input("\n🤔 Test adding a location? (y/n, default=n): ").strip().lower()
    if test_add == 'y':
        print("\n7️⃣ Testing add location...")
        location_data = {
            "hotel_name": "Test Hotel",
            "street_address": "123 Test St",
            "city": "Test City",
            "zip_code": "07001",
            "email": email
        }
        
        try:
            response = session.post(f"{base_url}/locations/add", json=location_data)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 201:
                print("   ✅ Location added successfully!")
            else:
                error_msg = response.json().get('error', 'Unknown error')
                print(f"   ❌ Add location failed: {error_msg}")
                
        except Exception as e:
            print(f"   ❌ Add location test failed: {e}")
    
    # Test 8: Logout
    print("\n8️⃣ Testing logout...")
    try:
        response = session.post(f"{base_url}/logout")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Logout successful!")
        else:
            print("   ⚠️ Logout response unexpected")
            
    except Exception as e:
        print(f"   ❌ Logout failed: {e}")
    
    # Test 9: Session status after logout
    print("\n9️⃣ Testing session status (after logout)...")
    try:
        response = session.get(f"{base_url}/session-status")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 401:
            print("   ✅ Session correctly cleared after logout!")
        else:
            data = response.json()
            if not data.get('active'):
                print("   ✅ Session correctly shows inactive after logout!")
            else:
                print("   ❌ Session still active after logout")
                
    except Exception as e:
        print(f"   ❌ Session status check failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Session authentication test completed!")
    print("\n📋 Summary:")
    print("✅ If all tests passed, session authentication is working correctly!")
    print("❌ If any tests failed, check the backend logs for details.")
    
    return True

if __name__ == "__main__":
    try:
        test_session_auth_interactive()
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
