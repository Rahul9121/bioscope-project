#!/usr/bin/env python3
"""
Test script to verify session-based authentication fixes
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_session_authentication():
    """Test the session-based authentication flow"""
    print("🔍 Testing Session-Based Authentication Fixes")
    print("=" * 50)
    
    # Step 1: Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   ✅ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return False
    
    # Step 2: Test session status without login
    print("\n2. Testing session status without login...")
    try:
        response = requests.get(f"{BASE_URL}/session-status")
        print(f"   ✅ Session status (no login): {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"   ❌ Session status failed: {e}")
    
    # Step 3: Test location access without login
    print("\n3. Testing location access without login...")
    try:
        response = requests.get(f"{BASE_URL}/locations/view")
        print(f"   Expected 401: {response.status_code} - {response.json()}")
        if response.status_code == 401:
            print("   ✅ Correctly blocked unauthenticated access")
        else:
            print("   ❌ Should have blocked unauthenticated access")
    except Exception as e:
        print(f"   ❌ Location test failed: {e}")
    
    # Step 4: Test login (you'll need to use real credentials)
    print("\n4. Testing login...")
    print("   📝 Note: You'll need to register a user first or use existing credentials")
    
    # For this demo, we'll just test the endpoints are responding
    test_credentials = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        # Create a session to maintain cookies
        session = requests.Session()
        
        response = session.post(
            f"{BASE_URL}/login",
            json=test_credentials,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Login attempt: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Login successful!")
            
            # Test session status after login
            print("\n5. Testing session status after login...")
            response = session.get(f"{BASE_URL}/session-status")
            print(f"   Session status (after login): {response.status_code} - {response.json()}")
            
            # Test location access after login
            print("\n6. Testing location access after login...")
            response = session.get(f"{BASE_URL}/locations/view")
            print(f"   Location access (after login): {response.status_code} - {response.json()}")
            
        else:
            print(f"   Expected login failure (no test user): {response.json()}")
    except Exception as e:
        print(f"   ❌ Login test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")
    print("\n💡 To fully test:")
    print("1. Start the backend: cd backend && py app.py")
    print("2. Register a test user first")
    print("3. Run this script: py test_session_fix.py")

if __name__ == "__main__":
    test_session_authentication()
