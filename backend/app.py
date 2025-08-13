import json
import os
import psycopg2
from flask import Flask, request, jsonify, session, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import logging
from flask_cors import CORS
from flask_session import Session
from datetime import timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask_caching import Cache
import pandas as pd
from backend.routes.account_routes import account_bp
from backend.routes.location_routes import location_bp




import xlsxwriter
import traceback
from backend.mitigation_action import (
    generate_mitigation_report,
    query_mitigation_action,
    threat_level_from_code
)

app = Flask(__name__)
app.config["CACHE_TYPE"] = "simple"
cache = Cache(app)

# Get allowed origins from environment or default to localhost and Vercel
allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000,https://bioscope-project.vercel.app').split(',')
CORS(app, resources={r"/*": {"origins": allowed_origins}}, supports_credentials=True)

app.register_blueprint(account_bp, url_prefix="/account")
app.register_blueprint(location_bp, url_prefix="/locations")

# Use environment variable for secret key
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key_change_in_production')
logging.basicConfig(level=logging.DEBUG)

app.config.update({
    "SECRET_KEY": "your_secret_key",
    "SESSION_FILE_DIR": "./flask_session",
    "SESSION_TYPE": "filesystem",
    "SESSION_PERMANENT": True,
    "PERMANENT_SESSION_LIFETIME": timedelta(minutes=15),
    "SESSION_COOKIE_SAMESITE": "Lax",
    "SESSION_COOKIE_SECURE": False,
    "SESSION_COOKIE_HTTPONLY": True,
    "SESSION_COOKIE_NAME": "biodiv_session"
})

Session(app)

# Database configuration from environment variables
def get_db_config():
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Parse DATABASE_URL for services like Railway, Heroku
        import urllib.parse as urlparse
        url = urlparse.urlparse(database_url)
        return {
            'host': url.hostname,
            'user': url.username,
            'password': url.password,
            'dbname': url.path[1:],
            'port': url.port or 5432
        }
    else:
        # Fallback to individual environment variables
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'password'),
            'dbname': os.getenv('DB_NAME', 'postgres'),
            'port': os.getenv('DB_PORT', 5432)
        }

GEOCODING_API_URL = "https://nominatim.openstreetmap.org/search"

# Health check endpoint for deployment
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "message": "Bioscope API is running"}), 200

# Database debug endpoint
@app.route("/db-status", methods=["GET"])
def db_status():
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

@app.route("/session-risks", methods=["GET"])
def get_session_risks():
    return jsonify({"risks": session.get("risks", [])})

@app.before_request
def log_request():
    print(f"🔍 Request: {request.method} {request.path}")
    if request.method in ["POST", "PUT"]:
        print(f"Body: {request.get_data(as_text=True)}")

def connect_db():
    try:
        db_config = get_db_config()
        
        # Add SSL mode for production (Supabase requires SSL)
        if 'supabase.com' in db_config.get('host', ''):
            db_config['sslmode'] = 'require'
        
        print(f"🔗 Attempting database connection to: {db_config.get('host', 'unknown')}:{db_config.get('port', 'unknown')}")
        return psycopg2.connect(**db_config)
    except psycopg2.OperationalError as err:
        print(f"❌ PostgreSQL Operational Error: {err}")
        print("This usually means connection/authentication issues")
        return None
    except psycopg2.DatabaseError as err:
        print(f"❌ PostgreSQL Database Error: {err}")
        return None
    except Exception as err:
        print(f"❌ Unexpected database connection error: {err}")
        print(f"Error type: {type(err).__name__}")
        return None

