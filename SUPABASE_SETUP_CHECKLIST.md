# 🚀 Supabase Database Setup Checklist

## 📋 Pre-Setup Checklist
- [ ] Python 3.9+ installed
- [ ] All dependencies installed (`py -m pip install -r requirements.txt`)
- [ ] Data files present in `backend/database/`

## 🎯 Step 1: Create Supabase Project

### 1.1 Account Setup
1. **Go to Supabase:** https://supabase.com
2. **Sign up/Login** with GitHub
3. **Create Organization** (if needed)

### 1.2 Create Project
1. Click **"New project"**
2. **Project name:** `bioscope-biodiversity`
3. **Database password:** Create strong password (SAVE THIS!)
4. **Region:** Choose closest to you:
   - US East (N. Virginia) 
   - US West (Oregon)
   - EU West (Ireland)
   - Asia Southeast (Singapore)
5. Click **"Create new project"**

⏱️ **Wait 2-3 minutes for initialization**

## 🔗 Step 2: Get Connection Details

### 2.1 Database Connection String
1. Go to **Settings** → **Database** 
2. Scroll to **"Connection string"** section
3. Copy the **"URI"** format (NOT psql command)
4. Format: `postgresql://postgres:[password]@db.[ref].supabase.co:5432/postgres`

### 2.2 Save Your Details
- **Project Reference:** Random string in URL (e.g., `abcdefghijklmnop`)
- **Database Password:** Your chosen password
- **Full Connection String:** Complete URI from above

## ⚙️ Step 3: Configure Local Environment

### 3.1 Update .env File
Open your `.env` file and replace these values:

```env
# Replace with your actual Supabase connection string
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT_REF.supabase.co:5432/postgres

# Generate a random secret key
SECRET_KEY=your_super_long_random_secret_key_here_change_this

# Update with your frontend domain
ALLOWED_ORIGINS=http://localhost:3000,https://bioscope-project.vercel.app
```

### 3.2 Test Connection
```bash
py test_supabase_connection.py
```

Expected output:
```
✅ Connected successfully!
📊 PostgreSQL version: PostgreSQL 15.x...
📋 Database is empty - tables need to be created
💡 Run: python backend/init_db.py to initialize
```

## 📊 Step 4: Load Your Data

### 4.1 Initialize Database with All Data
```bash
py init_supabase_with_data.py
```

This will:
- Create optimized database tables
- Load 14,509 invasive species records
- Load 257,895 freshwater risk records  
- Load 233,336 terrestrial risk records
- Load 10,000 marine HCI records (sample)
- Create sample biodiversity data
- Create test user account

**Expected duration:** 10-15 minutes

### 4.2 Verify Data Load
```bash
py test_supabase_connection.py
```

Expected output:
```
✅ Connected successfully!
👥 Users table has 1 records
🌿 Biodiversity risks table has 12 records
```

## ✅ Step 5: Test Your Setup

### 5.1 Test Backend Locally
```bash
py start_dev.py
```

### 5.2 Test Endpoints
Open browser and visit:
- **Health Check:** http://localhost:5000/health
- **Database Status:** http://localhost:5000/db-status

### 5.3 Test API Endpoints
Use a tool like Postman or curl:

```bash
# Test registration
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"hotel_name":"Test Hotel","email":"user@test.com","password":"password123"}'

# Test search
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{"input_text":"08540"}'
```

## 🚀 Step 6: Ready for Deployment

Once local testing works:
1. **Deploy backend to Railway** (see SETUP_GUIDE.md)
2. **Deploy frontend to Vercel** 
3. **Update environment variables** on hosting platforms
4. **Test live endpoints**

## 🔧 Troubleshooting

### Connection Issues
- [ ] Check DATABASE_URL format
- [ ] Verify password is correct
- [ ] Ensure project is fully initialized
- [ ] Try from different network

### Data Loading Issues
- [ ] Check file paths in `backend/database/`
- [ ] Verify all dependencies installed
- [ ] Check available disk space
- [ ] Monitor Supabase dashboard for errors

### Performance Issues
- [ ] Large datasets may take 10-15 minutes
- [ ] Monitor memory usage during load
- [ ] Check internet connection stability

## 📞 Support Resources

### Supabase Documentation
- Getting Started: https://supabase.com/docs
- Database Guide: https://supabase.com/docs/guides/database

### Your Test Credentials
- **Test User:** test@bioscope.com
- **Test Password:** Test123!
- **Test ZIP Codes:** 08540, 07001, 08701, 08902

## 🎉 Success Indicators

✅ **Database Ready When:**
- Connection test passes
- All tables created with data
- Health check returns HTTP 200
- Search API returns biodiversity data
- User registration/login works

✅ **Production Ready When:**
- Backend deployed to Railway
- Frontend deployed to Vercel  
- All environment variables configured
- End-to-end testing successful
