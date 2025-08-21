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
    DATABASE_AVAILABLE = True
    print("✅ Database dependencies loaded successfully")
except ImportError as e:
    print(f"⚠️ Database dependencies not available: {e}")
    DATABASE_AVAILABLE = False

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
