#!/usr/bin/env python3
"""
Minimal Flask app to test Railway deployment
This removes all complex dependencies and database connections
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS

# Create minimal Flask app
app = Flask(__name__)

# Simple CORS setup
CORS(app, origins="*")

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "message": "Bioscope Backend is running!",
        "status": "healthy",
        "port": os.getenv('PORT', 'unknown'),
        "environment": os.getenv('FLASK_ENV', 'unknown')
    })

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy", 
        "message": "Bioscope API is running",
        "port": os.getenv('PORT', 'unknown')
    }), 200

@app.route("/test", methods=["GET"])
def test():
    return jsonify({
        "message": "Test endpoint working",
        "environment_vars": {
            "PORT": os.getenv('PORT'),
            "DATABASE_URL_EXISTS": bool(os.getenv('DATABASE_URL')),
            "SECRET_KEY_EXISTS": bool(os.getenv('SECRET_KEY'))
        }
    })

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    print(f"🚀 Starting minimal Flask app on 0.0.0.0:{port}")
    
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False,
            threaded=True,
            use_reloader=False
        )
    except Exception as e:
        print(f"❌ Failed to start: {e}")
        import traceback
        traceback.print_exc()
