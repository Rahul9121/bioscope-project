import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

# Load environment variables (try multiple locations)
try:
    load_dotenv(dotenv_path='../.env')  # Local development
except:
    load_dotenv()  # Default location

# Detect deployment environment
is_railway = bool(os.getenv('RAILWAY_ENVIRONMENT'))
is_render = bool(os.getenv('RENDER'))
is_heroku = bool(os.getenv('DYNO'))
is_production = is_railway or is_render or is_heroku

print("🚀 Starting BiodivProScope Backend (Minimal)...")
print(f"🐍 Python working directory: {os.getcwd()}")
print(f"🌍 Environment: {'Production' if is_production else 'Development'}")
print(f"🔧 Platform: {'Railway' if is_railway else 'Render' if is_render else 'Heroku' if is_heroku else 'Local'}")
print(f"📡 PORT: {os.getenv('PORT')}")

app = Flask(__name__)

# Production CORS Configuration
default_origins = [
    'http://localhost:3000',
    'http://localhost:3001',
    'https://bioscope-project.vercel.app',
    'https://bioscope-project-rahul9121.vercel.app',
    'https://bioscope-project-git-main-rahul9121.vercel.app',
    'https://bioscope-project-git-new-main-rahul9121.vercel.app'
]
allowed_origins_str = os.getenv('ALLOWED_ORIGINS', ','.join(default_origins))
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(',')]
print(f"🌐 CORS allowed origins: {allowed_origins}")

CORS(app, resources={
    r"/*": {
        "origins": allowed_origins,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "expose_headers": ["Content-Type", "Authorization"]
    }
}, supports_credentials=True)

# Basic routes for testing
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy", 
        "message": "Minimal Bioscope API is running",
        "port": os.getenv('PORT', '5001')
    }), 200

@app.route("/test", methods=["GET"])
def test_endpoint():
    return jsonify({
        "message": "Backend connection successful!",
        "timestamp": "2024-08-24",
        "working": True
    }), 200

# Mock authentication endpoints
@app.route("/account/login", methods=["POST", "OPTIONS"])
def mock_login():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    
    data = request.get_json()
    email = data.get('email') if data else None
    
    if email:
        return jsonify({
            "success": True,
            "message": "Login successful (mock)",
            "user": {"email": email, "name": "Test User"},
            "token": "mock-jwt-token"
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Email required"
        }), 400

@app.route("/account/register", methods=["POST", "OPTIONS"])
def mock_register():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    
    data = request.get_json()
    email = data.get('email') if data else None
    
    if email:
        return jsonify({
            "success": True,
            "message": "Registration successful (mock)",
            "user": {"email": email}
        }), 201
    else:
        return jsonify({
            "success": False,
            "message": "Email required"
        }), 400

# Mock location/risk assessment endpoints
@app.route("/locations/search", methods=["POST", "OPTIONS"])
def mock_location_search():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    
    return jsonify({
        "success": True,
        "message": "Location search working (mock)",
        "results": [
            {
                "location": "Sample Location",
                "risk_level": "moderate",
                "species_count": 15
            }
        ]
    }), 200

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5001))
    
    # Configure debug mode based on environment
    debug_mode = not is_production and os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting Flask app on 0.0.0.0:{port}")
    print(f"🔍 Debug mode: {debug_mode}")
    print(f"🌍 Ready for {'production' if is_production else 'development'} use")
    
    # Run the Flask application
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
