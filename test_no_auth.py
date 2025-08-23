#!/usr/bin/env python3
"""
Test location operations without authentication
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_no_auth_operations():
    """Test all location operations without any authentication"""
    print("🧪 LOCATION OPERATIONS WITHOUT AUTHENTICATION TEST")
    print("=" * 60)
    
    # No login required! Direct testing
    session = requests.Session()
    
    timestamp = int(time.time())
    
    # Step 1: Test VIEW locations (should work without auth)
    print("\n1. 👀 Testing VIEW locations (no authentication)...")
    try:
        response = session.get(f"{BASE_URL}/locations/view")
        if response.status_code == 200:
            locations = response.json()
            print(f"   ✅ View successful: Found {len(locations.get('locations', []))} locations")
        else:
            print(f"   ❌ View failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ View error: {e}")
        return False
    
    # Step 2: Test ADD location (should work without auth)
    print("\n2. ➕ Testing ADD location (no authentication)...")
    test_location = {
        "hotel_name": f"No Auth Hotel {timestamp}",
        "street_address": "456 No Auth Street",
        "city": "Trenton",
        "zip_code": "08608"
    }
    
    try:
        response = session.post(f"{BASE_URL}/locations/add", json=test_location)
        if response.status_code == 201:
            print(f"   ✅ Add successful: {response.json()}")
        else:
            print(f"   ❌ Add failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Add error: {e}")
        return False
    
    # Step 3: View locations again to get the added location
    print("\n3. 👀 Testing VIEW locations (after adding)...")
    try:
        response = session.get(f"{BASE_URL}/locations/view")
        if response.status_code == 200:
            locations_data = response.json()
            locations = locations_data.get('locations', [])
            print(f"   ✅ View successful: Found {len(locations)} locations")
            
            # Find our test location
            test_loc = None
            for loc in locations:
                if loc.get('hotel_name') == test_location['hotel_name']:
                    test_loc = loc
                    break
            
            if test_loc:
                print(f"   ✅ Test location found: ID={test_loc['id']}")
                location_id = test_loc['id']
            else:
                print("   ❌ Test location not found in results")
                return False
        else:
            print(f"   ❌ View failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ View error: {e}")
        return False
    
    # Step 4: Test EDIT location (should work without auth)
    print("\n4. ✏️ Testing EDIT location (no authentication)...")
    updated_location = {
        "id": location_id,
        "hotel_name": f"Updated No Auth Hotel {timestamp}",
        "street_address": "789 Updated Street",
        "city": "Trenton",
        "zip_code": "08608"
    }
    
    try:
        response = session.post(f"{BASE_URL}/locations/edit", json=updated_location)
        if response.status_code == 200:
            print(f"   ✅ Edit successful: {response.json()}")
        else:
            print(f"   ❌ Edit failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Edit error: {e}")
        return False
    
    # Step 5: Test DELETE location (should work without auth)
    print("\n5. ❌ Testing DELETE location (no authentication)...")
    delete_location = {
        "hotel_name": updated_location['hotel_name'],
        "street_address": updated_location['street_address'],
        "city": updated_location['city'],
        "zip_code": updated_location['zip_code']
    }
    
    try:
        response = session.post(f"{BASE_URL}/locations/delete", json=delete_location)
        if response.status_code == 200:
            print(f"   ✅ Delete successful: {response.json()}")
        else:
            print(f"   ❌ Delete failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Delete error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED! Location operations work WITHOUT authentication!")
    print("\n✅ Location operations verified (NO AUTH REQUIRED):")
    print("   • ADD location - ✅ Working (no login needed)")
    print("   • VIEW locations - ✅ Working (no login needed)")
    print("   • EDIT location - ✅ Working (no login needed)")
    print("   • DELETE location - ✅ Working (no login needed)")
    print("\n🚀 Solution: Authentication removed from location operations!")
    return True

if __name__ == "__main__":
    try:
        if test_no_auth_operations():
            print("\n🎯 SUCCESS: Your location management now works without authentication!")
            exit(0)
        else:
            print("\n❌ Some tests failed.")
            exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        exit(1)
