#!/usr/bin/env python3
"""
Debug session authentication flow to find the root cause
"""
import requests
import time

BASE_URL = "http://localhost:5000"

def debug_session_flow():
    """Debug the complete session authentication flow"""
    print("🔍 DEBUGGING SESSION AUTHENTICATION FLOW")
    print("=" * 60)
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Step 1: Check initial session status
    print("\n1. 📊 Initial session status...")
    try:
        response = session.get(f"{BASE_URL}/session-status")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print(f"   Cookies: {dict(session.cookies)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Step 2: Register a test user
    print("\n2. 👤 Registering test user...")
    timestamp = int(time.time())
    test_user = {
        "hotel_name": f"Debug Test {timestamp}",
        "email": f"debug{timestamp}@example.com",
        "password": "testpass123"
    }
    
    try:
        response = session.post(f"{BASE_URL}/register", json=test_user)
        print(f"   Registration: {response.status_code}")
        if response.status_code != 201:
            print(f"   Response: {response.text}")
            # Try with existing user
            test_user["email"] = "debug@example.com"  # Use existing email
    except Exception as e:
        print(f"   Error: {e}")
    
    # Step 3: Login and monitor session
    print("\n3. 🔐 Login and session monitoring...")
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    
    try:
        print(f"   Attempting login with: {login_data['email']}")
        response = session.post(f"{BASE_URL}/login", json=login_data)
        print(f"   Login status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   Login response: {response.json()}")
            print(f"   Session cookies after login: {dict(session.cookies)}")
            
            # Check if cookies are being set
            for cookie in session.cookies:
                print(f"   Cookie: {cookie.name} = {cookie.value}")
                print(f"     - Domain: {cookie.domain}")
                print(f"     - Path: {cookie.path}")
                print(f"     - Secure: {cookie.secure}")
                print(f"     - HttpOnly: {cookie.has_nonstandard_attr('HttpOnly')}")
        else:
            print(f"   Login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"   Login error: {e}")
        return False
    
    # Step 4: Check session status after login
    print("\n4. 📊 Session status after login...")
    try:
        response = session.get(f"{BASE_URL}/session-status")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print(f"   Request headers: {dict(response.request.headers)}")
        print(f"   Cookies sent: {dict(session.cookies)}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Step 5: Try location operation
    print("\n5. 👀 Testing location view (should work now)...")
    try:
        response = session.get(f"{BASE_URL}/locations/view")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        print(f"   Cookies sent: {dict(session.cookies)}")
        
        if response.status_code == 401:
            print("   ❌ STILL GETTING 401 - SESSION NOT PERSISTING!")
            return False
        elif response.status_code == 200:
            print("   ✅ SUCCESS - Session authentication working!")
            return True
        
    except Exception as e:
        print(f"   Error: {e}")
        return False
    
    return False

def test_manual_cookie():
    """Test if the issue is with cookie handling"""
    print("\n" + "=" * 60)
    print("🍪 MANUAL COOKIE TEST")
    print("=" * 60)
    
    # Try to manually extract and set cookies
    session1 = requests.Session()
    session2 = requests.Session()
    
    # Login with session1
    login_data = {"email": "debug@example.com", "password": "testpass123"}
    
    try:
        print("\n1. Login with session1...")
        response = session1.post(f"{BASE_URL}/login", json=login_data)
        if response.status_code == 200:
            print("   Login successful")
            
            # Extract cookies
            cookies = dict(session1.cookies)
            print(f"   Cookies from session1: {cookies}")
            
            # Set cookies manually in session2
            print("\n2. Setting cookies manually in session2...")
            for name, value in cookies.items():
                session2.cookies.set(name, value)
                print(f"   Set cookie: {name} = {value}")
            
            # Test with session2
            print("\n3. Testing location view with session2...")
            response = session2.get(f"{BASE_URL}/locations/view")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
            if response.status_code == 200:
                print("   ✅ Manual cookie transfer worked!")
            else:
                print("   ❌ Manual cookie transfer failed!")
        
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    print("🔧 COMPREHENSIVE SESSION DEBUG")
    
    # Run main debug
    success = debug_session_flow()
    
    # If main test fails, try manual cookie test
    if not success:
        test_manual_cookie()
    
    print("\n" + "=" * 60)
    if not success:
        print("❌ Session authentication is still broken")
        print("\n🔍 POTENTIAL ISSUES:")
        print("   • Session cookies not being set properly")
        print("   • CORS cookie domain issues")
        print("   • Session storage not working")
        print("   • Cookie security settings preventing transmission")
    else:
        print("✅ Session authentication is working correctly!")
