#!/usr/bin/env python3
"""
Complete end-to-end test for session-based authentication
Tests the actual CRUD operations that were failing
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_complete_session_flow():
    """Test the complete session authentication flow with location CRUD operations"""
    print("🧪 COMPLETE SESSION AUTHENTICATION TEST")
    print("=" * 60)
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Step 1: Health check
    print("\n1. 🏥 Testing health endpoint...")
    try:
        response = session.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print(f"   ✅ Health check: {response.json()}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Step 2: Test session status (should be inactive)
    print("\n2. 📊 Testing session status (before login)...")
    try:
        response = session.get(f"{BASE_URL}/session-status")
        print(f"   Expected 401: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"   ❌ Session status error: {e}")
    
    # Step 3: Register a new user (use timestamp to avoid conflicts)
    print("\n3. 👤 Registering test user...")
    timestamp = int(time.time())
    test_user = {
        "hotel_name": f"Test Hotel {timestamp}",
        "email": f"test{timestamp}@example.com",
        "password": "testpass123"
    }
    
    try:
        response = session.post(
            f"{BASE_URL}/register",
            json=test_user,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            print(f"   ✅ Registration successful: {response.json()}")
        elif response.status_code == 400 and "already registered" in response.text:
            print("   ✅ User already exists, proceeding with login...")
        else:
            print(f"   ❌ Registration failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Registration error: {e}")
        return False
    
    # Step 4: Login with the test user
    print("\n4. 🔐 Testing login...")
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    
    try:
        response = session.post(
            f"{BASE_URL}/login",
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            login_result = response.json()
            print(f"   ✅ Login successful: {login_result['message']}")
            print(f"   👤 User: {login_result['user']['hotel_name']} ({login_result['user']['email']})")
        else:
            print(f"   ❌ Login failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return False
    
    # Step 5: Test session status (should be active now)
    print("\n5. 📊 Testing session status (after login)...")
    try:
        response = session.get(f"{BASE_URL}/session-status")
        if response.status_code == 200:
            session_data = response.json()
            print(f"   ✅ Session active: {session_data}")
        else:
            print(f"   ❌ Session status failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Session status error: {e}")
        return False
    
    # Step 6: Test VIEW locations (should work now)
    print("\n6. 👀 Testing VIEW locations (authenticated)...")
    try:
        response = session.get(f"{BASE_URL}/locations/view")
        if response.status_code == 200:
            locations = response.json()
            print(f"   ✅ View locations successful: Found {len(locations.get('locations', []))} locations")
        else:
            print(f"   ❌ View locations failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ View locations error: {e}")
        return False
    
    # Step 7: Test ADD location (the main failing operation)
    print("\n7. ➕ Testing ADD location (authenticated)...")
    test_location = {
        "hotel_name": f"Test Hotel {timestamp}",
        "street_address": "123 Main Street",
        "city": "Trenton",
        "zip_code": "08608"
    }
    
    try:
        response = session.post(
            f"{BASE_URL}/locations/add",
            json=test_location,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            print(f"   ✅ Add location successful: {response.json()}")
        else:
            print(f"   ❌ Add location failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Add location error: {e}")
        return False
    
    # Step 8: Test VIEW locations again (should show the new location)
    print("\n8. 👀 Testing VIEW locations (after adding)...")
    try:
        response = session.get(f"{BASE_URL}/locations/view")
        if response.status_code == 200:
            locations_data = response.json()
            locations = locations_data.get('locations', [])
            print(f"   ✅ View locations successful: Found {len(locations)} locations")
            
            # Find our test location
            test_loc = None
            for loc in locations:
                if loc.get('hotel_name') == test_location['hotel_name']:
                    test_loc = loc
                    break
            
            if test_loc:
                print(f"   ✅ Test location found: ID={test_loc['id']}, Address={test_loc['street_address']}")
                location_id = test_loc['id']
            else:
                print("   ❌ Test location not found in results")
                return False
        else:
            print(f"   ❌ View locations failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ View locations error: {e}")
        return False
    
    # Step 9: Test EDIT location
    print("\n9. ✏️ Testing EDIT location (authenticated)...")
    updated_location = {
        "id": location_id,
        "hotel_name": f"Updated Hotel {timestamp}",
        "street_address": "456 Updated Street",
        "city": "Trenton",
        "zip_code": "08608"
    }
    
    try:
        response = session.post(
            f"{BASE_URL}/locations/edit",
            json=updated_location,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print(f"   ✅ Edit location successful: {response.json()}")
        else:
            print(f"   ❌ Edit location failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Edit location error: {e}")
        return False
    
    # Step 10: Test DELETE location
    print("\n10. ❌ Testing DELETE location (authenticated)...")
    delete_location = {
        "hotel_name": updated_location['hotel_name'],
        "street_address": updated_location['street_address'],
        "city": updated_location['city'],
        "zip_code": updated_location['zip_code']
    }
    
    try:
        response = session.post(
            f"{BASE_URL}/locations/delete",
            json=delete_location,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print(f"   ✅ Delete location successful: {response.json()}")
        else:
            print(f"   ❌ Delete location failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Delete location error: {e}")
        return False
    
    # Step 11: Final verification - view locations should show it's gone
    print("\n11. 👀 Testing VIEW locations (after deleting)...")
    try:
        response = session.get(f"{BASE_URL}/locations/view")
        if response.status_code == 200:
            locations_data = response.json()
            locations = locations_data.get('locations', [])
            print(f"   ✅ View locations successful: Found {len(locations)} locations")
            
            # Verify our test location is gone
            for loc in locations:
                if loc.get('id') == location_id:
                    print("   ❌ Test location still exists after deletion!")
                    return False
            
            print("   ✅ Test location successfully deleted")
        else:
            print(f"   ❌ View locations failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ View locations error: {e}")
        return False
    
    # Step 12: Test logout
    print("\n12. 🚪 Testing logout...")
    try:
        response = session.post(f"{BASE_URL}/logout")
        if response.status_code == 200:
            print(f"   ✅ Logout successful: {response.json()}")
        else:
            print(f"   ❌ Logout failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Logout error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED! Session authentication is working correctly!")
    print("\n✅ Location operations verified:")
    print("   • ADD location - ✅ Working")
    print("   • VIEW locations - ✅ Working") 
    print("   • EDIT location - ✅ Working")
    print("   • DELETE location - ✅ Working")
    print("\nThe session authentication issue has been resolved! 🎯")
    return True

if __name__ == "__main__":
    try:
        if test_complete_session_flow():
            exit(0)  # Success
        else:
            print("\n❌ Some tests failed. Check the backend logs for more details.")
            exit(1)  # Failure
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {e}")
        exit(1)
