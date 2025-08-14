import os
import psycopg2
from flask import Flask, request, jsonify, session
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

# Simple CORS setup
CORS(app, origins=['http://localhost:3000'])

def connect_db():
    """Simple database connection using environment variable"""
    try:
        # Use DATABASE_URL from environment
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            conn = psycopg2.connect(database_url)
            return conn
        else:
            # Fallback to individual environment variables
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'postgres'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'password'),
                port=os.getenv('DB_PORT', 5432)
            )
            return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Backend is running"}), 200

@app.route('/db-status', methods=['GET'])
def db_status():
    """Check database connection status"""
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({"status": "error", "message": "Cannot connect to database"}), 500
        
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        cursor.fetchone()
        cursor.close()
        conn.close()
        
        return jsonify({"status": "connected", "message": "Database connection successful"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    """Simple test endpoint"""
    return jsonify({"message": "Backend is working!"}), 200

@app.route('/search', methods=['POST'])
def search():
    """Basic search endpoint - simplified version"""
    try:
        data = request.get_json()
        search_term = data.get('input_text', '')
        
        conn = connect_db()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        # Simple response for now
        response = {
            "message": f"Search performed for: {search_term}",
            "center": {"latitude": 40.0, "longitude": -74.0, "zipcode": "00000"},
            "risks": [
                {
                    "risk_type": "Test Risk",
                    "description": "This is a test risk for demonstration",
                    "threat_code": "low"
                }
            ]
        }
        
        conn.close()
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Use environment variable for port, default to 5000
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
