#!/usr/bin/env python3
import requests
import json

# Replace with your actual Railway URL
BACKEND_URL = "https://bioscope-project-production.up.railway.app"
# Replace with your Vercel URL
FRONTEND_URL = "https://bioscope-project.vercel.app"

def test_registration():
    """Test the registration endpoint directly"""
    
    print("🧪 Testing Registration Endpoint")
    print("=" * 50)
    
    # Test data
    test_user = {
        "hotel_name": "Test Hotel",
        "email": "test@example.com", 
        "password": "TestPass123!"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Origin": FRONTEND_URL
    }
    
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Frontend Origin: {FRONTEND_URL}")
    print(f"Test data: {json.dumps(test_user, indent=2)}")
    
    try:
        # Test health endpoint first
        print("\n1. Testing health endpoint...")
        health_response = requests.get(f"{BACKEND_URL}/health")
        print(f"Health status: {health_response.status_code}")
        if health_response.status_code == 200:
            print(f"Health response: {health_response.json()}")
        else:
            print(f"Health error: {health_response.text}")
            return
        
        # Test database status
        print("\n2. Testing database status...")
        db_response = requests.get(f"{BACKEND_URL}/db-status")
        print(f"DB status: {db_response.status_code}")
        if db_response.status_code == 200:
            print(f"DB response: {json.dumps(db_response.json(), indent=2)}")
        else:
            print(f"DB error: {db_response.text}")
        
        # Test registration
        print("\n3. Testing registration...")
        registration_response = requests.post(
            f"{BACKEND_URL}/register",
            json=test_user,
            headers=headers
        )
        
        print(f"Registration status: {registration_response.status_code}")
        print(f"Registration headers: {dict(registration_response.headers)}")
        
        if registration_response.status_code in [200, 201]:
            print(f"✅ Registration successful: {registration_response.json()}")
        else:
            print(f"❌ Registration failed:")
            print(f"Response text: {registration_response.text}")
            try:
                print(f"Response JSON: {json.dumps(registration_response.json(), indent=2)}")
            except:
                print("Could not parse response as JSON")
                
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection Error: {e}")
        print("This usually means the backend is not accessible")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    test_registration()