# Get Latitude, Longitude from ZIP Code
def get_lat_lon_from_zip(zipcode):
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
    """
    Fetch latitude, longitude, and ZIP code for a given address using Nominatim API.
    Adjusts query parameters to avoid conflicts.
    """
    try:
        # Remove state to prevent conflicts with ZIP code
        response = requests.get(
            GEOCODING_API_URL,
            params={"q": address, "countrycodes": "us", "format": "json"},
            headers={"User-Agent": "BiodivProScopeApp/1.0"}
        )

        print(f"API Request URL: {response.url}")  # Debugging
        print(f"API Response Status: {response.status_code}")  # Debugging

        if response.status_code == 200:
            json_response = response.json()
            print(f"API Response JSON: {json_response}")  # Debugging full response

            if json_response:
                data = json_response[0]  # Use first result
                latitude = float(data["lat"])
                longitude = float(data["lon"])

                # Extract ZIP Code if available
                address_parts = data.get("display_name", "").split(",")
                zip_code = address_parts[-2].strip() if len(address_parts) > 1 else None
                print(f"Extracted ZIP Code: {zip_code}")

                return latitude, longitude, zip_code
            else:
                print("No results found for the address.")
                return None, None, None
        else:
            print(f"Nominatim API Error: {response.status_code}")
            return None, None, None

    except Exception as e:
        print(f"Error fetching address data: {e}")
        return None, None, None
@app.route("/address-autocomplete", methods=["GET"])
def address_autocomplete():
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
            print(f"Nominatim API returned status {response.status_code}")
            return jsonify([])
    except Exception as e:
        print(f"Error fetching autocomplete data: {e}")
        return jsonify([])


def standardize_threat_status(status):
    mapping = {
        "critically endangered": "high",
        "endangered": "high",
        "vulnerable": "moderate",
        "near threatened": "moderate",
        "least concern": "low",
        "data deficient": "unknown",
        "extinct": "high",
        "extinct in the wild": "high",
        "unknown": "low"
    }
    return mapping.get(status.lower(), "low")

# API Endpoint: Registration
@app.route('/register', methods=['POST', 'OPTIONS'])
def register():
    # Handle CORS preflight
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS preflight successful"}), 200

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
            "INSERT INTO users (hotel_name, email, password) VALUES (%s, %s, %s)",
            (hotel_name, email, hashed_password)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Registration successful!"}), 201

    except psycopg2.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

# Ensure all responses include CORS headers
def _build_cors_response(response, status_code=200):
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response, status_code

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required."}), 400

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, hotel_name, email, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "Invalid email or password"}), 401

        user_id, hotel_name, user_email, hashed_password = user

        if not check_password_hash(hashed_password, password):
            return jsonify({"error": "Invalid email or password"}), 401

        # ✅ Set session
        session['user_id'] = user_id
        session['email'] = email
        session.permanent = True

        # ✅ Debug
        print("✅ Session after login:", dict(session))

        # ✅ Build response
        response = jsonify({
            "message": "Login successful",
            "user": {
                "id": user_id,
                "hotel_name": hotel_name,
                "email": user_email
            }
        })

        # ✅ Explicit CORS headers
        origin = request.headers.get('Origin', 'http://localhost:3000')
        allowed_origin = origin if origin in ['http://localhost:3000', 'https://bioscope-project.vercel.app'] else 'http://localhost:3000'
        response.headers.add("Access-Control-Allow-Origin", allowed_origin)
        response.headers.add("Access-Control-Allow-Credentials", "true")

        return response, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/logout', methods=['POST', 'OPTIONS'])
def logout():
    if request.method == "OPTIONS":
        # Handle CORS preflight
        response = jsonify({"message": "CORS preflight success"})
        origin = request.headers.get('Origin', 'http://localhost:3000')
        allowed_origin = origin if origin in ['http://localhost:3000', 'https://bioscope-project.vercel.app'] else 'http://localhost:3000'
        response.headers.add("Access-Control-Allow-Origin", allowed_origin)
        response.headers.add("Access-Control-Allow-Credentials", "true")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200

    session.clear()
    print("🧹 Session cleared on logout")

    response = jsonify({"message": "Logout successful"})
    origin = request.headers.get('Origin', 'http://localhost:3000')
    allowed_origin = origin if origin in ['http://localhost:3000', 'https://bioscope-project.vercel.app'] else 'http://localhost:3000'
    response.headers.add("Access-Control-Allow-Origin", allowed_origin)
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response, 200


@app.route('/session-status', methods=['GET'])
def session_status():
    if 'user_id' in session:
        return jsonify({"active": True, "message": "Session is active"}), 200
    return jsonify({"active": False, "message": "Session expired"}), 401
