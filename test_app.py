#!/usr/bin/env python3
"""
Comprehensive Bioscope Application Testing Script
Tests all major functionality with real data
"""

import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

# Test configurations
BACKEND_URL = "http://localhost:5000"  # Local backend
FRONTEND_URL = "http://localhost:3000"  # Local frontend (if running)

# Test locations in New Jersey
TEST_LOCATIONS = [
    {"name": "Newark, NJ", "input": "Newark, NJ", "expected_lat": 40.7357, "expected_lon": -74.1724},
    {"name": "Princeton, NJ", "input": "Princeton, NJ", "expected_lat": 40.3573, "expected_lon": -74.6672},
    {"name": "Atlantic City, NJ", "input": "Atlantic City, NJ", "expected_lat": 39.3643, "expected_lon": -74.4229},
    {"name": "ZIP Code 07302", "input": "07302", "expected_lat": 40.7178, "expected_lon": -74.0431},
    {"name": "Coordinates", "input": "40.7589, -74.0278", "expected_lat": 40.7589, "expected_lon": -74.0278},
]

TEST_USER = {
    "hotel_name": "Test Eco Lodge",
    "email": "test@ecolodge.com", 
    "password": "testpass123"
}

def test_backend_health():
    """Test if backend is running and healthy"""
    print("🏥 TESTING BACKEND HEALTH...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend not accessible: {e}")
        print("   Make sure your backend is running on port 5000")
        return False

