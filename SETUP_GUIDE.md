# 🚀 Bioscope Project Setup Guide

Complete guide to set up and deploy your biodiversity risk assessment application.

## 📋 Prerequisites

- Python 3.9+ installed
- Node.js 18+ installed  
- Git installed
- Supabase account (free tier)
- Railway account (free tier)
- Vercel account (free tier)

## 🎯 Step 1: Database Setup (Supabase)

### 1.1 Create Supabase Project
1. Go to [https://supabase.com](https://supabase.com)
2. Sign in with GitHub
3. Click "New project"
4. Project name: `bioscope-biodiversity`
5. Create strong database password (save it!)
6. Choose region closest to your users
7. Click "Create new project" (takes 2-3 minutes)

### 1.2 Get Connection String
1. Go to Settings → Database
2. Find "Connection string" section  
3. Copy the "URI" format:
   ```
   postgresql://postgres:[YOUR_PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
   ```
4. Note down your project reference (the random string in the URL)

## 🔧 Step 2: Local Environment Setup

### 2.1 Configure Environment Variables
1. Copy `.env.template` to `.env`
2. Update the following values in `.env`:
   ```env
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT_REF.supabase.co:5432/postgres
   SECRET_KEY=your_very_long_random_secret_key_here
   ALLOWED_ORIGINS=http://localhost:3000,https://bioscope-project.vercel.app
   ```

### 2.2 Install Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies (if testing locally)
cd frontend
npm install
cd ..
```

### 2.3 Test Database Connection
```bash
py test_supabase_connection.py
```

### 2.4 Initialize Database
```bash
py backend/init_db.py
```

### 2.5 Test Backend Locally
```bash
py start_dev.py
```

Visit http://localhost:5000/health to verify it's running.

## 🚢 Step 3: Deploy Backend (Railway)

### 3.1 Prepare Railway Deployment
1. Go to [https://railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your bioscope project repository

### 3.2 Configure Railway Environment Variables
In Railway dashboard, go to Variables and add:
```
DATABASE_URL=your_supabase_connection_string
SECRET_KEY=your_secret_key
ALLOWED_ORIGINS=http://localhost:3000,https://bioscope-project.vercel.app
PORT=5000
```

### 3.3 Deploy and Test
1. Railway will automatically deploy
2. Get your Railway domain: `https://your-app.up.railway.app`
3. Test endpoints:
   - Health check: `https://your-app.up.railway.app/health`
   - Database status: `https://your-app.up.railway.app/db-status`

## 🌐 Step 4: Deploy Frontend (Vercel)

### 4.1 Update Frontend Environment
1. In `frontend/.env.local`, set:
   ```env
   NEXT_PUBLIC_API_URL=https://your-app.up.railway.app
   ```

### 4.2 Deploy to Vercel
1. Go to [https://vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Set build command: `cd frontend && npm run build`
4. Set output directory: `frontend/.next`
5. Add environment variables:
   ```
   NEXT_PUBLIC_API_URL=https://your-app.up.railway.app
   ```
6. Deploy

## ✅ Step 5: Testing Complete Integration

### 5.1 Test Registration/Login
1. Visit your Vercel frontend URL
2. Try registering a new user
3. Try logging in

### 5.2 Test Risk Assessment
1. Go to Risk Assessment page
2. Enter a New Jersey ZIP code (e.g., "08540", "07001")
3. Verify map shows biodiversity data
4. Try generating and downloading reports

### 5.3 Common Test ZIP Codes
- Princeton: 08540
- Avenel: 07001  
- Lakewood: 08701
- North Brunswick: 08902

## 🔧 Troubleshooting

### Database Connection Issues
```bash
py test_supabase_connection.py
```

### Backend Deployment Issues
1. Check Railway logs
2. Verify environment variables
3. Test database connectivity

### Frontend Issues
1. Check browser console for errors
2. Verify API URLs in Network tab
3. Check CORS configuration

### CORS Issues
Update `ALLOWED_ORIGINS` in your environment variables to include your actual frontend domain.

## 📊 Monitoring and Logs

### Railway Backend Logs
- Go to Railway dashboard
- Click on your service
- View "Deployments" tab for logs

### Vercel Frontend Logs
- Go to Vercel dashboard
- Click on your project
- View "Functions" tab for logs

### Database Monitoring
- Use Supabase dashboard
- Monitor connections and queries
- Check table data

## 🚀 Going to Production

### Security Checklist
- [ ] Use strong SECRET_KEY
- [ ] Restrict ALLOWED_ORIGINS to your domains only
- [ ] Enable SSL on all endpoints
- [ ] Review database permissions
- [ ] Set up monitoring and backups

### Performance Optimization
- [ ] Enable caching where appropriate
- [ ] Optimize database queries
- [ ] Add database indexing
- [ ] Configure CDN for static assets

## 📞 Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Review logs in Railway/Vercel dashboards
3. Test each component individually
4. Verify environment variables are correct

## 🎉 Success!

Once everything is working:
- ✅ Database connected and initialized
- ✅ Backend deployed and accessible
- ✅ Frontend deployed and working
- ✅ Registration/login functional
- ✅ Risk assessment with real data
- ✅ Report generation working

Your biodiversity risk assessment application is now live!
