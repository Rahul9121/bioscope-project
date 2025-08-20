# 🚀 Backend Deployment Fix Guide

## Issues Fixed:

### 1. ✅ Missing Dependencies
- Added `chromadb==0.4.15` and `sentence-transformers==2.2.2` to requirements.txt
- Added CPU-only PyTorch for lighter deployment

### 2. ✅ Updated Procfile  
- Changed from `cd backend && python app.py` to proper Gunicorn command
- Now uses: `web: gunicorn --bind 0.0.0.0:$PORT --chdir backend app:app`

### 3. 🔧 Environment Variables (MUST SET IN RAILWAY DASHBOARD)

**In Railway Dashboard → Your Project → Variables, set these:**

```bash
# Required Database Connection
DATABASE_URL=postgresql://postgres:your_password@your_host:5432/your_database?sslmode=require

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=false

# CORS - Update with your actual frontend URL
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000

# Security
SECRET_KEY=your-super-secret-production-key-change-this

# Port (Railway sets this automatically, but you can verify)
PORT=5000
```

### 4. 🗂️ File Structure Check
Your `mitigation_action.py` handles missing ML files gracefully with fallback mode.

## 🔄 Deployment Steps:

1. **Commit and push your changes:**
   ```bash
   git add .
   git commit -m "Fix deployment issues - add ML deps, update Procfile"
   git push origin main
   ```

2. **Set Environment Variables in Railway Dashboard:**
   - Go to Railway → Your Project → Variables
   - Add each environment variable listed above
   - **CRITICAL**: Replace placeholder values with your actual Supabase connection details

3. **Redeploy:**
   - Railway should auto-deploy after your push
   - Or manually trigger redeploy in Railway dashboard

4. **Test Endpoints:**
   ```bash
   # Health check
   curl https://your-railway-app.railway.app/health
   
   # Database status
   curl https://your-railway-app.railway.app/db-status
   ```

## 🚨 Common Issues & Solutions:

### Database Connection Issues:
- Verify DATABASE_URL format: `postgresql://user:password@host:port/database?sslmode=require`
- Ensure Supabase allows connections from Railway IPs
- Check Supabase connection pooling settings

### Missing ChromaDB Files:
- The app runs in fallback mode if ChromaDB files are missing
- Consider uploading your `chroma_storage_rag` folder to deployment if needed

### Import Errors:
- All dependencies are now in requirements.txt
- If still having issues, try pinning specific versions

## 🔍 Debug Commands:

Check deployment logs in Railway dashboard for specific error messages.

Common error patterns:
- `ModuleNotFoundError` → Missing dependency
- `psycopg2.OperationalError` → Database connection issue  
- `FileNotFoundError` → Missing ML model files (should fallback gracefully)

## ✅ Success Indicators:

1. `/health` endpoint returns `{"status": "healthy"}`
2. `/db-status` shows database connection successful
3. No import errors in deployment logs
4. Frontend can connect to backend APIs
