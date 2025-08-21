# Manual Backend Testing Guide

Since there are DNS resolution issues from your local machine, here's how to test your backend manually using your browser or tools like Postman.

## Backend URL
```
https://bioscope-project-production.up.railway.app
```

## Test 1: Basic Connectivity Tests

### Health Check
**URL:** `https://bioscope-project-production.up.railway.app/health`
**Method:** GET
**Expected Response:**
```json
{
  "status": "healthy",
  "message": "Bioscope API is running"
}
```

### Database Status
**URL:** `https://bioscope-project-production.up.railway.app/db-status`
**Method:** GET
**Expected Response:**
```json
{
  "status": "connected",
  "postgres_version": "PostgreSQL 15...",
  "users_table_exists": true,
  "database_url_configured": true
}
```

## Test 2: User Authentication

### User Registration
**URL:** `https://bioscope-project-production.up.railway.app/register`
**Method:** POST
**Headers:** `Content-Type: application/json`
**Body:**
```json
{
  "email": "test123@example.com",
  "password": "TestPassword123!",
  "confirm_password": "TestPassword123!",
  "hotel_name": "Test Hotel"
}
```
**Expected Response:**
```json
{
  "message": "Registration successful!"
}
```

### User Login
**URL:** `https://bioscope-project-production.up.railway.app/login`
**Method:** POST
**Headers:** `Content-Type: application/json`
**Body:**
```json
{
  "email": "test123@example.com",
  "password": "TestPassword123!"
}
```
**Expected Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "hotel_name": "Test Hotel",
    "email": "test123@example.com"
  }
}
```

## Test 3: Search Functionality

### Address Autocomplete
**URL:** `https://bioscope-project-production.up.railway.app/autocomplete?q=Princeton%2C%20NJ`
**Method:** GET
**Expected Response:**
```json
[
  {
    "place_id": "123456",
    "display_name": "Princeton, Mercer County, New Jersey, United States",
    "lat": "40.3572976",
    "lon": "-74.6672226"
  }
]
```

### Location Search
**URL:** `https://bioscope-project-production.up.railway.app/search`
**Method:** POST
**Headers:** `Content-Type: application/json`
**Body:**
```json
{
  "latitude": 40.3573,
  "longitude": -74.6672,
  "radius": 50
}
```
**Expected Response:**
```json
{
  "success": true,
  "location": "Princeton, NJ area",
  "risks": {
    "invasive_species": "Medium",
    "freshwater": "Low",
    "marine": "Low", 
    "terrestrial": "Medium",
    "iucn_species": "High"
  },
  "species": [
    {
      "common_name": "Norway Maple",
      "scientific_name": "Acer platanoides",
      "threat_level": "Medium"
    }
  ]
}
```

## Test 4: Report Generation

### Generate PDF Report
**URL:** `https://bioscope-project-production.up.railway.app/generate-report`
**Method:** POST
**Headers:** `Content-Type: application/json`
**Body:**
```json
{
  "location": "Princeton, NJ",
  "latitude": 40.3573,
  "longitude": -74.6672,
  "risks": {
    "invasive_species": "Medium",
    "freshwater": "Low",
    "marine": "Low",
    "terrestrial": "Medium",
    "iucn_species": "High"
  },
  "species": [
    {
      "common_name": "Norway Maple",
      "scientific_name": "Acer platanoides",
      "threat_level": "Medium"
    }
  ]
}
```
**Expected Response:** PDF file download or success message

## Testing with Browser

1. **GET Requests**: Simply paste the URLs into your browser
2. **POST Requests**: Use browser developer tools or Postman

## Testing with Postman

1. Import the requests above
2. Set proper headers
3. Test each endpoint systematically

## Expected Results

If your backend is working correctly, you should see:

✅ **Health Check**: Returns healthy status
✅ **Database**: Connected with proper version info
✅ **Registration**: Successfully creates new users
✅ **Login**: Authentication works properly
✅ **Search**: Returns biodiversity data for locations
✅ **Reports**: Generates PDF reports successfully

## Troubleshooting

### If endpoints return errors:
1. Check Railway logs for error messages
2. Verify environment variables are set
3. Ensure database connection is working

### If you get 404 errors:
- The minimal_app might be running instead of the full app
- Check the Railway deployment logs
- Verify the correct app.py is being executed

### If you get 500 errors:
- Database connection issues
- Missing environment variables
- Application code errors

## Alternative Testing Methods

If you still can't access the backend:

1. **Use a different network** (mobile hotspot, different WiFi)
2. **Use a VPN** to change your DNS resolver
3. **Use online tools** like curl.trillworks.com or httpie.io
4. **Ask someone else** to test the endpoints for you

## Next Steps

Once you've tested the endpoints manually, let me know:
1. Which endpoints are working
2. Any error messages you encounter
3. Whether you need help fixing any issues

This will help us ensure your backend is fully functional before moving to frontend integration!
