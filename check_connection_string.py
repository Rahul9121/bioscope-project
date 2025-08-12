#!/usr/bin/env python3
"""
Connection String Checker
"""

import os
from dotenv import load_dotenv
import urllib.parse as urlparse

def check_connection_string():
    load_dotenv()
    database_url = os.getenv('DATABASE_URL')
    
    print(f"Raw DATABASE_URL: {database_url}")
    
    if database_url:
        try:
            url = urlparse.urlparse(database_url)
            print(f"Scheme: {url.scheme}")
            print(f"Username: {url.username}")
            print(f"Password: {url.password}")
            print(f"Hostname: {url.hostname}")
            print(f"Port: {url.port}")
            print(f"Database: {url.path[1:]}")
        except Exception as e:
            print(f"Error parsing URL: {e}")

if __name__ == "__main__":
    check_connection_string()
