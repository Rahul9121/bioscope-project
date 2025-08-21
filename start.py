#!/usr/bin/env python3
"""
Railway deployment start script for Bioscope Flask backend
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("🚀 Starting Bioscope Backend...")
logger.info(f"🐍 Python version: {sys.version}")
logger.info(f"📁 Current directory: {os.getcwd()}")
logger.info(f"🌍 PORT: {os.getenv('PORT')}, DATABASE_URL exists: {bool(os.getenv('DATABASE_URL'))}")

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

logger.info(f"📂 Backend path: {backend_path}")
logger.info(f"🐍 Updated Python path: {sys.path[:3]}")

# Change to backend directory to ensure relative imports work
try:
    os.chdir(backend_path)
    logger.info(f"✅ Changed to backend directory: {os.getcwd()}")
except Exception as e:
    logger.error(f"❌ Failed to change directory: {e}")
    sys.exit(1)

try:
    logger.info("📦 Importing Flask app...")
    from app import app
    logger.info("✅ Flask app imported successfully")
    
    # Verify the app has routes
    logger.info(f"🛣️ App routes: {[rule.rule for rule in app.url_map.iter_rules()][:5]}")
    
    if __name__ == '__main__':
        # Railway automatically provides PORT environment variable
        port = int(os.getenv('PORT', 5000))
        logger.info(f"🌐 Starting server on 0.0.0.0:{port}")
        
        # Use production-ready server settings
        app.run(
            host='0.0.0.0', 
            port=port, 
            debug=False,
            threaded=True,
            use_reloader=False
        )
        
except ImportError as e:
    logger.error(f"❌ Import error: {e}")
    logger.error("📂 Files in backend directory:")
    try:
        for file in os.listdir(backend_path)[:10]:  # Show first 10 files
            logger.error(f"  - {file}")
    except:
        pass
    sys.exit(1)
except Exception as e:
    logger.error(f"❌ Failed to start app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
