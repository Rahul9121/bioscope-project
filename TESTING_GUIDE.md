# 🧪 COMPREHENSIVE TESTING GUIDE FOR BIOSCOPE APPLICATION

## 📋 PRE-TESTING CHECKLIST

### ✅ Requirements Verification
Before testing, ensure you have:
- [x] Python 3.9+ installed
- [x] All dependencies installed (`pip install -r requirements.txt`)
- [x] Database loaded with 1.5M+ biodiversity records
- [x] `.env` file configured with DATABASE_URL
- [x] Backend code in working condition

---

## 🎯 TESTING PHASES

## **PHASE 1: BACKEND TESTING** 🖥️

### Step 1: Start Your Backend
```bash
# In your project directory
cd C:\Users\R.A.NAVEENTHEJA\Downloads\rahulfinal project\bioscope-project
py app.py
```

**Expected Output:**
```
🚀 Starting Bioscope Backend...
📦 Loading core imports...
✅ Core imports successful
🌐 CORS allowed origins: ['http://localhost:3000', ...]
✅ Database connection verified on startup
🚀 Starting Flask app on 0.0.0.0:5000
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

### Step 2: Test Backend Health
Open new terminal and run:
```bash
py test_app.py
```

**What to Look For:**
- ✅ Backend health check passes
- ✅ Database connection successful 
- ✅ PostgreSQL version shows (17.4+)
- ✅ Users table exists

---

## **PHASE 2: API ENDPOINT TESTING** 🔌

### Manual API Tests (Using Browser or Postman)

#### Test 1: Health Check
**URL:** `http://localhost:5000/health`
**Expected Response:**
```json
{
  "status": "healthy",
  "message": "Bioscope API is running"
}
```

#### Test 2: Database Status
**URL:** `http://localhost:5000/db-status`
**Expected Response:**
```json
{
  "status": "connected",
  "postgres_version": "PostgreSQL 17.4...",
  "users_table_exists": true,
  "database_url_configured": true
}
```

#### Test 3: User Registration (POST)
**URL:** `http://localhost:5000/register`
**Method:** POST
**Headers:** `Content-Type: application/json`
**Body:**
```json
{
  "hotel_name": "Test Eco Lodge",
  "email": "test@ecolodge.com",
  "password": "testpass123"
}
```
**Expected:** Status 201 or "already registered" message

#### Test 4: User Login (POST)
**URL:** `http://localhost:5000/login`
**Method:** POST
**Body:**
```json
{
  "email": "test@ecolodge.com",
  "password": "testpass123"
}
```
**Expected Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "hotel_name": "Test Eco Lodge",
    "email": "test@ecolodge.com"
  }
}
```

---

## **PHASE 3: BIODIVERSITY SEARCH TESTING** 🔍

### Test Location Searches

#### Test 5: Address Search
**URL:** `http://localhost:5000/search`
**Method:** POST
**Body:**
```json
{
  "input_text": "Newark, NJ"
}
```

**What to Verify:**
- ✅ Returns coordinates for Newark (~40.7357, -74.1724)
- ✅ Returns multiple risk types
- ✅ Risk data includes: Marine Risk, Freshwater Risk, Terrestrial Risk, Invasive Species
- ✅ Each risk has latitude, longitude, risk_type, description, threat_code

#### Test 6: ZIP Code Search
**Body:**
```json
{
  "input_text": "07302"
}
```

#### Test 7: Coordinate Search
**Body:**
```json
{
  "input_text": "40.7589, -74.0278"
}
```

### Expected Risk Data Structure:
```json
{
  "center": {
    "latitude": 40.7357,
    "longitude": -74.1724,
    "zipcode": "Newark, NJ"
  },
  "risks": [
    {
      "latitude": 40.7357,
      "longitude": -74.1724,
      "risk_type": "Marine Risk",
      "description": "Marine HCI Score: 0.85",
      "threat_code": "high",
      "mitigation": {
        "action": "Monitor marine ecosystem..."
      }
    }
  ]
}
```

---

## **PHASE 4: DATA QUALITY TESTING** 📊

### Verify Database Coverage

#### Test Different NJ Regions:
1. **Northern NJ:** "Paramus, NJ"
2. **Central NJ:** "Princeton, NJ" 
3. **Southern NJ:** "Atlantic City, NJ"
4. **Shore Area:** "Seaside Heights, NJ"

**For Each Location, Verify:**
- [ ] Gets valid coordinates within NJ bounds
- [ ] Returns multiple data types (marine, freshwater, terrestrial, invasive)
- [ ] Threat levels are appropriate (low, moderate, high)
- [ ] Mitigation actions are provided

