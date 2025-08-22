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

# Configure app for production
app.secret_key = os.getenv('SECRET_KEY', 'bioscope_production_secret_key_2024')

# Production-optimized session configuration
app.config.update({
    "SESSION_TYPE": "sqlalchemy",
    "SESSION_PERMANENT": True,
    "PERMANENT_SESSION_LIFETIME": timedelta(hours=24),  # Longer session for better UX
    "SESSION_COOKIE_SAMESITE": None,  # Allow cross-site cookies
    "SESSION_COOKIE_SECURE": True if os.getenv('FLASK_ENV') == 'production' else False,
    "SESSION_COOKIE_HTTPONLY": False,  # Allow JavaScript access for debugging
    "SESSION_COOKIE_NAME": "bioscope_session",
    "SESSION_USE_SIGNER": True,
    "SESSION_KEY_PREFIX": "bioscope:",
    "SESSION_SQLALCHEMY_TABLE": "user_sessions",
})

# Fallback to filesystem if database not available
try:
    from flask_sqlalchemy import SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', '').replace('postgresql://', 'postgresql+psycopg2://')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    app.config['SESSION_SQLALCHEMY'] = db
    Session(app)
    print("✅ Using database-backed sessions")
except Exception as e:
    print(f"⚠️ Database sessions failed, using filesystem: {e}")
    app.config.update({
        "SESSION_TYPE": "filesystem",
        "SESSION_FILE_DIR": "/tmp/flask_session",
        "SESSION_FILE_THRESHOLD": 100,
    })
    # Create session directory
    import tempfile
    os.makedirs("/tmp/flask_session", exist_ok=True)
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

# Biodiversity risk helper functions
def standardize_threat_status(status):
    """Standardize IUCN threat status to threat codes"""
    if not status:
        return "low"
    
    status = status.lower().strip()
    mapping = {
        "critically endangered": "high",
        "endangered": "high", 
        "vulnerable": "moderate",
        "near threatened": "moderate",
        "least concern": "low",
        "data deficient": "low",
        "not evaluated": "low"
    }
    return mapping.get(status, "low")

def calculate_risk_from_hci(hci_value, hci_type="general"):
    """Calculate risk level from HCI (Human-Coexistence Index) value"""
    if hci_value is None:
        return "low", 0.1
    
    # Different thresholds for different HCI types
    if hci_type == "marine":
        if hci_value >= 0.75:
            return "high", min(hci_value, 1.0)
        elif hci_value >= 0.4:
            return "moderate", hci_value
        else:
            return "low", hci_value
    else:
        # Terrestrial and freshwater
        if hci_value >= 2.0:
            return "high", min(hci_value / 3.0, 1.0)
        elif hci_value >= 1.5:
            return "moderate", hci_value / 3.0
        else:
            return "low", max(hci_value / 3.0, 0.1)

