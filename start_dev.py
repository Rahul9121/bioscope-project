#!/usr/bin/env python3
"""
Development startup script for Bioscope backend
Run this locally to start the development server
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

if __name__ == "__main__":
    # Import and run the app
    from backend.app import app
    
    print("🚀 Starting Bioscope Development Server...")
    print("📍 Backend running on: http://localhost:5000")
    print("🔍 Health check: http://localhost:5000/health")
    print("📊 Database status: http://localhost:5000/db-status")
    print("\n💡 Press Ctrl+C to stop the server")
    
    # Run the development server
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('DEBUG', 'true').lower() == 'true'
    )
