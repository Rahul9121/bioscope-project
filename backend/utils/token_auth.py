import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

# Use a strong secret key
SECRET_KEY = os.getenv('SECRET_KEY', 'biodiv_jwt_secret_key_2024_production')

def generate_token(user_id, email):
    """Generate JWT token for user"""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=24),  # Token expires in 24 hours
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    print(f"✅ Generated token for user {user_id}: {token[:20]}...")
    return token

def verify_token(token):
    """Verify JWT token and return user info"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print(f"✅ Token verified for user {payload['user_id']}")
        return payload
    except jwt.ExpiredSignatureError:
        print("❌ Token has expired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"❌ Token is invalid: {e}")
        return None

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        
        print(f"🔍 Token Auth Debug:")
        print(f"- Authorization header: {auth_header}")
        
        if not auth_header:
            print("❌ No Authorization header")
            return jsonify({'error': 'No authorization token provided'}), 401
            
        try:
            # Extract token from "Bearer <token>"
            token = auth_header.split(' ')[1]
            print(f"- Token extracted: {token[:20]}...")
        except IndexError:
            print("❌ Invalid Authorization header format")
            return jsonify({'error': 'Invalid authorization header format'}), 401
            
        # Verify token
        payload = verify_token(token)
        if not payload:
            print("❌ Token verification failed")
            return jsonify({'error': 'Invalid or expired token'}), 401
            
        # Add user info to request context
        request.user_id = payload['user_id']
        request.user_email = payload['email']
        
        print(f"✅ Token auth successful for user {payload['user_id']}")
        return f(*args, **kwargs)
        
    return wrapper
