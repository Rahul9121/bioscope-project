# 🚀 Deployment Checklist for BiodivProScope

## ✅ Pre-Deployment Tasks Completed

### Backend Configuration
- [x] Removed hardcoded database credentials
- [x] Added environment variable configuration for DATABASE_URL
- [x] Updated CORS settings to use ALLOWED_ORIGINS environment variable
- [x] Added health check endpoint at `/health`
- [x] Updated requirements.txt with all dependencies
- [x] Configured production-ready Flask app settings

### Frontend Configuration
- [x] Updated API service to use REACT_APP_API_URL environment variable
- [x] Added withCredentials for CORS support
- [x] Configured for production builds

### Database & Data
- [x] Created sample data files for development
- [x] Added instructions for handling large data files
- [x] Database configuration supports both DATABASE_URL and individual variables

### Documentation
- [x] Updated DEPLOYMENT.md with comprehensive instructions
- [x] Created .env file template
- [x] Added sample data creation script

## 🔧 Required Actions Before Deployment

### 1. Environment Variables Setup

**For Railway/Render/Heroku:**
```bash
DATABASE_URL=postgresql://user:pass@host:port/dbname
SECRET_KEY=generate_a_strong_secret_key_here
FLASK_ENV=production
ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
PORT=5001
```

**For Vercel (Frontend):**
```bash
REACT_APP_API_URL=https://your-backend-domain.railway.app
```

### 2. Database Setup

#### Option A: Upload Large Data Files
1. Upload the missing large files to cloud storage (AWS S3, Google Cloud)
2. Update data loading scripts to fetch from cloud storage
3. Set environment variables for cloud storage URLs

#### Option B: Import to Database
1. Import large CSV files directly into your production PostgreSQL database
2. Use database queries instead of CSV file reading
3. More efficient for production

#### Option C: Use Sample Data (Development Only)
```bash
cd backend/database
python create_sample_data.py
```

### 3. Production Database Tables
Ensure these tables exist in your production database:
- `users` (for authentication)
- `invasive_species`
- `iucn_data`
- `freshwater_risk`
- `marine_hci`
- `terrestrial_risk`

## 🚨 Security Checklist

- [ ] Change SECRET_KEY from default value
- [ ] Update ALLOWED_ORIGINS to your actual frontend domain
- [ ] Verify DATABASE_URL doesn't contain hardcoded credentials
- [ ] Ensure .env file is in .gitignore (it is)
- [ ] Use HTTPS in production (automatic with hosting platforms)

## 📋 Testing Before Go-Live

### Backend Health Check
```bash
curl https://your-backend-domain.railway.app/health
# Should return: {"status": "healthy", "message": "Bioscope API is running"}
```

### Frontend API Connection
1. Deploy frontend with correct REACT_APP_API_URL
2. Test login functionality
3. Test search functionality
4. Verify CORS is working

### Database Connectivity
1. Check backend logs for database connection errors
2. Verify all required tables are present
3. Test a few API endpoints that query the database

## 🌐 Recommended Deployment Stack

### Backend: Railway (Recommended)
- Automatic GitHub deploys
- Built-in PostgreSQL
- Environment variables support
- $5/month credit (covers small apps)

### Frontend: Vercel (Recommended)
- Automatic GitHub deploys
- Perfect for React apps
- Custom domains
- Unlimited deployments on free tier

### Database: Railway PostgreSQL or Supabase
- Railway: Integrated with backend deployment
- Supabase: 500MB free, additional features

## 🔄 Deployment Commands

### Backend (Railway)
1. Connect GitHub repository
2. Set environment variables in Railway dashboard
3. Railway auto-deploys on git push

### Frontend (Vercel)
1. Connect GitHub repository
2. Set build command: `cd frontend && npm run build`
3. Set environment variables in Vercel dashboard
4. Vercel auto-deploys on git push

## ⚠️ Known Issues & Solutions

### Large Data Files
**Issue**: Some data files (>100MB) not in repository
**Solution**: Use cloud storage or database import (see section 2 above)

### CORS Errors
**Issue**: Frontend can't connect to backend
**Solution**: Verify ALLOWED_ORIGINS includes your frontend domain

### Database Connection
**Issue**: "Database connection failed"
**Solution**: Check DATABASE_URL format and database accessibility

## 🎉 Post-Deployment Verification

- [ ] Health check endpoint responds correctly
- [ ] Frontend loads without errors
- [ ] User registration works
- [ ] User login works
- [ ] Search functionality works
- [ ] Report generation works
- [ ] All API endpoints respond correctly

## 📞 Support Resources

- [Railway Documentation](https://docs.railway.app)
- [Vercel Documentation](https://vercel.com/docs)
- [Flask Production Deployment](https://flask.palletsprojects.com/en/2.2.x/deploying/)
- [React Production Build](https://create-react-app.dev/docs/deployment/)

---

**Status**: ✅ Repository is deployment-ready with configuration fixes applied!
