#!/usr/bin/env python3
"""
Session Authentication Debugging Script
Comprehensive test to identify why sessions are not persisting after login
"""

import requests
import json
import sys
import getpass
import time

def debug_session_issue():
    """Debug session authentication issue step by step"""
    print("🔍 COMPREHENSIVE SESSION DEBUGGING")
    print("=" * 70)
    print("This script will help identify why sessions aren't working after login.")
    print()
    
    # Configuration
    base_url = input("Enter backend URL (default: http://localhost:5000): ").strip()
    if not base_url:
        base_url = "http://localhost:5000"
    
    print(f"🌐 Testing against: {base_url}")
    print()
    
    # Create a requests session to handle cookies
    session = requests.Session()
    
    # Step 1: Test basic connectivity
    print("1️⃣ Testing basic connectivity...")
    try:
        response = session.get(f"{base_url}/health")
        if response.status_code == 200:
            print("   ✅ Backend is responding")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to backend: {e}")
        return False
    
    # Step 2: Check session status before login
    print("\n2️⃣ Checking session status before login...")
    try:
        response = session.get(f"{base_url}/session-status")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
        print(f"   Cookies before login: {dict(session.cookies)}")
        
        if response.status_code == 401 or not response.json().get('active', False):
            print("   ✅ Correctly shows no active session")
        else:
            print("   ⚠️ Unexpected: session appears active before login")
    except Exception as e:
        print(f"   ❌ Session status check failed: {e}")
    
    # Step 3: Attempt login with debugging
    print("\n3️⃣ Attempting login with full debugging...")
    print("Enter your credentials:")
    email = input("Email: ").strip()
    password = getpass.getpass("Password: ")
    
    login_data = {"email": email, "password": password}
    
    try:
        # Show request details
        print(f"   📤 Login Request:")
        print(f"      URL: {base_url}/login")
        print(f"      Method: POST")
        print(f"      Headers: Content-Type: application/json")
        print(f"      Data: {json.dumps(login_data, indent=6)}")
        
        response = session.post(
            f"{base_url}/login",
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   📥 Login Response:")
        print(f"      Status Code: {response.status_code}")
        print(f"      Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"      Body: {json.dumps(response_data, indent=6)}")
        except:
            print(f"      Body (raw): {response.text}")
        
        print(f"   🍪 Cookies after login: {dict(session.cookies)}")
        
        if response.status_code == 200:
            print("   ✅ Login request successful")
            
            # Check if we got the expected session cookie
            cookie_names = list(session.cookies.keys())
            print(f"   Cookie names received: {cookie_names}")
            
            expected_cookie = 'biodiv_session_v5'
            if expected_cookie in cookie_names:
                print(f"   ✅ Session cookie '{expected_cookie}' received")
                cookie_value = session.cookies[expected_cookie]
                print(f"   Cookie value: {cookie_value[:50]}..." if len(cookie_value) > 50 else f"   Cookie value: {cookie_value}")
            else:
                print(f"   ❌ Expected session cookie '{expected_cookie}' NOT received")
                print("   This is likely the root cause of the issue!")
                
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Login request failed: {e}")
        return False
    
    # Step 4: Check session status immediately after login
    print("\n4️⃣ Checking session status immediately after login...")
    try:
        response = session.get(f"{base_url}/session-status")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=4)}")
        print(f"   Cookies sent with request: {dict(session.cookies)}")
        
        if response.status_code == 200 and response.json().get('active'):
            print("   ✅ Session is active immediately after login")
        else:
            print("   ❌ Session is NOT active after login - THIS IS THE ISSUE")
            print("   The login succeeded but the session is not being maintained")
            
    except Exception as e:
        print(f"   ❌ Session status check failed: {e}")
    
    # Step 5: Test location access with detailed debugging
    print("\n5️⃣ Testing location access with full debugging...")
    try:
        print(f"   📤 Location Request:")
        print(f"      URL: {base_url}/locations/view")
        print(f"      Method: GET")
        print(f"      Cookies being sent: {dict(session.cookies)}")
        
        response = session.get(f"{base_url}/locations/view")
        
        print(f"   📥 Location Response:")
        print(f"      Status Code: {response.status_code}")
        print(f"      Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"      Body: {json.dumps(response_data, indent=4)}")
        except:
            print(f"      Body (raw): {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Location access successful - session authentication working!")
            locations = response.json().get('locations', [])
            print(f"   Found {len(locations)} locations")
        elif response.status_code == 401:
            print("   ❌ Location access failed - Session authentication NOT working")
            print("   This confirms the session issue")
        else:
            print(f"   ⚠️ Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Location access test failed: {e}")
    
    # Step 6: Test with manual cookie inspection
    print("\n6️⃣ Manual cookie inspection...")
    cookies = session.cookies
    print(f"   Total cookies: {len(cookies)}")
    for cookie in cookies:
        print(f"   Cookie: {cookie.name} = {cookie.value[:50]}...")
        print(f"           Domain: {cookie.domain}")
        print(f"           Path: {cookie.path}")
        print(f"           Secure: {cookie.secure}")
        print(f"           HttpOnly: {hasattr(cookie, 'get_nonstandard_attr') and cookie.get_nonstandard_attr('HttpOnly')}")
    
    # Step 7: Test with curl equivalent
    print("\n7️⃣ Generating curl equivalent for manual testing...")
    if session.cookies:
        cookie_header = "; ".join([f"{c.name}={c.value}" for c in session.cookies])
        curl_cmd = f"""
curl -X GET "{base_url}/locations/view" \\
     -H "Content-Type: application/json" \\
     -H "Cookie: {cookie_header}" \\
     -v"""
        print("   You can test manually with this curl command:")
        print(curl_cmd)
    
    print("\n" + "=" * 70)
    print("🔍 DEBUGGING SUMMARY")
    print("=" * 70)
    
    # Analyze the results
    has_session_cookie = 'biodiv_session_v5' in [c.name for c in session.cookies]
    
    if not has_session_cookie:
        print("❌ ROOT CAUSE IDENTIFIED: Session cookie not being set by backend")
        print("   Potential issues:")
        print("   1. Flask session configuration issue")
        print("   2. CORS configuration not allowing cookies") 
        print("   3. Domain/path mismatch for cookies")
        print("   4. Session middleware not working properly")
        print("\n   RECOMMENDED FIXES:")
        print("   1. Check backend logs during login for session creation")
        print("   2. Verify Flask session configuration")
        print("   3. Check CORS configuration for credentials")
        print("   4. Test with same-origin request (no CORS)")
        
    else:
        print("✅ Session cookie is being set correctly")
        print("❌ But authentication is still failing")
        print("   This suggests:")
        print("   1. Session data is not being persisted properly")
        print("   2. Session validation logic has issues")
        print("   3. Different Flask app contexts")
        print("\n   RECOMMENDED FIXES:")
        print("   1. Check Flask session storage (filesystem vs memory)")
        print("   2. Verify session validation in location routes")
        print("   3. Check if multiple Flask app instances are running")
    
    return True

if __name__ == "__main__":
    try:
        debug_session_issue()
    except KeyboardInterrupt:
        print("\n⚠️ Debugging interrupted by user")
    except Exception as e:
        print(f"\n❌ Debugging failed: {e}")
        import traceback
        traceback.print_exc()
