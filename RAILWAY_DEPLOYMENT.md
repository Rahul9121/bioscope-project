# Railway Deployment Fix Guide

## Issues Identified & Fixed

### 1. **Database Connection Issues**
- **Problem**: SSL mode not properly configured for Supabase
- **Solution**: Added `?sslmode=require` to DATABASE_URL in `.railway.env`

### 2. **Port Configuration**  
- **Problem**: Using non-standard port 5001 instead of Railway's default
- **Solution**: Changed to use Railway's PORT environment variable (defaults to 5000)

### 3. **Environment Variables**
- **Problem**: Mixed configuration causing conflicts
- **Solution**: Simplified to use Railway's standard approach

## What Was Changed

### `.railway.env` (Railway Environment Variables)
```bash
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5000

# Database with SSL enabled for Supabase
DATABASE_URL=postgresql://postgres.fxxxwgomogyzafrvrjio:rahul2002rahul@aws-0-us-east-2.pooler.supabase.com:6543/postgres?sslmode=require

# CORS for your frontend
ALLOWED_ORIGINS=https://bioscope-project.vercel.app,http://localhost:3000

# Security key
SECRET_KEY=your-super-secret-key-change-this-in-production
```

### `railway.toml` (Railway Configuration)
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "python start.py"
restartPolicyType = "ON_FAILURE"  
restartPolicyMaxRetries = 3
```

### `start.py` (Entry Point)
```python
if __name__ == '__main__':
    # Railway automatically provides PORT environment variable
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

## Deployment Steps

### 1. **Update Railway Environment Variables**
Go to your Railway dashboard:
1. Select your project
2. Click on your backend service
3. Go to "Variables" tab  
4. Set these variables:
   ```
   DATABASE_URL=postgresql://postgres.fxxxwgomogyzafrvrjio:rahul2002rahul@aws-0-us-east-2.pooler.supabase.com:6543/postgres?sslmode=require
   FLASK_ENV=production
   ALLOWED_ORIGINS=https://bioscope-project.vercel.app,http://localhost:3000
   SECRET_KEY=your-super-secret-key-change-this-in-production
   ```

### 2. **Push Changes to Git**
```bash
git add .
git commit -m "Fix Railway deployment configuration"
git push
```

### 3. **Railway will automatically redeploy**
- Check the deployment logs for any errors
- Test the health endpoint: `https://your-app.railway.app/health`
- Test database status: `https://your-app.railway.app/db-status`

## Testing Your Deployment

### 1. **Test Health Check**
```bash
curl https://your-railway-url.railway.app/health
```
Should return: `{"status":"healthy","message":"Bioscope API is running"}`

### 2. **Test Database Connection**  
```bash
curl https://your-railway-url.railway.app/db-status
```
Should return connection status and table information.

### 3. **Test Registration**
```bash
curl -X POST https://your-railway-url.railway.app/register \
  -H "Content-Type: application/json" \
  -d '{"hotel_name":"Test Hotel","email":"test@example.com","password":"testpass123"}'
```

## Common Issues & Solutions

### **"Database connection failed"**
- Check that DATABASE_URL includes `?sslmode=require`
- Verify Supabase credentials are correct
- Check Supabase project is running

### **"Port already in use"**
- Railway handles port automatically - don't specify a custom port
- Make sure PORT environment variable is not set to a conflicting value

### **CORS errors from frontend**
- Ensure ALLOWED_ORIGINS includes your Vercel URL
- Check that frontend is making requests to correct Railway URL

### **Build failures**
- Check requirements.txt has all needed packages
- Verify Python path setup in start.py
- Look at Railway build logs for specific error messages

## Next Steps

1. **Update Frontend**: Make sure your React app is pointing to the correct Railway URL
2. **Test End-to-End**: Test registration, login, and search functionality  
3. **Monitor**: Check Railway logs for any runtime errors
4. **SSL Certificate**: Railway provides HTTPS automatically for custom domains

## Railway Dashboard Links
- **Project**: https://railway.app/dashboard
- **Logs**: Go to your service → "Deployments" → Click latest deployment  
- **Variables**: Go to your service → "Variables"
- **Settings**: Go to your service → "Settings"
