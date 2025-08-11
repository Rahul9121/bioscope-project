import requests

GEOCODING_API_URL = "https://nominatim.openstreetmap.org/search"

def get_lat_lon_from_address(address):
    try:
        response = requests.get(
            GEOCODING_API_URL,
            params={"q": address, "countrycodes": "us", "format": "json"},
            headers={"User-Agent": "BiodivProScopeApp/1.0"}
        )

        if response.status_code == 200:
            results = response.json()
            if results:
                lat = float(results[0]["lat"])
                lon = float(results[0]["lon"])
                zip_code = results[0].get("display_name", "").split(",")[-2].strip()
                return lat, lon, zip_code
        return None, None, None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None, None, None
