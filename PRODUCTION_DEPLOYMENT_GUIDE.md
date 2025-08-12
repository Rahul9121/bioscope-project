# Bioscope App Production Deployment Guide

Your app has extensive data and functionality, but needs proper database setup. Follow these steps to get everything working.

## 🔧 Step 1: Configure Database Credentials

1. **Update your `.env` file** with your actual Supabase credentials:
   ```
   # Replace [YOUR-SUPABASE-PASSWORD] with your actual password
   # Replace [YOUR-PROJECT-REF] with your project reference
   DATABASE_URL=postgresql://postgres:your_actual_password@db.your_project_ref.supabase.co:5432/postgres
   
   # Update these URLs with your actual deployment URLs
   ALLOWED_ORIGINS=https://your-frontend-app.vercel.app,https://bioscope-project-production.up.railway.app,http://localhost:3000
   ```

2. **Get your Supabase credentials:**
   - Go to your Supabase project
   - Settings > Database > Connection string
   - Copy the connection string and update your `.env` file

## 🧪 Step 2: Test Database Connection

Run the connection test:
```bash
python test_db_connection.py
```

If successful, proceed to Step 3. If it fails, check your database credentials.

## 📊 Step 3: Setup Database with Your Data

This will create all tables and load your CSV data:
```bash
python setup_production_database.py
```

This script will:
- Create all necessary database tables
- Load your freshwater risk data (thousands of records)
- Load your terrestrial risk data (thousands of records) 
- Load your marine HCI data
- Load your IUCN sample data
- Add invasive species data
- Create performance indexes

## 🚀 Step 4: Deploy to Railway (Backend)

1. **Set Environment Variables in Railway:**
   - Go to your Railway project dashboard
   - Add these environment variables:
     ```
     DATABASE_URL=your_supabase_connection_string
     ALLOWED_ORIGINS=https://your-frontend-app.vercel.app,http://localhost:3000
     SECRET_KEY=your-secret-key
     FLASK_ENV=production
     PORT=5001
     ```

2. **Redeploy your Railway app** to apply the new environment variables

## 🌐 Step 5: Deploy to Vercel (Frontend)

1. **Update your frontend `.env.production`:**
   ```
   REACT_APP_API_URL=https://your-railway-backend-url.railway.app
   ```

2. **Redeploy your Vercel app**

## ✅ Step 6: Verify Everything Works

1. **Test the backend API:**
   ```bash
   curl https://your-railway-backend-url.railway.app/health
   ```

2. **Test the frontend:**
   - Visit your Vercel app URL
   - Try searching for a New Jersey location (e.g., "07663" or "Princeton, NJ")
   - Verify you see risk data points on the map

## 🔍 What Your App Does Now

With all your data loaded, your app provides:

- **Freshwater Risk Assessment**: Analysis of freshwater ecosystems
- **Terrestrial Risk Assessment**: Land-based biodiversity risks  
- **Marine Risk Assessment**: Ocean and coastal ecosystem analysis
- **Invasive Species Tracking**: Non-native species monitoring
- **IUCN Data Integration**: Conservation status information
- **Risk Mitigation Reports**: Actionable recommendations
- **Interactive Mapping**: Visual risk assessment tools

## 🛠️ Troubleshooting

### Database Connection Issues:
- Verify Supabase credentials in `.env`
- Check that your Supabase project is active
- Ensure your IP is whitelisted in Supabase

### CORS Issues:
- Update `ALLOWED_ORIGINS` with your actual frontend URL
- Redeploy backend after changing CORS settings

### Data Loading Issues:
- Check that CSV files exist in `backend/database/`
- Verify database has enough storage space
- Review logs in the setup script

### Frontend-Backend Connection:
- Ensure `REACT_APP_API_URL` points to your Railway backend
- Check that both deployments are using HTTPS

## 📈 Performance Notes

Your app handles large datasets:
- Freshwater risk: ~thousands of coordinates
- Terrestrial risk: ~thousands of coordinates  
- Marine HCI: ~thousands of coordinates
- Database indexes are created for optimal query performance
- Data is chunked during loading to handle large files

## 🔐 Security Considerations

- Environment variables contain sensitive data
- Database credentials are never exposed in code
- CORS is properly configured for your domains
- Secret keys are environment-specific

---

## Quick Commands Summary

```bash
# Test database connection
python test_db_connection.py

# Setup production database with all data
python setup_production_database.py

# Test local development
python backend/app.py
```

Your app is now production-ready with all your critical biodiversity data!
