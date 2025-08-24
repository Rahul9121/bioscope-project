# 🚀 BiodivProScope - Minimal App Deployment Guide

**Current Status:** The application is running locally with `minimal_app.py` and is ready for production deployment.

## ✅ What's Working

- **Backend:** `minimal_app.py` running on port 5001
- **Frontend:** React app connecting to backend on port 5001
- **Authentication:** Mock login/register endpoints working
- **Risk Assessment:** Mock location search endpoint working
- **CORS:** Properly configured for cross-origin requests

## 🎯 Deployment Strategy

Since we're using the minimal app approach, deployment is simplified:

### Backend Dependencies (minimal_app.py)
```
Flask==2.2.3
Flask-Cors==3.0.10
python-dotenv==1.0.0
Werkzeug==2.2.3
```

## 🚂 Railway Backend Deployment

### Step 1: Set Environment Variables in Railway

```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5001
RAILWAY_ENVIRONMENT=production

# CORS - Update with your Vercel frontend URL
ALLOWED_ORIGINS=https://your-frontend-app.vercel.app,http://localhost:3000

# Security
SECRET_KEY=your_super_secure_production_secret_key

# App Config  
APP_ENV=production
DEBUG=false
```

### Step 2: Deploy Process

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "🚀 Deploy minimal app to production"
   git push origin main
   ```

2. **Railway Setup:**
   - Connect your GitHub repo to Railway
   - Railway will detect Python project automatically
   - It will use the `Procfile` which points to `minimal_app.py`

3. **Automatic Build:**
   ```
   web: python minimal_app.py
   ```

4. **Health Check:** 
   Railway will use `/health` endpoint for health monitoring

### Step 3: Get Your Backend URL

After deployment, you'll get a URL like:
`https://bioscope-project-production.up.railway.app`

## 🌐 Vercel Frontend Deployment

### Step 1: Update API Configuration

Edit `frontend/src/services/api.js`:

```javascript
// Replace this line:
const railwayUrl = 'https://your-backend-app-production.up.railway.app';

// With your actual Railway URL:
const railwayUrl = 'https://bioscope-project-production.up.railway.app';
```

### Step 2: Deploy to Vercel

1. **Push Frontend Changes:**
   ```bash
   git add .
   git commit -m "🌐 Update API URL for production"
   git push origin main
   ```

2. **Vercel Configuration:**
   - Root Directory: `frontend`
   - Framework: Create React App
   - Build Command: `npm run build`
   - Output Directory: `build`

### Step 3: Update CORS After Frontend Deployment

Once you have your Vercel URL, update Railway environment variables:

```env
ALLOWED_ORIGINS=https://your-actual-vercel-url.vercel.app,https://your-actual-vercel-url-git-main.vercel.app,http://localhost:3000
```

## 🧪 Testing Production Deployment

### Backend Tests

```bash
# Health check
curl https://your-railway-url.up.railway.app/health

# Login test  
curl -X POST https://your-railway-url.up.railway.app/account/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Location search test
curl -X POST https://your-railway-url.up.railway.app/locations/search \
  -H "Content-Type: application/json" \
  -d '{"location":"New York"}'
```

Expected responses:
- Health: `{"status": "healthy", "message": "Minimal Bioscope API is running"}`
- Login: `{"success": true, "message": "Login successful (mock)", "user": {...}}`
- Search: `{"success": true, "message": "Location search working (mock)", "results": [...]}`

### Frontend Tests

1. Visit your Vercel URL
2. Try logging in with any email/password
3. Try searching for locations
4. Check browser console for any CORS errors

## 🔧 Current Functionality

### Mock Endpoints Working

| Endpoint | Method | Status | Description |
|----------|--------|---------|-------------|
| `/health` | GET | ✅ Working | Health check |
| `/account/login` | POST | ✅ Working | Mock authentication |
| `/account/register` | POST | ✅ Working | Mock registration |
| `/locations/search` | POST | ✅ Working | Mock location search |

### What's Mocked

- **Authentication:** Returns success for any email/password
- **Registration:** Returns success for any email
- **Location Search:** Returns sample biodiversity data
- **Risk Assessment:** Returns mock risk levels and species counts

## 🔄 Future Enhancements

To add full functionality later:

1. **Database Integration:** Add PostgreSQL connection
2. **Real Authentication:** Implement proper user management
3. **IUCN Data:** Connect to real biodiversity databases
4. **Risk Algorithms:** Implement actual risk calculation logic
5. **Report Generation:** Add PDF/Excel export functionality

## 📊 Deployment Files Structure

```
bioscope-project/
├── backend/
│   ├── minimal_app.py          # ✅ Production backend
│   ├── requirements-minimal.txt # ✅ Minimal dependencies
│   └── venv/                   # Local development only
├── frontend/
│   ├── src/services/api.js     # ✅ API configuration
│   ├── package.json            # ✅ Frontend dependencies
│   └── build/                  # Generated on deployment
├── Procfile                    # ✅ Railway start command
├── railway.json               # ✅ Railway configuration
├── .env.railway               # ✅ Production environment template
└── MINIMAL_APP_DEPLOYMENT.md  # ✅ This guide
```

## 🚨 Important Notes

1. **Mock Data Only:** Current deployment uses mock endpoints
2. **No Database Required:** Minimal app doesn't need database connection
3. **Production Ready:** CORS, environment detection, and error handling included
4. **Easy Scaling:** Can easily add real functionality later

## 🆘 Troubleshooting

### Common Issues

**CORS Errors:**
- Check `ALLOWED_ORIGINS` in Railway environment variables
- Ensure frontend URL is included

**Backend Won't Start:**  
- Check Railway logs
- Verify `PORT=5001` is set
- Ensure `minimal_app.py` exists

**API Connection Failed:**
- Verify Railway backend URL in `api.js`
- Check backend health endpoint
- Look for typos in URLs

---

**Status: Ready for Production Deployment! 🎉**

The minimal app provides a working foundation that can be deployed immediately and enhanced incrementally.
