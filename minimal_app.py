#!/usr/bin/env python3
"""
Bioscope Flask Backend - Step 1: Adding Database Support
"""
import os
import sys
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_session import Session
from datetime import timedelta

# Try to import database dependencies
try:
    import psycopg2
    from werkzeug.security import generate_password_hash, check_password_hash
    import requests
    DATABASE_AVAILABLE = True
    print("✅ Database dependencies loaded successfully")
except ImportError as e:
    print(f"⚠️ Database dependencies not available: {e}")
    DATABASE_AVAILABLE = False

# Try to import report generation dependencies
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from flask import send_file
    import io
    import tempfile
    REPORTS_AVAILABLE = True
    print("✅ Report generation dependencies loaded successfully")
except ImportError as e:
    print(f"⚠️ Report generation dependencies not available: {e}")
    REPORTS_AVAILABLE = False

# Constants
GEOCODING_API_URL = "https://nominatim.openstreetmap.org/search"
NJ_BOUNDS = {"north": 41.36, "south": 38.92, "west": -75.58, "east": -73.90}

# Create Flask app
app = Flask(__name__)

# Configure app
app.secret_key = os.getenv('SECRET_KEY', 'dev_secret_key')
app.config.update({
    "SESSION_TYPE": "filesystem",
    "SESSION_PERMANENT": True,
    "PERMANENT_SESSION_LIFETIME": timedelta(minutes=15),
    "SESSION_COOKIE_SAMESITE": "Lax",
    "SESSION_COOKIE_SECURE": False,
    "SESSION_COOKIE_HTTPONLY": True,
})

Session(app)

# CORS setup
allowed_origins = os.getenv('ALLOWED_ORIGINS', 'https://bioscope-project.vercel.app,http://localhost:3000').split(',')
CORS(app, resources={r"/*": {"origins": allowed_origins}}, supports_credentials=True)

# Database connection function
def connect_db():
    """Connect to database if available"""
    if not DATABASE_AVAILABLE:
        return None
    
    try:
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            return None
            
        # Ensure SSL for Supabase
        if 'supabase.com' in database_url and '?sslmode=' not in database_url:
            database_url += '?sslmode=require'
            
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

# Geocoding helper functions
def get_lat_lon_from_zip(zipcode):
    """Get coordinates from ZIP code"""
    try:
        response = requests.get(
            GEOCODING_API_URL,
            params={"postalcode": zipcode, "countrycodes": "us", "format": "json"},
            headers={"User-Agent": "BiodivProScopeApp/1.0"}
        )

        if response.status_code == 200 and response.json():
            data = response.json()[0]
            latitude = float(data["lat"])
            longitude = float(data["lon"])
            return latitude, longitude
        else:
            return 40.0583, -74.4057  # Default coordinates for New Jersey

    except Exception as e:
        print(f"Error fetching ZIP code data: {e}")
        return 40.0583, -74.4057  # Default fallback coordinates

def get_lat_lon_from_address(address):
    """Get coordinates from address string"""
    try:
        response = requests.get(
            GEOCODING_API_URL,
            params={"q": address, "countrycodes": "us", "format": "json"},
            headers={"User-Agent": "BiodivProScopeApp/1.0"}
        )

        if response.status_code == 200 and response.json():
            data = response.json()[0]
            latitude = float(data["lat"])
            longitude = float(data["lon"])
            # Extract ZIP code from display name
            address_parts = data.get("display_name", "").split(",")
            zip_code = address_parts[-2].strip() if len(address_parts) > 1 else "Unknown"
            return latitude, longitude, zip_code
        else:
            return None, None, None

    except Exception as e:
        print(f"Error fetching address data: {e}")
        return None, None, None

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
        "database_available": DATABASE_AVAILABLE,
        "environment_vars": {
            "PORT": os.getenv('PORT'),
            "DATABASE_URL_EXISTS": bool(os.getenv('DATABASE_URL')),
            "SECRET_KEY_EXISTS": bool(os.getenv('SECRET_KEY'))
        }
    })

