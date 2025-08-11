
import mysql.connector

# Database configuration
db_config = {
    "host": "localhost",       # Or '127.0.0.1'
    "user": "user", # Replace with your MySQL username
    "password": "your_password", # Replace with your MySQL password
    "database": "postgres"  # Existing database name
}

# Test the connection
try:
    connection = mysql.connector.connect(**db_config)
    print("Connected to the database successfully!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed.")