def query_biodiversity_risks(lat, lon, search_radius=0.1):
    """Query all types of biodiversity risks around a location"""
    if not DATABASE_AVAILABLE:
        return []
    
    conn = connect_db()
    if conn is None:
        return []
    
    cursor = conn.cursor()
    risk_data = []
    
    try:
        # Query invasive species (handle potential missing scientific_name column)
        try:
            cursor.execute("""
                SELECT latitude, longitude, common_name, scientific_name, threat_code 
                FROM invasive_species 
                WHERE ABS(latitude - %s) <= %s AND ABS(longitude - %s) <= %s
            """, (lat, search_radius, lon, search_radius))
            
            for row in cursor.fetchall():
                risk_data.append({
                    "latitude": float(row[0]) if row[0] else lat,
                    "longitude": float(row[1]) if row[1] else lon,
                    "risk_type": "Invasive Species",
                    "description": f"{row[2]} ({row[3] if row[3] else 'Unknown scientific name'})",
                    "threat_code": row[4] or "low",
                    "source": "invasive_species"
                })
        except:
            # Fallback query without scientific_name column
            cursor.execute("""
                SELECT latitude, longitude, common_name, threat_code 
                FROM invasive_species 
                WHERE ABS(latitude - %s) <= %s AND ABS(longitude - %s) <= %s
            """, (lat, search_radius, lon, search_radius))
            
            for row in cursor.fetchall():
                risk_data.append({
                    "latitude": float(row[0]) if row[0] else lat,
                    "longitude": float(row[1]) if row[1] else lon,
                    "risk_type": "Invasive Species",
                    "description": f"{row[2]}",
                    "threat_code": row[3] or "low",
                    "source": "invasive_species"
                })
        
        # Query IUCN endangered species (handle potential missing habitat column)
        try:
            cursor.execute("""
                SELECT latitude, longitude, species_name, threat_status, habitat 
                FROM iucn_data 
                WHERE ABS(latitude - %s) <= %s AND ABS(longitude - %s) <= %s
            """, (lat, search_radius, lon, search_radius))
            
            for row in cursor.fetchall():
                threat_code = standardize_threat_status(row[3])
                risk_data.append({
                    "latitude": float(row[0]) if row[0] else lat,
                    "longitude": float(row[1]) if row[1] else lon,
                    "risk_type": "Endangered Species",
                    "description": f"{row[2]} ({row[3]}) in {row[4] if row[4] else 'Unknown habitat'}",
                    "threat_code": threat_code,
                    "source": "iucn_data"
                })
        except Exception as e:
            print(f"Error querying IUCN data with habitat column: {e}")
            # Fallback query without habitat column
            try:
                cursor.execute("""
                    SELECT latitude, longitude, species_name, threat_status 
                    FROM iucn_data 
                    WHERE ABS(latitude - %s) <= %s AND ABS(longitude - %s) <= %s
                """, (lat, search_radius, lon, search_radius))
                
                for row in cursor.fetchall():
                    threat_code = standardize_threat_status(row[3])
                    risk_data.append({
                        "latitude": float(row[0]) if row[0] else lat,
                        "longitude": float(row[1]) if row[1] else lon,
                        "risk_type": "Endangered Species",
                        "description": f"{row[2]} ({row[3]})",
                        "threat_code": threat_code,
                        "source": "iucn_data"
                    })
            except Exception as e2:
                print(f"Error querying IUCN data without habitat column: {e2}")
        
        # Query freshwater risks (handle potential missing columns)
        try:
            cursor.execute("""
                SELECT x, y, normalized_risk, risk_level 
                FROM freshwater_risk 
                WHERE ABS(y - %s) <= %s AND ABS(x - %s) <= %s
            """, (lat, search_radius, lon, search_radius))
            
            for row in cursor.fetchall():
                normalized_risk = float(row[2]) if row[2] else 0.5
                risk_level_db = row[3] if row[3] else "Low"
                risk_level, _ = calculate_risk_from_hci(normalized_risk, "freshwater")
                risk_data.append({
                    "latitude": float(row[1]) if row[1] else lat,
                    "longitude": float(row[0]) if row[0] else lon,
                    "risk_type": "Freshwater Ecosystem Risk",
                    "description": f"Normalized Risk: {normalized_risk:.2f}, Risk Level: {risk_level_db}",
                    "threat_code": risk_level,
                    "source": "freshwater_risk"
                })
        except Exception as e:
            print(f"Error querying freshwater risks: {e}")
        
        # Query marine risks
        cursor.execute("""
            SELECT x, y, marine_hci 
            FROM marine_hci 
            WHERE ABS(y - %s) <= %s AND ABS(x - %s) <= %s
        """, (lat, search_radius, lon, search_radius))
        
        for row in cursor.fetchall():
            hci_value = float(row[2]) if row[2] else 0.1
            risk_level, normalized_risk = calculate_risk_from_hci(hci_value, "marine")
            risk_data.append({
                "latitude": float(row[1]) if row[1] else lat,
                "longitude": float(row[0]) if row[0] else lon,
                "risk_type": "Marine Ecosystem Risk",
                "description": f"Marine HCI: {hci_value:.2f}, Human-coexistence impact level: {risk_level}",
                "threat_code": risk_level,
                "source": "marine_hci"
            })
        
        # Query terrestrial risks (handle potential missing columns)
        try:
            cursor.execute("""
                SELECT x, y, normalized_risk, risk_level 
                FROM terrestrial_risk 
                WHERE ABS(y - %s) <= %s AND ABS(x - %s) <= %s
            """, (lat, search_radius, lon, search_radius))
            
            for row in cursor.fetchall():
                normalized_risk = float(row[2]) if row[2] else 0.5
                risk_level_db = row[3] if row[3] else "low"
                risk_level, _ = calculate_risk_from_hci(normalized_risk, "terrestrial")
                risk_data.append({
                    "latitude": float(row[1]) if row[1] else lat,
                    "longitude": float(row[0]) if row[0] else lon,
                    "risk_type": "Terrestrial Ecosystem Risk",
                    "description": f"Normalized Risk: {normalized_risk:.2f}, Risk Level: {risk_level_db}",
                    "threat_code": risk_level_db.lower() if risk_level_db else risk_level,
                    "source": "terrestrial_risk"
                })
        except Exception as e:
            print(f"Error querying terrestrial risks: {e}")
        
    except Exception as e:
        print(f"Error querying biodiversity risks: {e}")
    finally:
        cursor.close()
        conn.close()
    
    return risk_data

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
    """Initialize database tables with biodiversity data"""
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
        
        # Create biodiversity tables
        # 1. Invasive Species table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invasive_species (
                id SERIAL PRIMARY KEY,
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                common_name VARCHAR(255),
                scientific_name VARCHAR(255),
                threat_code VARCHAR(50) DEFAULT 'low'
            );
        """)
        
        # 2. IUCN Data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS iucn_data (
                id SERIAL PRIMARY KEY,
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                species_name VARCHAR(255),
                threat_status VARCHAR(100),
                habitat VARCHAR(255)
            );
        """)
        
        # 3. Freshwater Risk table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS freshwater_risk (
                id SERIAL PRIMARY KEY,
                x DECIMAL(11, 8),
                y DECIMAL(10, 8),
                freshwater_hci DECIMAL(10, 6),
                normalized_risk DECIMAL(5, 3),
                risk_level VARCHAR(50) DEFAULT 'Low'
            );
        """)
        
        # 4. Marine HCI table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS marine_hci (
                id SERIAL PRIMARY KEY,
                x DECIMAL(11, 8),
                y DECIMAL(10, 8),
                marine_hci DECIMAL(5, 3) DEFAULT 0.0
            );
        """)
        
        # 5. Terrestrial Risk table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS terrestrial_risk (
                id SERIAL PRIMARY KEY,
                x DECIMAL(11, 8),
                y DECIMAL(10, 8),
                terrestrial_hci DECIMAL(10, 6),
                normalized_risk DECIMAL(5, 3),
                risk_level VARCHAR(50) DEFAULT 'low'
            );
        """)
        
        # 6. Hotel Locations table (for location management)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hotel_locations (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                hotel_name VARCHAR(255) NOT NULL,
                street_address VARCHAR(255) NOT NULL,
                city VARCHAR(100) NOT NULL,
                zip_code VARCHAR(10) NOT NULL,
                email VARCHAR(255) NOT NULL,
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Add missing columns to existing tables if needed
        try:
            cursor.execute("ALTER TABLE invasive_species ADD COLUMN IF NOT EXISTS scientific_name VARCHAR(255);")
        except:
            pass  # Column might already exist
        
        
        # Skip data insertion for now due to schema conflicts
        # The existing database already has invasive species data
        print("Database tables created/verified successfully")
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_invasive_species_location ON invasive_species(latitude, longitude);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_iucn_data_location ON iucn_data(latitude, longitude);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_freshwater_risk_location ON freshwater_risk(x, y);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_marine_hci_location ON marine_hci(x, y);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_terrestrial_risk_location ON terrestrial_risk(x, y);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_hotel_locations_user ON hotel_locations(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_hotel_locations_coords ON hotel_locations(latitude, longitude);")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Database and biodiversity tables initialized successfully"}), 200
        
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
        
        # Query real biodiversity risks from database
        print(f"🔍 Searching biodiversity risks around lat: {lat}, lon: {lon}")
        biodiversity_risks = query_biodiversity_risks(lat, lon, search_radius=0.1)
        
        # If no risks found in immediate area, expand search radius
        if not biodiversity_risks:
            print("🔍 Expanding search radius to 0.2 degrees")
            biodiversity_risks = query_biodiversity_risks(lat, lon, search_radius=0.2)
        
        # If still no risks, provide general New Jersey biodiversity info
        if not biodiversity_risks:
            biodiversity_risks = [
                {
                    "latitude": lat,
                    "longitude": lon,
                    "risk_type": "General New Jersey Biodiversity",
                    "description": "This area may contain undocumented biodiversity risks. Consider general conservation practices.",
                    "threat_code": "low",
                    "source": "general"
                }
            ]
        
        # Store in session for later use
        session["risks"] = biodiversity_risks
        session["last_search"] = {"lat": lat, "lon": lon, "zip": zip_code}
        
        print(f"✅ Found {len(biodiversity_risks)} biodiversity risks")
        
        return jsonify({
            "center": {
                "latitude": lat,
                "longitude": lon,
                "zipcode": zip_code
            },
            "risks": biodiversity_risks,
            "total_risks": len(biodiversity_risks),
            "message": f"Found {len(biodiversity_risks)} biodiversity risk(s) in the area"
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

@app.route("/session-risks", methods=["GET"])
def get_session_risks():
    """Get risks from current session"""
    return jsonify({"risks": session.get("risks", [])})

# Location Management Routes
@app.route("/locations/add", methods=["POST"])
def add_location():
    """Add a new hotel location"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database not available"}), 500
    
    # Check if user is logged in
    if 'user_id' not in session:
        return jsonify({"error": "Please login first"}), 401
    
    try:
        data = request.json
        hotel_name = data.get('hotel_name')
        street_address = data.get('street_address')
        city = data.get('city')
        zip_code = data.get('zip_code')
        email = data.get('email')
        
        # Validate required fields
        if not all([hotel_name, street_address, city, zip_code, email]):
            return jsonify({"error": "All fields are required"}), 400
        
        # Get coordinates from address
        full_address = f"{street_address}, {city}, NJ {zip_code}"
        lat, lon, _ = get_lat_lon_from_address(full_address)
        
        if lat is None or lon is None:
            return jsonify({"error": "Could not determine coordinates for this address"}), 400
        
        # Check if location is within New Jersey bounds
        if not (NJ_BOUNDS["south"] <= lat <= NJ_BOUNDS["north"] and 
                NJ_BOUNDS["west"] <= lon <= NJ_BOUNDS["east"]):
            return jsonify({"error": "Location must be within New Jersey"}), 400
        
        # Connect to database
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Failed to connect to database"}), 500
        
        cursor = conn.cursor()
        
        # Check if location already exists
        cursor.execute("""
            SELECT id FROM hotel_locations 
            WHERE hotel_name = %s AND street_address = %s AND city = %s AND zip_code = %s
        """, (hotel_name, street_address, city, zip_code))
        
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"error": "This location already exists"}), 400
        
        # Insert new location
        cursor.execute("""
            INSERT INTO hotel_locations 
            (user_id, hotel_name, street_address, city, zip_code, email, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (session['user_id'], hotel_name, street_address, city, zip_code, email, lat, lon))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Location added successfully!"}), 201
        
    except Exception as e:
        return jsonify({"error": f"Failed to add location: {str(e)}"}), 500

@app.route("/locations/view", methods=["GET"])
def view_locations():
    """View all hotel locations for the current user"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database not available"}), 500
    
    # Check if user is logged in
    if 'user_id' not in session:
        return jsonify({"error": "Please login first"}), 401
    
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Failed to connect to database"}), 500
        
        cursor = conn.cursor()
        
        # Get all locations for the current user
        cursor.execute("""
            SELECT hotel_name, street_address, city, zip_code, email, latitude, longitude, created_at
            FROM hotel_locations 
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (session['user_id'],))
        
        locations = []
        for row in cursor.fetchall():
            locations.append({
                "hotel_name": row[0],
                "street_address": row[1],
                "city": row[2],
                "zip_code": row[3],
                "email": row[4],
                "latitude": float(row[5]) if row[5] else 0,
                "longitude": float(row[6]) if row[6] else 0,
                "created_at": row[7].strftime('%Y-%m-%d %H:%M:%S') if row[7] else None
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({"locations": locations}), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to fetch locations: {str(e)}"}), 500

@app.route("/locations/delete", methods=["POST"])
def delete_location():
    """Delete a hotel location"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database not available"}), 500
    
    # Check if user is logged in
    if 'user_id' not in session:
        return jsonify({"error": "Please login first"}), 401
    
    try:
        data = request.json
        hotel_name = data.get('hotel_name')
        street_address = data.get('street_address')
        city = data.get('city')
        zip_code = data.get('zip_code')
        
        # Validate required fields
        if not all([hotel_name, street_address, city, zip_code]):
            return jsonify({"error": "All location fields are required for deletion"}), 400
        
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Failed to connect to database"}), 500
        
        cursor = conn.cursor()
        
        # Delete the location (only for the current user)
        cursor.execute("""
            DELETE FROM hotel_locations 
            WHERE user_id = %s AND hotel_name = %s AND street_address = %s 
                  AND city = %s AND zip_code = %s
        """, (session['user_id'], hotel_name, street_address, city, zip_code))
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Location not found or you don't have permission to delete it"}), 404
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Location deleted successfully!"}), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to delete location: {str(e)}"}), 500

