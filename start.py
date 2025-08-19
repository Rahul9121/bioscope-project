#!/usr/bin/env python3
"""
Railway deployment start script for Bioscope Flask backend
"""
import os
import sys

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import and run the Flask app
from app import app

if __name__ == '__main__':
    # Railway automatically provides PORT environment variable
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
