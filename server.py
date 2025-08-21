#!/usr/bin/env python3
"""
Ultra-simple Railway entry point for Bioscope Flask backend
"""
import os
import sys

# Minimal setup for Railway
print("🚀 Ultra-simple Railway entry point")
print(f"Current dir: {os.getcwd()}")

# Set environment
os.environ.setdefault('FLASK_ENV', 'production')

# Move to backend and start
try:
    os.chdir('backend')
    print(f"Changed to: {os.getcwd()}")
    
    # Simple import and run
    from app import app
    
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting on port {port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
