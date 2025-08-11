import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'password',
    'dbname': 'postgres'
}

def connect_db():
    return psycopg2.connect(**DB_CONFIG)
