from flask import Blueprint, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from services.db import connect_db

account_bp = Blueprint("account", __name__)

@account_bp.route("/update-profile", methods=["PUT","OPTIONS"])
def update_profile():
    print("📦 Incoming session:", dict(session))

    if request.method == "OPTIONS":
            # Handle CORS preflight request
            response = jsonify({"message": "CORS preflight accepted"})
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
            response.headers.add("Access-Control-Allow-Credentials", "true")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type")
            response.headers.add("Access-Control-Allow-Methods", "PUT, OPTIONS")
            return response, 200

    print("🧪 OPTIONS handled")

    try:
        data = request.json
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET hotel_name=%s, email=%s WHERE id=%s",
                       (data["hotel_name"], data["email"], user_id))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Profile updated."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@account_bp.route("/change-password", methods=["POST"])
def change_password():
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight accepted"})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200
    try:
        print("📦 Incoming session:", dict(session))
        user_id = session.get("user_id")
        data = request.json
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT password_hash FROM users WHERE id=%s", (user_id,))
        stored_hash = cursor.fetchone()[0]

        if not check_password_hash(stored_hash, data["currentPassword"]):
            return jsonify({"error": "Incorrect current password"}), 400

        hashed_new = generate_password_hash(data["newPassword"])
        cursor.execute("UPDATE users SET password_hash=%s WHERE id=%s", (hashed_new, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Password updated."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
