from flask import Blueprint, request, session, jsonify
from backend.services.db import connect_db
from backend.utils.geocode import get_lat_lon_from_address
from functools import wraps

location_bp = Blueprint("location", __name__)

# Session auth decorator
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper

# ✅ Add Location
@location_bp.route("/add", methods=["POST"])
@login_required
def add_location():
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
        """, (session['user_id'], hotel_name, street_address, city, zip_code, lat, lon))
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
        user_id = session.get("user_id")
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
            session['user_id'], data.get("hotel_name"), data.get("street_address"),
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
        """, (hotel_name, street_address, city, zip_code, lat, lon, location_id, session['user_id']))
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
