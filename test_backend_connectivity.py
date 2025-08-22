#!/usr/bin/env python3
"""
Test Railway backend connectivity and functionality
"""
import requests
import json
import sys

# Common Railway URL patterns to test
possible_urls = [
    "https://bioscope-project-production.up.railway.app",
    "https://web-production-1234.up.railway.app",  # Will need actual URL
    "https://backend-production-5678.up.railway.app",  # Will need actual URL
    "https://app-production-9abc.up.railway.app"  # Will need actual URL
]

def test_railway_endpoints():
    """Test Railway backend endpoints"""
    print("🚂 Testing Railway Backend Connectivity")
    print("=" * 50)
    
    working_url = None
    
    for url in possible_urls:
        print(f"\n🧪 Testing: {url}")
        
        try:
            # Test health endpoint
            response = requests.get(f"{url}/health", timeout=10)
            if response.status_code == 200:
                print(f"  ✅ Health check: {response.json()}")
                working_url = url
                break
            else:
                print(f"  ❌ Health check failed: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"  ❌ Connection failed: Could not connect")
        except requests.exceptions.Timeout:
            print(f"  ❌ Timeout: Request timed out")
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:50]}...")
    
    if working_url:
        print(f"\n🎉 Found working backend URL: {working_url}")
        return test_full_functionality(working_url)
    else:
        print(f"\n❌ No working Railway URLs found")
        print(f"📋 Manual steps needed:")
        print(f"   1. Go to https://railway.app")
        print(f"   2. Find your bioscope project")
        print(f"   3. Get the deployment URL")
        print(f"   4. Update this script with the correct URL")
        return None

def test_full_functionality(base_url):
    """Test full backend functionality"""
    print(f"\n🔍 Testing full functionality for: {base_url}")
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Health check
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("  ✅ Health endpoint working")
            tests_passed += 1
        else:
            print(f"  ❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Health endpoint error: {e}")
    
    # Test 2: Database status
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/db-status")
        if response.status_code == 200:
            db_info = response.json()
            print(f"  ✅ Database status: {db_info.get('status', 'unknown')}")
            tests_passed += 1
        else:
            print(f"  ❌ Database status failed: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Database status error: {e}")
    
    # Test 3: Search functionality
    total_tests += 1
    try:
        search_data = {"input_text": "08540"}  # Princeton, NJ
        response = requests.post(f"{base_url}/search", 
                               json=search_data, 
                               headers={"Content-Type": "application/json"},
                               timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'risks' in result and len(result['risks']) > 0:
                print(f"  ✅ Search working: {len(result['risks'])} risks found")
                print(f"    Sample risk: {result['risks'][0].get('risk_type', 'Unknown')}")
                tests_passed += 1
            else:
                print(f"  ⚠️  Search returns empty results")
        else:
            print(f"  ❌ Search failed: {response.status_code}")
            if response.text:
                print(f"    Error: {response.text[:100]}...")
    except Exception as e:
        print(f"  ❌ Search error: {e}")
    
    # Test 4: CORS headers
    total_tests += 1
    try:
        response = requests.options(f"{base_url}/search")
        if 'Access-Control-Allow-Origin' in response.headers:
            print(f"  ✅ CORS configured properly")
            tests_passed += 1
        else:
            print(f"  ⚠️  CORS may need configuration")
    except Exception as e:
        print(f"  ❌ CORS test error: {e}")
    
    print(f"\n📊 Backend Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed >= 3:
        print(f"🎉 Backend is functional! Ready for frontend integration")
        return base_url
    else:
        print(f"⚠️  Backend has issues that need to be resolved")
        return None

def create_frontend_config(backend_url):
    """Create frontend configuration for the working backend"""
    print(f"\n⚙️  Creating frontend configuration...")
    
    # Create environment configuration for frontend
    frontend_config = f"""# Frontend Environment Configuration
# Add this to your Vercel environment variables

NEXT_PUBLIC_API_URL={backend_url}
NEXT_PUBLIC_API_BASE_URL={backend_url}

# Or update your frontend code to use this URL:
const API_BASE_URL = "{backend_url}";
"""
    
    # Write to file
    with open("frontend_config.txt", "w") as f:
        f.write(frontend_config)
    
    print(f"✅ Configuration saved to 'frontend_config.txt'")
    print(f"📋 Next steps:")
    print(f"   1. Copy the backend URL: {backend_url}")
    print(f"   2. Update your Vercel environment variables")
    print(f"   3. Redeploy your frontend")
    print(f"   4. Test the full integration")

if __name__ == "__main__":
    print("🧪 Bioscope Backend Connectivity Test")
    working_url = test_railway_endpoints()
    
    if working_url:
        create_frontend_config(working_url)
