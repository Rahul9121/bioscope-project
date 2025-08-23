from flask import Blueprint, request, session, jsonify
from functools import wraps
import sys
import os

# Add parent directory to path to import from main app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the database connection function from the main app
def connect_db():
    """Use the same database connection logic as main app"""
    import psycopg2
    import os
    
    # Get database connection string directly (same as main app)
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Ensure SSL for Supabase
        if 'supabase.com' in database_url and '?sslmode=' not in database_url:
            database_url += '?sslmode=require'
        connection_string = database_url
    else:
        # Fallback - build connection string from individual variables
        host = os.getenv('DB_HOST', 'localhost')
        user = os.getenv('DB_USER', 'postgres')
        password = os.getenv('DB_PASSWORD', 'password')
        dbname = os.getenv('DB_NAME', 'postgres')
        port = os.getenv('DB_PORT', 5432)
        connection_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    
    try:
        return psycopg2.connect(connection_string)
    except Exception as err:
        print(f"❌ Location route DB connection error: {err}")
        return None

try:
    # Try to import geocoding function from utils
    from utils.geocode import get_lat_lon_from_address
except ImportError:
    # Fallback geocoding function if utils not available
    def get_lat_lon_from_address(address):
        print(f"⚠️ Geocoding not available for: {address}")
        return 40.0583, -74.4057, "07001"  # Default NJ coordinates

location_bp = Blueprint("location", __name__)

# 🔧 Fixed session-based auth decorator
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # 🔧 FIX: Skip authentication for CORS preflight requests
        if request.method == "OPTIONS":
            return f(*args, **kwargs)
            
        print(f"🔍 Session Auth Debug in {f.__name__}:")
        
        # Check if user_id exists in session
        user_id = session.get('user_id')
        user_email = session.get('email')
        
        print(f"- Session user_id: {user_id}")
        print(f"- Session email: {user_email}")
        print(f"- Session keys: {list(session.keys())}")
        
        if not user_id:
            print("❌ No user_id in session")
            return jsonify({"error": "🔒 Please login first. Your session may have expired."}), 401
            
        # Add user info to request context
        request.user_id = user_id
        request.user_email = user_email
        
        print(f"✅ Session auth successful for user {user_id}")
        return f(*args, **kwargs)
        
    return wrapper

# ✅ Add Location
@location_bp.route("/add", methods=["POST", "OPTIONS"])
@login_required  # 🔧 FIX: Apply decorator directly to the route handler
def add_location():
    # Handle CORS preflight
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight accepted"})
        # 🔧 CRITICAL FIX: Cannot use * with credentials - must specify exact origin
        origin = request.headers.get('Origin', 'http://localhost:3000')
        # Get allowed origins from main app configuration
        default_origins = [
            'http://localhost:3000',
            'http://localhost:3001', 
            'https://bioscope-project.vercel.app',
            'https://bioscope-project-rahul9121.vercel.app',
            'https://bioscope-project-git-new-main-rahul9121.vercel.app',
            'https://bioscope-project-git-main-rahul9121.vercel.app'
        ]
        allowed_origin = origin if origin in default_origins else default_origins[0]
        response.headers.add("Access-Control-Allow-Origin", allowed_origin)
        response.headers.add("Access-Control-Allow-Credentials", "true")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200
    
    # 🔧 Moved the actual implementation inline
    try:
        data = request.get_json()
        hotel_name = data.get("hotel_name")
        street_address = data.get("street_address")
        city = data.get("city")
        zip_code = data.get("zip_code")

        # 🔧 FIX: Proper New Jersey zip code validation (starts with 07, 08, or 09)
        if not zip_code or not zip_code.isdigit() or len(zip_code) != 5:
            return jsonify({"error": "Invalid zipcode format (must be 5 digits)"}), 400
        
        if not zip_code.startswith(("07", "08", "09")):
            return jsonify({"error": "Invalid New Jersey zipcode (must start with 07, 08, or 09)"}), 400

        full_address = f"{street_address}, {city}, NJ {zip_code}"
        lat, lon, _ = get_lat_lon_from_address(full_address)
        if not lat or not lon:
            return jsonify({"error": "Could not geocode address"}), 400

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO hotel_locations (user_id, hotel_name, street_address, city, zip_code, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (request.user_id, hotel_name, street_address, city, zip_code, lat, lon))
        conn.commit()
        cursor.close()
        conn.close()

        response = jsonify({"message": "Location added successfully"})
        # Add CORS headers for successful response
        origin = request.headers.get('Origin', 'http://localhost:3000')
        default_origins = [
            'http://localhost:3000', 'http://localhost:3001', 
            'https://bioscope-project.vercel.app',
            'https://bioscope-project-rahul9121.vercel.app',
            'https://bioscope-project-git-new-main-rahul9121.vercel.app',
            'https://bioscope-project-git-main-rahul9121.vercel.app'
        ]
        allowed_origin = origin if origin in default_origins else default_origins[0]
        response.headers.add("Access-Control-Allow-Origin", allowed_origin)
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 201

    except Exception as e:
        print(f"⚠️ Add location error: {e}")
        error_response = jsonify({"error": "Something went wrong"})
        # Add CORS headers for error response
        origin = request.headers.get('Origin', 'http://localhost:3000')
        default_origins = [
            'http://localhost:3000', 'http://localhost:3001', 
            'https://bioscope-project.vercel.app',
            'https://bioscope-project-rahul9121.vercel.app',
            'https://bioscope-project-git-new-main-rahul9121.vercel.app',
            'https://bioscope-project-git-main-rahul9121.vercel.app'
        ]
        allowed_origin = origin if origin in default_origins else default_origins[0]
        error_response.headers.add("Access-Control-Allow-Origin", allowed_origin)
        error_response.headers.add("Access-Control-Allow-Credentials", "true")
        return error_response, 500