@app.route("/db-status", methods=["GET"])
def db_status():
    """Check database connection status"""
    if not DATABASE_AVAILABLE:
        return jsonify({
            "status": "error",
            "message": "Database dependencies not installed"
        }), 500
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({
                "status": "error", 
                "message": "Cannot connect to database",
                "database_url_exists": bool(os.getenv('DATABASE_URL'))
            }), 500
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        # Check if users table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'users'
            );
        """)
        users_table_exists = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "status": "connected",
            "postgres_version": version[0] if version else "unknown",
            "users_table_exists": users_table_exists,
            "database_url_configured": bool(os.getenv('DATABASE_URL'))
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "database_url_configured": bool(os.getenv('DATABASE_URL'))
        }), 500

@app.route("/init-db", methods=["GET"])
def init_database():
    """Initialize database tables"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database dependencies not available"}), 500
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Failed to connect to database"}), 500
        
        cursor = conn.cursor()
        
        # Create users table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                hotel_name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Database initialized successfully"}), 200
        
    except Exception as e:
        return jsonify({"error": f"Database initialization failed: {str(e)}"}), 500

# User Authentication Routes
@app.route('/register', methods=['POST', 'OPTIONS'])
def register():
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS preflight successful"}), 200
    
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database not available"}), 500

    try:
        data = request.json
        hotel_name = data.get('hotel_name')
        email = data.get('email')
        password = data.get('password')

        # Validate required fields
        if not hotel_name or not email or not password:
            return jsonify({"error": "All fields are required."}), 400

        # Validate password strength
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long."}), 400

        # Connect to database
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Failed to connect to the database."}), 500

        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"error": "Email is already registered."}), 400

        # Hash password and create user
        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (hotel_name, email, password_hash) VALUES (%s, %s, %s)",
            (hotel_name, email, hashed_password)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Registration successful!"}), 201

    except Exception as e:
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

@app.route('/login', methods=['POST'])
def login():
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database not available"}), 500
    
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required."}), 400

        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Failed to connect to the database."}), 500
            
        cursor = conn.cursor()
        cursor.execute("SELECT id, hotel_name, email, password_hash FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            cursor.close()
            conn.close()
            return jsonify({"error": "Invalid email or password"}), 401

        user_id, hotel_name, user_email, hashed_password = user

        if not check_password_hash(hashed_password, password):
            cursor.close()
            conn.close()
            return jsonify({"error": "Invalid email or password"}), 401

        # Set session
        session['user_id'] = user_id
        session['email'] = email
        session.permanent = True

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user_id,
                "hotel_name": hotel_name,
                "email": user_email
            }
        }), 200

    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}"}), 500

@app.route('/logout', methods=['POST', 'OPTIONS'])
def logout():
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS preflight success"}), 200

    session.clear()
    return jsonify({"message": "Logout successful"}), 200

@app.route('/session-status', methods=['GET'])
def session_status():
    if 'user_id' in session:
        return jsonify({"active": True, "message": "Session is active"}), 200
    return jsonify({"active": False, "message": "Session expired"}), 401

# Location and Search Routes
@app.route("/address-autocomplete", methods=["GET"])
def address_autocomplete():
    """Address autocomplete for search"""
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify([])

    try:
        response = requests.get(
            GEOCODING_API_URL,
            params={"q": query, "countrycodes": "us", "format": "json", "limit": 5},
            headers={"User-Agent": "BiodivProScopeApp/1.0"}
        )

        if response.status_code == 200:
            suggestions = [
                {"display_name": item.get("display_name", "")}
                for item in response.json()
                if "New Jersey" in item.get("display_name", "")
            ]
            return jsonify(suggestions)
        else:
            return jsonify([])
    except Exception as e:
        print(f"Error fetching autocomplete data: {e}")
        return jsonify([])

