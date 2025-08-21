#!/usr/bin/env python3
"""
Comprehensive Backend Testing Script for Bioscope Project
Tests all API endpoints and functionality to ensure everything works properly.
"""

import requests
import json
import time
import random
import string
from datetime import datetime

# Backend URL - Update this if different
BACKEND_URL = "https://bioscope-project-production.up.railway.app"

class BackendTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.test_user_email = f"test_{self.generate_random_string(6)}@example.com"
        self.test_user_password = "TestPassword123!"
        
    def generate_random_string(self, length):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def log_test(self, test_name, success, message, details=None):
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {test_name}: {message}")
        if details:
            print(f"    Details: {details}")
        print()
    
    def test_health_check(self):
        """Test the health check endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    self.log_test("Health Check", True, "Backend is healthy", data)
                else:
                    self.log_test("Health Check", False, "Unexpected health status", data)
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Health Check", False, f"Request failed: {str(e)}")
    
    def test_database_status(self):
        """Test the database connection status"""
        try:
            response = self.session.get(f"{self.base_url}/db-status")
            if response.status_code == 200:
                data = response.json()
                if data.get("database") == "connected":
                    self.log_test("Database Status", True, "Database connected successfully", data)
                else:
                    self.log_test("Database Status", False, "Database not connected", data)
            else:
                self.log_test("Database Status", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Database Status", False, f"Request failed: {str(e)}")
    
    def test_user_registration(self):
        """Test user registration"""
        try:
            user_data = {
                "email": self.test_user_email,
                "password": self.test_user_password,
                "confirm_password": self.test_user_password
            }
            
            response = self.session.post(f"{self.base_url}/register", json=user_data)
            if response.status_code == 201:
                data = response.json()
                if data.get("success"):
                    self.log_test("User Registration", True, "User registered successfully", data)
                else:
                    self.log_test("User Registration", False, "Registration failed", data)
            else:
                self.log_test("User Registration", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("User Registration", False, f"Request failed: {str(e)}")
    
    def test_user_login(self):
        """Test user login"""
        try:
            login_data = {
                "email": self.test_user_email,
                "password": self.test_user_password
            }
            
            response = self.session.post(f"{self.base_url}/login", json=login_data)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("User Login", True, "User logged in successfully", data)
                else:
                    self.log_test("User Login", False, "Login failed", data)
            else:
                self.log_test("User Login", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("User Login", False, f"Request failed: {str(e)}")
    
    def test_session_status(self):
        """Test session status check"""
        try:
            response = self.session.get(f"{self.base_url}/session")
            if response.status_code == 200:
                data = response.json()
                if data.get("logged_in"):
                    self.log_test("Session Status", True, "Session active", data)
                else:
                    self.log_test("Session Status", False, "No active session", data)
            else:
                self.log_test("Session Status", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Session Status", False, f"Request failed: {str(e)}")
    
    def test_address_autocomplete(self):
        """Test address autocomplete functionality"""
        try:
            test_queries = [
                "New York",
                "Princeton, NJ",
                "Newark",
                "Atlantic City"
            ]
            
            for query in test_queries:
                response = self.session.get(f"{self.base_url}/autocomplete", params={"q": query})
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        self.log_test(f"Autocomplete '{query}'", True, f"Found {len(data)} suggestions", data[:2])
                    else:
                        self.log_test(f"Autocomplete '{query}'", False, "No suggestions found", data)
                else:
                    self.log_test(f"Autocomplete '{query}'", False, f"HTTP {response.status_code}", response.text)
                    
                time.sleep(0.5)  # Rate limiting
        except Exception as e:
            self.log_test("Address Autocomplete", False, f"Request failed: {str(e)}")
    
    def test_location_search(self):
        """Test location-based biodiversity search"""
        try:
            test_locations = [
                {"lat": 40.7128, "lng": -74.0060, "name": "New York City"},
                {"lat": 40.3573, "lng": -74.6672, "name": "Princeton, NJ"},
                {"lat": 39.7391, "lng": -104.9847, "name": "Denver, CO"},
                {"lat": 39.3643, "lng": -74.4229, "name": "Atlantic City, NJ"}
            ]
            
            for location in test_locations:
                search_data = {
                    "latitude": location["lat"],
                    "longitude": location["lng"],
                    "radius": 50  # 50km radius
                }
                
                response = self.session.post(f"{self.base_url}/search", json=search_data)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        risks = data.get("risks", {})
                        species_count = len(data.get("species", []))
                        self.log_test(f"Search {location['name']}", True, 
                                    f"Found {species_count} species, Risk levels: {risks}", 
                                    {"species_count": species_count, "risks": risks})
                    else:
                        self.log_test(f"Search {location['name']}", False, "Search failed", data)
                else:
                    self.log_test(f"Search {location['name']}", False, f"HTTP {response.status_code}", response.text)
                    
                time.sleep(1)  # Rate limiting
        except Exception as e:
            self.log_test("Location Search", False, f"Request failed: {str(e)}")
    
    def test_report_generation(self):
        """Test PDF report generation"""
        try:
            report_data = {
                "location": "Princeton, NJ",
                "latitude": 40.3573,
                "longitude": -74.6672,
                "risks": {
                    "invasive_species": "Medium",
                    "freshwater": "Low",
                    "marine": "Low",
                    "terrestrial": "Medium",
                    "iucn_species": "High"
                },
                "species": [
                    {"common_name": "Norway Maple", "scientific_name": "Acer platanoides", "threat_level": "Medium"},
                    {"common_name": "House Sparrow", "scientific_name": "Passer domesticus", "threat_level": "Low"}
                ]
            }
            
            response = self.session.post(f"{self.base_url}/generate-report", json=report_data)
            if response.status_code == 200:
                # Check if it's a PDF by looking at content type
                content_type = response.headers.get('content-type', '')
                if 'application/pdf' in content_type:
                    pdf_size = len(response.content)
                    self.log_test("Report Generation", True, f"PDF generated successfully ({pdf_size} bytes)")
                else:
                    # It might be JSON response
                    try:
                        data = response.json()
                        if data.get("success"):
                            self.log_test("Report Generation", True, "Report generated", data)
                        else:
                            self.log_test("Report Generation", False, "Report generation failed", data)
                    except:
                        self.log_test("Report Generation", False, "Unexpected response format", content_type)
            else:
                self.log_test("Report Generation", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Report Generation", False, f"Request failed: {str(e)}")
    
    def test_data_integrity(self):
        """Test that real biodiversity data is properly loaded"""
        try:
            # Test a search in New Jersey where we know we have data
            search_data = {
                "latitude": 40.0583,
                "longitude": -74.4057,
                "radius": 25
            }
            
            response = self.session.post(f"{self.base_url}/search", json=search_data)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    species = data.get("species", [])
                    risks = data.get("risks", {})
                    
                    # Check if we have real species data (not just sample data)
                    has_real_data = len(species) > 0 and any(
                        sp.get("scientific_name") not in ["Acer platanoides", "Passer domesticus", "Gambusia affinis"] 
                        for sp in species
                    )
                    
                    if has_real_data:
                        self.log_test("Data Integrity", True, 
                                    f"Real biodiversity data loaded: {len(species)} species found", 
                                    {"sample_species": species[:3], "risks": risks})
                    else:
                        self.log_test("Data Integrity", False, 
                                    "Only sample data found, real data may not be loaded properly",
                                    {"species": species})
                else:
                    self.log_test("Data Integrity", False, "Search failed", data)
            else:
                self.log_test("Data Integrity", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("Data Integrity", False, f"Request failed: {str(e)}")
    
    def test_user_logout(self):
        """Test user logout"""
        try:
            response = self.session.post(f"{self.base_url}/logout")
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("User Logout", True, "User logged out successfully", data)
                else:
                    self.log_test("User Logout", False, "Logout failed", data)
            else:
                self.log_test("User Logout", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_test("User Logout", False, f"Request failed: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting Comprehensive Backend Testing...")
        print(f"Backend URL: {self.base_url}")
        print(f"Test User: {self.test_user_email}")
        print("="*60)
        print()
        
        # Basic connectivity tests
        print("📡 TESTING BASIC CONNECTIVITY")
        print("-" * 30)
        self.test_health_check()
        self.test_database_status()
        
        # Authentication tests
        print("🔐 TESTING USER AUTHENTICATION")
        print("-" * 30)
        self.test_user_registration()
        self.test_user_login()
        self.test_session_status()
        
        # Search functionality tests
        print("🔍 TESTING SEARCH FUNCTIONALITY")
        print("-" * 30)
        self.test_address_autocomplete()
        self.test_location_search()
        
        # Report generation test
        print("📊 TESTING REPORT GENERATION")
        print("-" * 30)
        self.test_report_generation()
        
        # Data integrity test
        print("🔬 TESTING DATA INTEGRITY")
        print("-" * 30)
        self.test_data_integrity()
        
        # Cleanup
        print("🧹 CLEANUP")
        print("-" * 30)
        self.test_user_logout()
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("="*60)
        print("📋 TEST SUMMARY")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        if failed_tests > 0:
            print("❌ FAILED TESTS:")
            print("-" * 20)
            for result in self.test_results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['message']}")
            print()
        
        print("✅ PASSED TESTS:")
        print("-" * 20)
        for result in self.test_results:
            if result["success"]:
                print(f"  • {result['test']}: {result['message']}")
        
        print()
        print("🎉 Testing Complete!")
        
        # Save results to file
        with open("backend_test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        print(f"📁 Detailed results saved to: backend_test_results.json")

if __name__ == "__main__":
    tester = BackendTester(BACKEND_URL)
    tester.run_all_tests()
