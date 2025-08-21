#!/usr/bin/env python3
"""
Railway deployment start script for Bioscope Flask backend
"""
import os
import sys

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

# Change to backend directory to ensure relative imports work
os.chdir(backend_path)

print(f"🚀 Starting from: {os.getcwd()}")
print(f"🐍 Python path: {sys.path[:3]}")

try:
    # Import and run the Flask app
    from app import app
    
    if __name__ == '__main__':
        # Railway automatically provides PORT environment variable
        port = int(os.getenv('PORT', 5000))
        print(f"🌐 Starting server on 0.0.0.0:{port}")
        app.run(host='0.0.0.0', port=port, debug=False)
except Exception as e:
    print(f"❌ Failed to start app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