@app.route("/search", methods=["POST"])
def search():
    """Main search endpoint for location-based risk analysis"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database not available"}), 500
    
    try:
        data = request.json
        input_text = data.get("input_text")
        
        if not input_text:
            return jsonify({"error": "Input text is required"}), 400
        
        lat, lon, zip_code = None, None, ""
        
        # Determine if input is coordinates, ZIP code, or address
        if input_text.replace(",", "").replace(".", "").replace(" ", "").isdigit():
            if "," in input_text:
                # Coordinates input
                lat, lon = map(float, input_text.split(","))
                zip_code = "Unknown"
            elif len(input_text) == 5:
                # ZIP code input
                lat, lon = get_lat_lon_from_zip(input_text)
                zip_code = input_text
        else:
            # Address input
            lat, lon, zip_code = get_lat_lon_from_address(input_text)
        
        if lat is None or lon is None:
            return jsonify({"error": "Could not determine location."}), 400
        
        # Check if location is within New Jersey bounds
        if not (NJ_BOUNDS["south"] <= lat <= NJ_BOUNDS["north"] and 
                NJ_BOUNDS["west"] <= lon <= NJ_BOUNDS["east"]):
            return jsonify({"error": "The location is outside of New Jersey."}), 400
        
        # For now, return basic location info (we'll add risk data in next step)
        # This simulates risk data without requiring all the database tables
        sample_risks = [
            {
                "latitude": lat + 0.01,
                "longitude": lon + 0.01,
                "risk_type": "Sample Risk",
                "description": "This is sample risk data for testing",
                "threat_code": "moderate"
            }
        ]
        
        # Store in session for later use
        session["risks"] = sample_risks
        session["last_search"] = {"lat": lat, "lon": lon, "zip": zip_code}
        
        return jsonify({
            "center": {
                "latitude": lat,
                "longitude": lon,
                "zipcode": zip_code
            },
            "risks": sample_risks,
            "message": "Location found successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

@app.route("/session-risks", methods=["GET"])
def get_session_risks():
    """Get risks from current session"""
    return jsonify({"risks": session.get("risks", [])})

# Report Generation Routes
@app.route("/download-report-direct", methods=["POST"])
def download_report_direct():
    """Generate and download biodiversity risk reports"""
    if not REPORTS_AVAILABLE:
        return jsonify({"error": "Report generation not available"}), 500
    
    try:
        data = request.get_json()
        risks = data.get("risks", [])
        file_format = data.get("format", "pdf")
        
        if not risks:
            # Use session risks if no risks provided
            risks = session.get("risks", [])
            
        if not risks:
            return jsonify({"error": "No risks data available for report."}), 400
        
        if file_format == "pdf":
            # Create PDF report
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter
            
            # PDF Header
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, "Biodiversity Risk Assessment Report")
            c.setFont("Helvetica", 10)
            c.drawString(50, height - 70, f"Generated from BiodivProScope - {len(risks)} risk(s) identified")
            
            # Add search location info if available
            last_search = session.get("last_search", {})
            if last_search:
                c.drawString(50, height - 90, f"Location: {last_search.get('zip', 'Unknown')} ({last_search.get('lat', 'N/A')}, {last_search.get('lon', 'N/A')})")
            
            c.setFont("Helvetica", 12)
            y = height - 130
            
            # Add risks to PDF
            for idx, risk in enumerate(risks[:20]):  # Limit to 20 risks for PDF
                if y < 100:  # Start new page if needed
                    c.showPage()
                    y = height - 50
                
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, y, f"{idx + 1}. {risk.get('risk_type', 'Unknown Risk')}")
                y -= 20
                
                c.setFont("Helvetica", 10)
                c.drawString(70, y, f"Threat Level: {risk.get('threat_code', 'unknown').title()}")
                y -= 15
                
                description = risk.get('description', 'No description available')
                # Wrap long descriptions
                if len(description) > 80:
                    description = description[:80] + "..."
                c.drawString(70, y, f"Description: {description}")
                y -= 15
                
                c.drawString(70, y, f"Location: ({risk.get('latitude', 'N/A')}, {risk.get('longitude', 'N/A')})")
                y -= 25
            
            c.save()
            buffer.seek(0)
            
            return send_file(
                io.BytesIO(buffer.read()),
                mimetype='application/pdf',
                as_attachment=True,
                download_name='biodiversity_risk_report.pdf'
            )
            
        else:
            return jsonify({"error": "Only PDF format supported currently"}), 400
            
    except Exception as e:
        print(f"Report generation error: {e}")
        return jsonify({"error": f"Failed to generate report: {str(e)}"}), 500

@app.route("/generate-report", methods=["POST"])
def generate_report():
    """Generate report from session data or provided risks"""
    if not REPORTS_AVAILABLE:
        return jsonify({"error": "Report generation not available"}), 500
    
    try:
        # Get risks from session or request
        risks = session.get("risks", [])
        search_info = session.get("last_search", {})
        
        if not risks:
            return jsonify({"error": "No risk data available. Please perform a search first."}), 400
        
        return jsonify({
            "message": "Report ready for generation",
            "risks_count": len(risks),
            "location": search_info,
            "available_formats": ["pdf"]
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Report preparation failed: {str(e)}"}), 500

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
