# 🚀 BiodivProScope Deployment Guide

This guide will help you deploy your BiodivProScope application for free using modern cloud platforms.

## 📋 Prerequisites

- GitHub account
- Your project pushed to GitHub
- Email accounts for deployment platforms

## 🎯 Recommended Free Hosting Stack

### 🗄️ Database: Supabase (Free PostgreSQL)
- **Free Tier**: 500MB database, 5GB bandwidth
- **Features**: Real-time subscriptions, authentication, APIs
- **Setup Time**: 5 minutes

### 🔧 Backend: Railway
- **Free Tier**: $5 monthly credits (covers small apps)
- **Features**: Auto-deploys from GitHub, built-in PostgreSQL
- **Setup Time**: 10 minutes

### 🌐 Frontend: Vercel
- **Free Tier**: Unlimited static sites, 100GB bandwidth
- **Features**: Auto-deploys from GitHub, custom domains
- **Setup Time**: 5 minutes

---

## 🗄️ Step 1: Database Setup (Supabase)

1. **Create Account**: Go to [supabase.com](https://supabase.com) and sign up
2. **New Project**: 
   - Click "New project"
   - Choose organization
   - Name: `bioscope-db`
   - Database Password: Generate a strong password (save it!)
   - Region: Choose closest to your users
   - Click "Create new project"
3. **Get Connection String**:
   - Go to Settings → Database
   - Copy the connection string under "Connection string"
   - Replace `[YOUR-PASSWORD]` with your actual password
   - Save this for later: `postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-REF].supabase.co:5432/postgres`

---

## 🔧 Step 2: Backend Deployment (Railway)

1. **Create Account**: Go to [railway.app](https://railway.app) and sign up with GitHub
2. **New Project**:
   - Click "New Project"
   - Choose "Deploy from GitHub repo"
   - Select your `bioscope-project` repository
   - Choose the backend directory if prompted
3. **Environment Variables**:
   - Go to your project → Variables tab
   - Add these variables:
     ```
     DATABASE_URL = [Your Supabase connection string from Step 1]
     FLASK_ENV = production
     PORT = 5001
     SECRET_KEY = [Generate a random secret key]
     ALLOWED_ORIGINS = https://your-project-name.vercel.app,http://localhost:3000
     ```
4. **Deploy**:
   - Railway will auto-deploy your backend
   - Copy your backend URL: `https://your-project-name.railway.app`

### Railway Alternative: Render

If Railway doesn't work, use [Render](https://render.com):
1. Create account with GitHub
2. New → Web Service
3. Connect your repository
4. Set build command: `cd backend && pip install -r requirements.txt`
5. Set start command: `cd backend && python app.py`
6. Add environment variables as above

---

## 🌐 Step 3: Frontend Deployment (Vercel)

1. **Create Account**: Go to [vercel.com](https://vercel.com) and sign up with GitHub
2. **Import Project**:
   - Click "New Project"
   - Select your `bioscope-project` repository
   - Framework Preset: React
   - Root Directory: `frontend`
   - Click "Deploy"
3. **Environment Variables**:
   - Go to Project Settings → Environment Variables
   - Add:
     ```
     REACT_APP_API_URL = [Your Railway backend URL from Step 2]
     ```
4. **Update Deployment**:
   - Go to Deployments tab
   - Click "Redeploy" to apply environment variables
5. **Custom Domain** (Optional):
   - Go to Settings → Domains
   - Add your custom domain if you have one

### Vercel Alternative: Netlify

If Vercel doesn't work, use [Netlify](https://netlify.com):
1. Create account with GitHub
2. New site from Git
3. Choose your repository
4. Build command: `cd frontend && npm run build`
5. Publish directory: `frontend/build`
6. Add environment variables in Site settings

---

## ⚙️ Step 4: Configuration Updates

### Update Backend CORS
Edit your Flask app to allow your frontend domain:

```python
# In your backend/app.py or main Flask file
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    "https://your-project-name.vercel.app",
    "http://localhost:3000"  # for development
])
```

### Update Frontend API Calls
Make sure your React app uses the environment variable:

```javascript
// In your frontend/src/services/api.js or similar
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';
```

---

## 🔄 Step 5: Enable Auto-Deployment

Both Vercel and Railway automatically deploy when you push to GitHub:

1. **Make changes** to your code
2. **Commit and push** to GitHub:
   ```bash
   git add .
   git commit -m "Update for production deployment"
   git push origin main
   ```
3. **Watch automatic deployments** in Vercel and Railway dashboards

---

## 🐞 Troubleshooting

### Common Issues

**Backend not starting**:
- Check Railway logs in the dashboard
- Ensure all environment variables are set
- Verify requirements.txt includes all dependencies

**Frontend can't connect to backend**:
- Check REACT_APP_API_URL environment variable
- Verify CORS settings in backend
- Check browser network tab for errors

**Database connection issues**:
- Verify DATABASE_URL is correct
- Check Supabase project is active
- Test connection from Railway logs

### Debugging Steps

1. **Check Logs**:
   - Railway: Project → Logs
   - Vercel: Project → Functions tab → View Function Logs
   - Supabase: Project → Logs

2. **Test Endpoints**:
   - Visit `https://your-backend.railway.app/api/health` (add a health check route)
   - Check if database tables are created

3. **Environment Variables**:
   - Double-check all variables are set correctly
   - No typos in variable names
   - Values don't have extra spaces

---

## 💰 Cost Monitoring

### Free Tier Limits
- **Supabase**: 500MB database, 5GB bandwidth
- **Railway**: $5 monthly credits (depletes with usage)
- **Vercel**: 100GB bandwidth, unlimited deployments

### Upgrade Considerations
- **Railway**: $20/month for unlimited
- **Supabase**: $25/month for Pro features
- **Vercel**: $20/month for Pro features

---

## 🔒 Security Best Practices

1. **Environment Variables**: Never commit `.env` files
2. **Database**: Use strong passwords
3. **API Keys**: Rotate regularly
4. **CORS**: Restrict to your domain only
5. **HTTPS**: Always use HTTPS in production (automatic with these platforms)

---

## 🎉 You're Live!

After completing these steps, your application will be live at:
- **Frontend**: `https://your-project-name.vercel.app`
- **Backend API**: `https://your-project-name.railway.app`
- **Database**: Managed by Supabase

### Share Your Project
- Add your live URL to your GitHub README
- Share with colleagues, professors, or on social media
- Consider adding your project to your portfolio

---

## 📞 Support

If you run into issues:
1. Check the troubleshooting section above
2. Review platform documentation:
   - [Vercel Docs](https://vercel.com/docs)
   - [Railway Docs](https://docs.railway.app)
   - [Supabase Docs](https://supabase.com/docs)
3. Check GitHub issues in your repository
4. Post questions on Stack Overflow with relevant tags

**Happy Deploying! 🚀**
