# Complete Deployment Instructions for Bioscope Project

## Overview
This guide will help you deploy the Bioscope project with:
- **Backend**: Railway (Flask API)
- **Database**: Supabase (PostgreSQL)  
- **Frontend**: Vercel (React)

## 🔧 Step 1: Setup Database (Supabase)

### 1.1 Create Supabase Project
1. Go to [supabase.com](https://supabase.com) and create a new project
2. Wait for the project to initialize
3. Go to **Settings > Database** and copy your connection string
4. Note down your project URL and anon key

### 1.2 Setup Database Schema
1. Go to **SQL Editor** in your Supabase dashboard
2. Copy and paste the contents of `database_setup.sql`
3. Execute the script to create all tables and sample data

## 🚀 Step 2: Deploy Backend to Railway

### 2.1 Create Railway Project
1. Go to [railway.app](https://railway.app) and create a new project
2. Connect your GitHub repository containing this code
3. Select "Deploy from GitHub repo"

### 2.2 Configure Environment Variables in Railway
Go to your Railway project dashboard and add these environment variables:

```
DATABASE_URL=postgresql://postgres.your_supabase_user:your_password@db.your_project_ref.supabase.co:5432/postgres?sslmode=require
FLASK_ENV=production
PORT=5000
SECRET_KEY=your-super-secret-key-here
ALLOWED_ORIGINS=https://your-vercel-app.vercel.app,http://localhost:3000
```

**Important**: Replace the DATABASE_URL with your actual Supabase connection string from Step 1.1

### 2.3 Deploy
1. Railway will automatically build and deploy your backend
2. Note the Railway URL (e.g., `https://your-app-name.railway.app`)
3. Test the deployment by visiting: `https://your-app-name.railway.app/health`

## 🌐 Step 3: Deploy Frontend to Vercel

### 3.1 Update Frontend Configuration
1. Open `frontend/.env.production`
2. Update `REACT_APP_API_URL` with your Railway backend URL:
```
REACT_APP_API_URL=https://your-app-name.railway.app
```

### 3.2 Deploy to Vercel
1. Go to [vercel.com](https://vercel.com) and create a new project
2. Import from your GitHub repository
3. Set the root directory to `frontend/`
4. Configure build settings:
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Install Command: `npm install`

### 3.3 Configure Environment Variables in Vercel
Add these environment variables in Vercel:
```
REACT_APP_API_URL=https://your-railway-backend.railway.app
GENERATE_SOURCEMAP=false
```

## ✅ Step 4: Test the Complete Setup

### 4.1 Test Backend API
```bash
# Test health endpoint
curl https://your-railway-backend.railway.app/health

# Test database connection
curl https://your-railway-backend.railway.app/db-status
```

### 4.2 Test Frontend
1. Visit your Vercel app URL
2. Try registering a new account
3. Try logging in
4. Search for a New Jersey location (e.g., "Princeton, NJ" or "07663")
5. Verify that risk data appears on the map

## 🔧 Step 5: Fix Common Issues

### Backend Issues

#### "Database connection failed"
- Verify your DATABASE_URL includes `?sslmode=require`
- Check Supabase credentials are correct
- Ensure your Supabase project is active

#### "Module import errors"
- Make sure `start.py` is properly configured
- Verify Python path setup in deployment

#### "CORS errors"
- Update ALLOWED_ORIGINS with your actual Vercel URL
- Make sure both HTTP and HTTPS origins are included

### Frontend Issues

#### "API calls failing"  
- Verify REACT_APP_API_URL points to your Railway backend
- Check that Railway backend is responding at `/health`
- Ensure both frontend and backend are using HTTPS

#### "Build failures"
- Check that all dependencies are listed in `package.json`
- Verify Node.js version compatibility

## 🔐 Step 6: Security Checklist

- [ ] Change SECRET_KEY to a strong, unique value
- [ ] Update DATABASE_URL with real credentials (not example values)
- [ ] Set ALLOWED_ORIGINS to only include your actual domains
- [ ] Enable Supabase RLS (Row Level Security) if needed
- [ ] Add API rate limiting in production

## 📊 Step 7: Monitor and Maintain

### Railway Backend Monitoring
- Check Railway logs for errors
- Monitor memory and CPU usage
- Set up uptime monitoring

### Vercel Frontend Monitoring  
- Check Vercel function logs
- Monitor build times and deployments
- Set up error tracking (optional)

### Database Maintenance
- Monitor Supabase usage and limits
- Backup database regularly
- Optimize queries for performance

## 🆘 Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| 500 Database Error | Check DATABASE_URL and Supabase status |
| CORS Error | Update ALLOWED_ORIGINS in Railway |
| Import Error | Verify Python path in start.py |
| Build Failed | Check requirements.txt and Python version |
| Frontend 404 | Verify REACT_APP_API_URL |

## 📞 Support

If you encounter issues:
1. Check the logs in Railway and Vercel dashboards
2. Verify all environment variables are set correctly
3. Test each component individually (database, backend, frontend)
4. Make sure all URLs and credentials are updated

## 🎉 Success!

Once all steps are complete, you should have:
- ✅ Supabase database with all tables and data
- ✅ Railway backend API responding to requests  
- ✅ Vercel frontend connected to backend
- ✅ Full functionality: registration, login, search, risk assessment

Your Bioscope application is now fully deployed and ready to use!