# 🔍 View Locations
@location_bp.route("/view", methods=["GET"])
@login_required
def view_locations():
    try:
        user_id = request.user_id
        print("📦 Viewing for user_id:", user_id)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, hotel_name, street_address, city, zip_code, latitude, longitude
            FROM hotel_locations
            WHERE user_id = %s
            ORDER BY id DESC
        """, (user_id,))
        rows = cursor.fetchall()
        print(f"✅ Retrieved {len(rows)} locations for user {user_id}")
        cursor.close()
        conn.close()

        locations = [
            {
                "id": r[0], "hotel_name": r[1], "street_address": r[2],
                "city": r[3], "zip_code": r[4], "latitude": r[5], "longitude": r[6]
            } for r in rows
        ]
        
        response = jsonify({"locations": locations})
        # Add CORS headers for successful response
        origin = request.headers.get('Origin', 'http://localhost:3000')
        default_origins = [
            'http://localhost:3000', 'http://localhost:3001', 
            'https://bioscope-project.vercel.app',
            'https://bioscope-project-rahul9121.vercel.app',
            'https://bioscope-project-git-new-main-rahul9121.vercel.app',
            'https://bioscope-project-git-main-rahul9121.vercel.app'
        ]
        allowed_origin = origin if origin in default_origins else default_origins[0]
        response.headers.add("Access-Control-Allow-Origin", allowed_origin)
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

    except Exception as e:
        print(f"⚠️ View location error: {e}")
        return jsonify({"error": "Could not fetch locations"}), 500


# ❌ Delete Location
@location_bp.route("/delete", methods=["POST"])
@login_required
def delete_location():
    try:
        data = request.json
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM hotel_locations
            WHERE user_id = %s AND hotel_name = %s AND street_address = %s AND city = %s AND zip_code = %s
        """, (
            request.user_id, data.get("hotel_name"), data.get("street_address"),
            data.get("city"), data.get("zip_code")
        ))
        deleted = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()

        if deleted == 0:
            return jsonify({"error": "Location Not Found"}), 404
        return jsonify({"message": "Location deleted successfully"})

    except Exception as e:
        print(f"⚠️ Delete location error: {e}")
        return jsonify({"error": "Something went wrong"}), 500

# ✏️ Edit Location
@location_bp.route("/edit", methods=["POST"])
@login_required
def edit_location():
    try:
        data = request.get_json()
        location_id = data.get("id")
        hotel_name = data.get("hotel_name")
        street_address = data.get("street_address")
        city = data.get("city")
        zip_code = data.get("zip_code")

        full_address = f"{street_address}, {city}, NJ {zip_code}"
        lat, lon, _ = get_lat_lon_from_address(full_address)
        if not lat or not lon:
            return jsonify({"error": "Could not geocode address"}), 400

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE hotel_locations
            SET hotel_name = %s, street_address = %s, city = %s, zip_code = %s,
                latitude = %s, longitude = %s
            WHERE id = %s AND user_id = %s
        """, (hotel_name, street_address, city, zip_code, lat, lon, location_id, request.user_id))
        updated = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()

        if updated == 0:
            return jsonify({"error": "Location Not Found"}), 404

        return jsonify({"message": "Location updated successfully"})
    except Exception as e:
        print(f"⚠️ Edit location error: {e}")
        return jsonify({"error": "Something went wrong"}), 500
