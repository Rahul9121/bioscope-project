#!/usr/bin/env python3
"""
Railway deployment main script for Bioscope Flask backend
This is the root entry point that Railway will use
"""
import os
import sys

print("🚀 Railway Main Entry Point")
print(f"📁 Current directory: {os.getcwd()}")
print(f"🗂️ Directory contents: {os.listdir('.')[:10]}")

# Check if we're in the right directory
if 'backend' not in os.listdir('.'):
    print("❌ Backend directory not found!")
    sys.exit(1)

# Add backend to Python path and change directory
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)

print(f"✅ Changed to backend directory: {os.getcwd()}")

try:
    # Import Flask app
    from app import app
    
    if __name__ == '__main__':
        port = int(os.getenv('PORT', 5000))
        print(f"🌐 Starting on 0.0.0.0:{port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
except Exception as e:
    print(f"❌ Failed to start: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
