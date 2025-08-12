import psycopg2
import os
import urllib.parse as urlparse

def get_db_config():
    """Get database configuration from environment variables"""
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Parse DATABASE_URL for services like Railway, Heroku, Supabase
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

def connect_db():
    """Connect to the database using environment configuration"""
    try:
        db_config = get_db_config()
        return psycopg2.connect(**db_config)
    except Exception as err:
        print(f"Database connection error: {err}")
        return None