def test_database_connection():
    """Test database connectivity"""
    print("\n🗄️ TESTING DATABASE CONNECTION...")
    try:
        response = requests.get(f"{BACKEND_URL}/db-status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Database connection successful")
            print(f"   PostgreSQL Version: {data.get('postgres_version', 'Unknown')}")
            print(f"   Users table exists: {data.get('users_table_exists', False)}")
            return True
        else:
            print(f"❌ Database connection failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_user_registration():
    """Test user registration"""
    print("\n👤 TESTING USER REGISTRATION...")
    try:
        response = requests.post(
            f"{BACKEND_URL}/register",
            json=TEST_USER,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 201:
            print("✅ User registration successful")
            return True
        elif response.status_code == 400 and "already registered" in response.text:
            print("✅ User already exists (expected)")
            return True
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Registration test failed: {e}")
        return False

def test_user_login():
    """Test user login and session management"""
    print("\n🔐 TESTING USER LOGIN...")
    try:
        session = requests.Session()
        response = session.post(
            f"{BACKEND_URL}/login",
            json={"email": TEST_USER["email"], "password": TEST_USER["password"]},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful")
            print(f"   User: {data.get('user', {}).get('hotel_name', 'Unknown')}")
            
            # Test session status
            session_response = session.get(f"{BACKEND_URL}/session-status")
            if session_response.status_code == 200:
                print("✅ Session validation successful")
                return session
            else:
                print("⚠️ Session validation failed")
                return session
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Login test failed: {e}")
        return None

def test_biodiversity_search(session):
    """Test biodiversity search with real locations"""
    print("\n🔍 TESTING BIODIVERSITY SEARCH...")
    
    if not session:
        print("❌ No valid session for search test")
        return False
    
    success_count = 0
    
    for location in TEST_LOCATIONS:
        print(f"\n   Testing: {location['name']} ({location['input']})")
        try:
            response = session.post(
                f"{BACKEND_URL}/search",
                json={"input_text": location["input"]},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                center = data.get("center", {})
                risks = data.get("risks", [])
                
                print(f"   ✅ Search successful")
                print(f"      📍 Location: {center.get('latitude', 'N/A'):.4f}, {center.get('longitude', 'N/A'):.4f}")
                print(f"      🎯 ZIP Code: {center.get('zipcode', 'N/A')}")
                print(f"      📊 Risk records found: {len(risks)}")
                
                # Analyze risk types found
                risk_types = {}
                for risk in risks:
                    risk_type = risk.get("risk_type", "Unknown")
                    risk_types[risk_type] = risk_types.get(risk_type, 0) + 1
                
                if risk_types:
                    print(f"      🔍 Risk types detected:")
                    for risk_type, count in risk_types.items():
                        print(f"         - {risk_type}: {count} records")
                
                success_count += 1
            else:
                print(f"   ❌ Search failed: {response.status_code}")
                if response.text:
                    print(f"      Error: {response.text}")
                    
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Search request failed: {e}")
        
        time.sleep(1)  # Brief pause between requests
    
    print(f"\n📊 SEARCH TEST SUMMARY: {success_count}/{len(TEST_LOCATIONS)} locations successful")
    return success_count > 0

def test_data_coverage():
    """Test that we have good data coverage in our database"""
    print("\n📈 TESTING DATA COVERAGE...")
    
    test_coordinates = [
        (40.7589, -74.0278),  # New York Harbor area
        (40.3573, -74.6672),  # Princeton area
        (39.3643, -74.4229),  # Atlantic City area
    ]
    
    session = requests.Session()
    coverage_results = []
    
    for lat, lon in test_coordinates:
        print(f"   Testing coverage at {lat:.4f}, {lon:.4f}")
        try:
            response = session.post(
                f"{BACKEND_URL}/search",
                json={"input_text": f"{lat}, {lon}"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                risk_count = len(data.get("risks", []))
                coverage_results.append(risk_count)
                print(f"   ✅ Found {risk_count} risk records")
            else:
                coverage_results.append(0)
                print(f"   ❌ No data found")
                
        except Exception as e:
            coverage_results.append(0)
            print(f"   ❌ Error: {e}")
    
    avg_coverage = sum(coverage_results) / len(coverage_results) if coverage_results else 0
    print(f"📊 Average data coverage: {avg_coverage:.1f} records per location")
    
    return avg_coverage > 0

def test_report_generation(session):
    """Test PDF/Excel report generation"""
    print("\n📄 TESTING REPORT GENERATION...")
    
    if not session:
        print("❌ No valid session for report test")
        return False
    
    # First get some risk data
    search_response = session.post(
        f"{BACKEND_URL}/search",
        json={"input_text": "Newark, NJ"},
        timeout=30
    )
    
    if search_response.status_code != 200:
        print("❌ Could not get data for report test")
        return False
    
    risks = search_response.json().get("risks", [])[:5]  # Use first 5 risks
    
    if not risks:
        print("❌ No risk data available for report generation")
        return False
    
    # Test PDF report
    try:
        pdf_response = session.post(
            f"{BACKEND_URL}/download-report-direct",
            json={"risks": risks, "format": "pdf"},
            timeout=30
        )
        
        if pdf_response.status_code == 200 and pdf_response.headers.get('content-type') == 'application/pdf':
            print("✅ PDF report generation successful")
            print(f"   PDF size: {len(pdf_response.content)} bytes")
        else:
            print("❌ PDF report generation failed")
            
    except Exception as e:
        print(f"❌ PDF report test failed: {e}")
    
    # Test Excel report
    try:
        excel_response = session.post(
            f"{BACKEND_URL}/download-report-direct",
            json={"risks": risks, "format": "excel"},
            timeout=30
        )
        
        if excel_response.status_code == 200:
            print("✅ Excel report generation successful")
            print(f"   Excel size: {len(excel_response.content)} bytes")
            return True
        else:
            print("❌ Excel report generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Excel report test failed: {e}")
        return False

def run_comprehensive_tests():
    """Run all tests in sequence"""
    print("🚀 STARTING COMPREHENSIVE BIOSCOPE APPLICATION TESTS")
    print("=" * 70)
    
    test_results = {}
    
    # 1. Backend Health
    test_results["backend_health"] = test_backend_health()
    
    # 2. Database Connection  
    test_results["database"] = test_database_connection()
    
    # 3. User Registration
    test_results["registration"] = test_user_registration()
    
    # 4. User Login
    session = test_user_login()
    test_results["login"] = session is not None
    
    # 5. Biodiversity Search
    test_results["search"] = test_biodiversity_search(session)
    
    # 6. Data Coverage
    test_results["coverage"] = test_data_coverage()
    
    # 7. Report Generation
    test_results["reports"] = test_report_generation(session)
    
    # Final Summary
    print("\n" + "=" * 70)
    print("🎯 TEST RESULTS SUMMARY")
    print("=" * 70)
    
    passed_tests = 0
    total_tests = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.upper().replace('_', ' ')}: {status}")
        if result:
            passed_tests += 1
    
    print(f"\n📊 OVERALL RESULT: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Your application is ready for production!")
    elif passed_tests >= total_tests * 0.8:
        print("✅ Most tests passed! Your application is nearly ready.")
    else:
        print("⚠️ Several tests failed. Check the issues above before deployment.")
    
    return test_results

if __name__ == "__main__":
    print("Starting Bioscope Application Tests...")
    print("Make sure your backend is running with: python app.py")
    print()
    
    results = run_comprehensive_tests()
