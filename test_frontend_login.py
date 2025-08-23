#!/usr/bin/env python3
"""
Frontend Login Test - JWT Token Analysis
This script tests the login flow and JWT token handling
"""

import requests
import json
import time

# Test URLs
BACKEND_URL = "https://bioscope-project-production.up.railway.app"
FRONTEND_URL = "https://bioscope-project.vercel.app"

def test_backend_health():
    """Test if backend is healthy"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        print(f"🏥 Backend Health Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
            return True
        return False
    except Exception as e:
        print(f"❌ Backend health check failed: {e}")
        return False

def test_login_endpoint():
    """Test backend login endpoint directly"""
    try:
        # Test with a simple login request
        login_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        
        print(f"🔐 Testing login endpoint...")
        response = requests.post(
            f"{BACKEND_URL}/login", 
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        print(f"   Content: {response.text[:500]}...")
        
        if response.status_code == 200:
            try:
                response_json = response.json()
                print(f"✅ Login response received:")
                print(f"   - Message: {response_json.get('message')}")
                print(f"   - Has Token: {'token' in response_json}")
                if 'token' in response_json:
                    token = response_json['token']
                    print(f"   - Token Preview: {str(token)[:50]}...")
                    print(f"   - Token Type: {type(token)}")
                    print(f"   - Token Length: {len(str(token)) if token else 0}")
                else:
                    print(f"❌ NO TOKEN in response!")
                return response_json
            except json.JSONDecodeError:
                print(f"⚠️ Response is not valid JSON")
                return None
        else:
            print(f"❌ Login failed with status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return None

def test_frontend_accessibility():
    """Test if frontend is accessible"""
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        print(f"🌐 Frontend Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Frontend is accessible")
            return True
        return False
    except Exception as e:
        print(f"❌ Frontend check failed: {e}")
        return False

def main():
    print("🧪 Frontend Login & JWT Token Test")
    print("=" * 50)
    
    # Step 1: Test backend health
    print("\n1. Backend Health Check")
    backend_healthy = test_backend_health()
    
    # Step 2: Test frontend accessibility
    print("\n2. Frontend Accessibility Check")
    frontend_accessible = test_frontend_accessibility()
    
    # Step 3: Test login endpoint
    print("\n3. Login Endpoint Test")
    login_response = test_login_endpoint()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print(f"   Backend Health: {'✅ PASS' if backend_healthy else '❌ FAIL'}")
    print(f"   Frontend Access: {'✅ PASS' if frontend_accessible else '❌ FAIL'}")
    print(f"   Login Endpoint: {'✅ PASS' if login_response else '❌ FAIL'}")
    
    if login_response:
        has_token = 'token' in login_response and login_response['token'] is not None
        print(f"   JWT Token: {'✅ PRESENT' if has_token else '❌ MISSING'}")
    
    # Recommendations
    print("\n🎯 RECOMMENDATIONS:")
    if not backend_healthy:
        print("   - Backend is not healthy - check Railway deployment")
    if not frontend_accessible:
        print("   - Frontend is not accessible - check Vercel deployment")
    if login_response and 'token' not in login_response:
        print("   - JWT token is missing from login response")
        print("   - Check backend JWT token generation code")
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    main()