---

## **PHASE 5: REPORT GENERATION TESTING** 📄

### Test PDF Reports
**URL:** `http://localhost:5000/download-report-direct`
**Method:** POST
**Body:**
```json
{
  "risks": [
    {
      "risk_type": "Marine Risk",
      "description": "High marine pollution",
      "threat_code": "high"
    }
  ],
  "format": "pdf"
}
```

**Expected:** PDF file download (content-type: application/pdf)

### Test Excel Reports
Same as above but with `"format": "excel"`

**Expected:** Excel file download

---

## **PHASE 6: FRONTEND TESTING** 🖥️

### If You Have Frontend Running:

#### Start Frontend (if available):
```bash
cd frontend  # or wherever your React/Next.js app is
npm start    # or npm run dev
```

#### Test Frontend Features:
1. **Registration Page**
   - [ ] Form accepts hotel name, email, password
   - [ ] Successful registration redirects to login
   - [ ] Error handling for duplicate emails

2. **Login Page** 
   - [ ] Valid credentials log in successfully
   - [ ] Invalid credentials show error message
   - [ ] Session persists after login

3. **Search Page**
   - [ ] Search box accepts addresses/ZIP codes/coordinates
   - [ ] Map displays search location
   - [ ] Risk markers appear on map
   - [ ] Risk details show in sidebar/popup

4. **Reports Page**
   - [ ] PDF download works
   - [ ] Excel download works
   - [ ] Reports contain searched risk data

---

## **PHASE 7: STRESS TESTING** ⚡

### Load Testing (Optional)
```bash
# Test multiple simultaneous searches
for i in {1..10}; do
  curl -X POST http://localhost:5000/search \
    -H "Content-Type: application/json" \
    -d '{"input_text": "Newark, NJ"}' &
done
```

### Database Query Performance
```python
# Time a large data query
import time
import requests

start = time.time()
response = requests.post(
    "http://localhost:5000/search",
    json={"input_text": "40.7589, -74.0278"}
)
elapsed = time.time() - start
print(f"Query took {elapsed:.2f} seconds")
# Should be under 2-3 seconds for good performance
```

---

## **PHASE 8: EDGE CASE TESTING** 🔍

### Test Invalid Inputs:
1. **Invalid Coordinates:** `"999, 999"`
2. **Outside NJ:** `"New York, NY"`
3. **Invalid ZIP:** `"00000"`
4. **Empty Input:** `""`
5. **Special Characters:** `"!@#$%"`

### Expected Behaviors:
- [ ] Graceful error messages
- [ ] No application crashes
- [ ] Appropriate HTTP status codes (400, 404, etc.)

---

## 🎯 **SUCCESS CRITERIA**

### Your Application is Ready When:
- ✅ **All API endpoints respond correctly**
- ✅ **Database queries return data for multiple NJ locations**
- ✅ **All risk types are represented in results** 
- ✅ **Report generation works for PDF and Excel**
- ✅ **Response times are under 3 seconds**
- ✅ **Error handling works gracefully**
- ✅ **1.5M+ records are accessible and searchable**

---

## 🚨 **TROUBLESHOOTING GUIDE**

### Common Issues:

#### "Backend not accessible"
```bash
# Check if running on correct port
netstat -an | findstr :5000
# Restart backend
py app.py
```

#### "Database connection failed"
- Check `.env` file has correct DATABASE_URL
- Verify Supabase connection string
- Test direct database connection:
```bash
py -c "import psycopg2; conn = psycopg2.connect('your_database_url')"
```

#### "No risk data found"
- Verify data import completed successfully
- Check if coordinates are within New Jersey bounds
- Test with known good coordinates: `40.7357, -74.1724`

#### "Session/Login issues"
- Clear browser cookies/sessions
- Check CORS settings in backend
- Verify session configuration in app.py

---

## 📞 **FINAL VALIDATION CHECKLIST**

Before declaring your application production-ready:

- [ ] **Backend runs without errors**
- [ ] **Database connection stable**
- [ ] **User registration/login functional**
- [ ] **Search returns biodiversity data for multiple locations**
- [ ] **All 5 data types represented** (Marine, Freshwater, Terrestrial, Invasive, IUCN)
- [ ] **PDF and Excel reports generate successfully**
- [ ] **Response times acceptable** (< 3 seconds)
- [ ] **Error handling graceful**
- [ ] **Session management working**
- [ ] **Data integrity verified** (coordinates match locations)

## 🎉 **CONGRATULATIONS!**

If all tests pass, your Bioscope application is ready for production deployment with comprehensive biodiversity data serving capabilities!
