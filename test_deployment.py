#!/usr/bin/env python3
"""
Test Bioscope Application Deployment
"""

import requests
import time

def test_deployment():
    frontend_url = 'https://bioscope-project.vercel.app/'
    backend_url = 'https://bioscope-project-production.up.railway.app'

    print('🌐 Testing Bioscope Application Deployment')
    print('=' * 60)

    # Test 1: Frontend accessibility
    print('📱 Testing Frontend...')
    try:
        response = requests.get(frontend_url, timeout=10)
        print(f'   Status: {response.status_code}')
        if response.status_code == 200:
            print(f'   ✅ Frontend is accessible!')
        else:
            print(f'   ⚠️ Frontend status code: {response.status_code}')
    except Exception as e:
        print(f'   ❌ Frontend error: {e}')

    print()

    # Test 2: Backend health
    print('🔧 Testing Backend Health...')
    try:
        response = requests.get(f'{backend_url}/health', timeout=10)
        if response.status_code == 200:
            print(f'   Status: {response.status_code}')
            print(f'   ✅ Backend is running!')
        else:
            print(f'   Status: {response.status_code}')
            print(f'   ⚠️ Backend responding but with issues')
    except Exception as e:
        print(f'   ❌ Backend health error: {e}')

    print()

    # Test 3: Database connection via backend
    print('🗄️ Testing Database Connection...')
    try:
        response = requests.get(f'{backend_url}/db-status', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f'   Status: {response.status_code}')
            print(f'   Database: {data.get("status", "unknown")}')
            if data.get('status') == 'connected':
                print(f'   ✅ Database connected successfully!')
            else:
                print(f'   ⚠️ Database connection issues')
        else:
            print(f'   Status: {response.status_code}')
            print(f'   ⚠️ Database endpoint issues')
    except Exception as e:
        print(f'   ❌ Database status error: {e}')

    print()

    # Test 4: API endpoints
    print('🔍 Testing Key API Endpoints...')
    endpoints_to_test = [
        '/api/biodiversity/search',
        '/api/invasive-species/search', 
        '/api/marine/search'
    ]

    for endpoint in endpoints_to_test:
        try:
            response = requests.get(f'{backend_url}{endpoint}', timeout=10)
            status = '✅' if response.status_code == 200 else '⚠️'
            print(f'   {endpoint:30}: {status} Status {response.status_code}')
        except Exception as e:
            print(f'   {endpoint:30}: ❌ Error - {str(e)[:30]}...')

    print()

    # Test 5: Test specific ZIP code functionality
    print('📍 Testing ZIP Code Risk Assessment...')
    try:
        # Test with a New Jersey ZIP code that should work with your mock data
        test_zip = '07001'
        response = requests.get(f'{backend_url}/api/biodiversity/search', 
                              params={'location': test_zip}, timeout=10)
        status = '✅' if response.status_code == 200 else '⚠️'
        print(f'   ZIP {test_zip} search: {status} Status {response.status_code}')
        
        if response.status_code == 200:
            data = response.json()
            print(f'   Response has {len(data)} risk records')
    except Exception as e:
        print(f'   ❌ ZIP code test error: {e}')

    print()
    print('🎯 Test Summary Complete!')
    print()
    print('💡 If you see any errors above, your mock data fallback should still work')
    print('   Try testing ZIP codes: 07001, 08540, 08701, 08902 on your frontend')

if __name__ == "__main__":
    test_deployment()
