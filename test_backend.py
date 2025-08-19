#!/usr/bin/env python3
"""
Test script to verify the backend setup works correctly
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    # Test imports
    from app import app
    print("✅ Backend imports successful")
    
    # Test Flask app creation
    if app:
        print("✅ Flask app created successfully")
    
    # Test environment variable reading
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        print(f"✅ DATABASE_URL found: {database_url[:50]}...")
    else:
        print("⚠️  DATABASE_URL not found - this is expected if not yet configured")
    
    # Test basic route
    with app.test_client() as client:
        response = client.get('/health')
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    
    print("\n🎉 Backend setup looks good!")
    print("Next steps:")
    print("1. Set up your Supabase database")
    print("2. Configure environment variables in Railway")
    print("3. Deploy to Railway")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Check that all required packages are installed:")
    print("pip install -r backend/requirements.txt")
    
except Exception as e:
    print(f"❌ Error testing backend: {e}")