@app.route("/locations/edit", methods=["POST"])
def edit_location():
    """Edit a hotel location"""
    if not DATABASE_AVAILABLE:
        return jsonify({"error": "Database not available"}), 500
    
    # Check if user is logged in
    if 'user_id' not in session:
        return jsonify({"error": "Please login first"}), 401
    
    try:
        data = request.json
        
        # Original location data (for identification)
        original = data.get('original', {})
        original_hotel_name = original.get('hotel_name')
        original_street_address = original.get('street_address')
        original_city = original.get('city')
        original_zip_code = original.get('zip_code')
        
        # Updated location data
        updated = data.get('updated', {})
        new_hotel_name = updated.get('hotel_name')
        new_street_address = updated.get('street_address')
        new_city = updated.get('city')
        new_zip_code = updated.get('zip_code')
        new_email = updated.get('email')
        
        # Validate required fields
        if not all([original_hotel_name, original_street_address, original_city, original_zip_code]):
            return jsonify({"error": "Original location data is required"}), 400
        
        if not all([new_hotel_name, new_street_address, new_city, new_zip_code, new_email]):
            return jsonify({"error": "All updated fields are required"}), 400
        
        # Get coordinates for new address
        full_address = f"{new_street_address}, {new_city}, NJ {new_zip_code}"
        lat, lon, _ = get_lat_lon_from_address(full_address)
        
        if lat is None or lon is None:
            return jsonify({"error": "Could not determine coordinates for the new address"}), 400
        
        # Check if new location is within New Jersey bounds
        if not (NJ_BOUNDS["south"] <= lat <= NJ_BOUNDS["north"] and 
                NJ_BOUNDS["west"] <= lon <= NJ_BOUNDS["east"]):
            return jsonify({"error": "New location must be within New Jersey"}), 400
        
        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Failed to connect to database"}), 500
        
        cursor = conn.cursor()
        
        # Update the location (only for the current user)
        cursor.execute("""
            UPDATE hotel_locations 
            SET hotel_name = %s, street_address = %s, city = %s, zip_code = %s, 
                email = %s, latitude = %s, longitude = %s, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = %s AND hotel_name = %s AND street_address = %s 
                  AND city = %s AND zip_code = %s
        """, (new_hotel_name, new_street_address, new_city, new_zip_code, new_email, lat, lon,
              session['user_id'], original_hotel_name, original_street_address, 
              original_city, original_zip_code))
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "Location not found or you don't have permission to edit it"}), 404
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Location updated successfully!"}), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to update location: {str(e)}"}), 500

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