@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    try:
        data = request.json
        email = data.get('email')
        new_password = data.get('new_password')

        if not email or not new_password:
            return jsonify({"error": "Email and new password are required."}), 400

        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Failed to connect to the database."}), 500
        cursor = conn.cursor()

        # Check if the email exists
        cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "Email not found."}), 404

        user_id, old_hashed_password = user

        # Check if the new password is different from the old password
        if check_password_hash(old_hashed_password, new_password):
            return jsonify({"error": "New password should be different"}), 400

        # Hash the new password
        hashed_new_password = generate_password_hash(new_password)

        # Update the password in the database
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_new_password, user_id))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Password reset successful. Redirecting to login page."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Sample threat data (Replace with database or dynamic query)
threat_data = [
    {"risk_type": "Invasive Species", "threat_code": "high", "description": "Fast-spreading non-native plant species"},
    {"risk_type": "Water Pollution", "threat_code": "moderate", "description": "Increased industrial waste in nearby rivers"},
    {"risk_type": "Air Pollution", "threat_code": "low", "description": "Localized emissions affecting air quality"},
]
@app.route("/search", methods=["POST"])
def search():
    try:
        input_text = request.json.get("input_text")
        lat, lon, zip_code = None, None, ""

        if input_text.replace(",", "").replace(".", "").replace(" ", "").isdigit():
            if "," in input_text:
                lat, lon = map(float, input_text.split(","))
                zip_code = "Unknown"
            elif len(input_text) == 5:
                response = requests.get(
                    GEOCODING_API_URL,
                    params={"postalcode": input_text, "countrycodes": "us", "format": "json"},
                    headers={"User-Agent": "BiodivProScopeApp/1.0"}
                )
                if response.status_code == 200 and response.json():
                    loc = response.json()[0]
                    lat = float(loc["lat"])
                    lon = float(loc["lon"])
                    zip_code = input_text
        else:
            response = requests.get(
                GEOCODING_API_URL,
                params={"q": input_text, "countrycodes": "us", "format": "json"},
                headers={"User-Agent": "BiodivProScopeApp/1.0"}
            )
            if response.status_code == 200 and response.json():
                loc = response.json()[0]
                lat = float(loc["lat"])
                lon = float(loc["lon"])
                zip_code = loc.get("display_name", "").split(",")[-2].strip()

        if lat is None or lon is None:
            return jsonify({"error": "Could not determine location."}), 400

        NJ_BOUNDS = {"north": 41.36, "south": 38.92, "west": -75.58, "east": -73.90}
        if not (NJ_BOUNDS["south"] <= lat <= NJ_BOUNDS["north"] and NJ_BOUNDS["west"] <= lon <= NJ_BOUNDS["east"]):
            return jsonify({"error": "The location is outside of New Jersey."}), 400

        conn = connect_db()
        if not conn:
            return jsonify({"error": "Database connection failed."}), 500

        cursor = conn.cursor()
        offset = int(request.json.get("offset", 0))
        print("Querying all risk types...")

        risk_data = []

        cursor.execute("""
            SELECT latitude, longitude, common_name, threat_code 
            FROM invasive_species 
            WHERE ABS(latitude - %s) <= 0.1 AND ABS(longitude - %s) <= 0.1
        """, (lat, lon))
        for row in cursor.fetchall():
            threat_code = row[3] or "low"
            risk_data.append({
                "latitude": row[0], "longitude": row[1],
                "risk_type": "Invasive Species",
                "description": row[2],
                "threat_code": threat_code,
                "mitigation": query_mitigation_action("Invasive Species", threat_code)
            })

        cursor.execute("""
            SELECT latitude, longitude, species_name, threat_status 
            FROM iucn_data 
            WHERE ABS(latitude - %s) <= 0.1 AND ABS(longitude - %s) <= 0.1 
            LIMIT 50 OFFSET %s
        """, (lat, lon, offset))
        for row in cursor.fetchall():
            threat_code = standardize_threat_status(row[3])
            risk_data.append({
                "latitude": row[0], "longitude": row[1],
                "risk_type": "IUCN",
                "description": row[2],
                "threat_code": threat_code,
                "mitigation": query_mitigation_action("IUCN", threat_code)
            })

        cursor.execute("""
            SELECT x, y, normalized_risk, COALESCE(risk_level, 'Low') 
            FROM freshwater_risk 
            WHERE ABS(y - %s) <= 0.5 AND ABS(x - %s) <= 0.1
        """, (lat, lon))
        for row in cursor.fetchall():
            threat_code = row[3].lower()
            risk_data.append({
                "latitude": row[1], "longitude": row[0],
                "risk_type": "Freshwater Risk",
                "description": f"Freshwater risk level: {row[2]}",
                "threat_code": threat_code,
                "mitigation": query_mitigation_action("Freshwater Risk", threat_code)
            })

        cursor.execute("""
            SELECT x, y, marine_hci 
            FROM marine_hci 
            WHERE ABS(y - %s) <= 0.5 AND ABS(x - %s) <= 0.1
        """, (lat, lon))
        for row in cursor.fetchall():
            hci = row[2] or 0
            level = "high" if hci >= 0.75 else "moderate" if hci >= 0.4 else "low"
            risk_data.append({
                "latitude": row[1], "longitude": row[0],
                "risk_type": "Marine Risk",
                "description": f"Marine HCI Score: {hci}",
                "threat_code": level,
                "mitigation": query_mitigation_action("Marine Risk", level)
            })

        cursor.execute("""
            SELECT x, y, normalized_risk, risk_level 
            FROM terrestrial_risk 
            WHERE ABS(y - %s) <= 0.5 AND ABS(x - %s) <= 0.1
        """, (lat, lon))

        for row in cursor.fetchall():
            score = float(row[2])
            level = row[3].lower() if row[3] else "low"

            risk_data.append({
                "latitude": row[1],  # y = latitude
                "longitude": row[0],  # x = longitude
                "risk_type": "Terrestrial Risk",
                "description": f"Terrestrial Risk Level: {score:.2f}",
                "threat_code": level,
                "mitigation": query_mitigation_action("Terrestrial Risk", level)
            })

        conn.close()
        session["risks"] = risk_data

        return jsonify({"center": {"latitude": lat, "longitude": lon, "zipcode": zip_code}, "risks": risk_data})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/download-report-direct", methods=["POST"])
