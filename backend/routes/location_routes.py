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

# JWT Token auth decorator
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print(f"🔍 Token Auth Debug in {f.__name__}:")
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        print(f"- Authorization header: {auth_header}")
        
        if not auth_header:
            print("❌ No Authorization header")
            return jsonify({"error": "🔒 Please login first. No authorization token provided."}), 401
            
        try:
            # Extract token from "Bearer <token>"
            token = auth_header.split(' ')[1]
            print(f"- Token extracted: {token[:20]}...")
        except IndexError:
            print("❌ Invalid Authorization header format")
            return jsonify({"error": "🔒 Please login first. Invalid authorization header format."}), 401
            
        # Import token verification
        try:
            from utils.token_auth import verify_token
        except ImportError:
            # Fallback token verification
            import base64
            import json
            def verify_token(token):
                try:
                    token_data = json.loads(base64.b64decode(token).decode())
                    return token_data
                except:
                    return None
        
        # Verify token
        payload = verify_token(token)
        if not payload:
            print("❌ Token verification failed")
            return jsonify({"error": "🔒 Please login first. Invalid or expired token."}), 401
            
        # Add user info to request context
        request.user_id = payload['user_id']
        request.user_email = payload['email']
        
        print(f"✅ Token auth successful for user {payload['user_id']}")
        return f(*args, **kwargs)
        
    return wrapper

# ✅ Add Location
@location_bp.route("/add", methods=["POST", "OPTIONS"])
def add_location():
    # Handle CORS preflight
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight accepted"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200
    
    return _add_location_impl()

@login_required
def _add_location_impl():
    try:
        data = request.get_json()
        hotel_name = data.get("hotel_name")
        street_address = data.get("street_address")
        city = data.get("city")
        zip_code = data.get("zip_code")

        if not zip_code or not zip_code.isdigit() or len(zip_code) != 5 or not zip_code.startswith("07"):
            return jsonify({"error": "Invalid New Jersey zipcode"}), 400

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

        return jsonify({"message": "Location added successfully"}), 201

    except Exception as e:
        print(f"⚠️ Add location error: {e}")
        return jsonify({"error": "Something went wrong"}), 500

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
        return jsonify({"locations": locations})

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