def download_report_direct():
    try:
        data = request.get_json()
        risks = data.get("risks", [])
        file_format = data.get("format", "pdf")

        if not risks:
            return jsonify({"error": "No risks provided."}), 400

        if file_format == "pdf":
            filename = "biodiv_report.pdf"
            filepath = f"/tmp/{filename}"
            c = canvas.Canvas(filepath, pagesize=letter)
            width, height = letter

            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, "Biodiversity Risk Mitigation Report")
            c.setFont("Helvetica", 12)

            y = height - 100
            for idx, risk in enumerate(risks):
                c.drawString(50, y, f"{idx + 1}. {risk.get('risk_type', 'Unknown')} - {risk.get('description', '')}")
                y -= 20
                action = risk.get("mitigation", {}).get("action", "")
                if isinstance(action, str):
                    for line in action.split("\n"):
                        c.drawString(70, y, line.strip())
                        y -= 15
                        if y < 100:
                            c.showPage()
                            y = height - 50


            c.save()
            return send_file(filepath, as_attachment=True, download_name=filename)

        elif file_format in ["csv", "excel"]:
            df = pd.DataFrame(risks)
            filename = f"biodiv_report.{ 'xlsx' if file_format == 'excel' else 'csv' }"
            filepath = f"/tmp/{filename}"

            if file_format == "csv":
                df.to_csv(filepath, index=False)
            else:
                writer = pd.ExcelWriter(filepath, engine="xlsxwriter")
                df.to_excel(writer, index=False, sheet_name="Mitigation")
                writer.close()

            return send_file(filepath, as_attachment=True, download_name=filename)

        else:
            return jsonify({"error": "Unsupported format."}), 400

    except Exception as e:
        print("⚠️ Error generating report:", str(e))
        return jsonify({"error": "Failed to generate report."}), 500


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5001))
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
