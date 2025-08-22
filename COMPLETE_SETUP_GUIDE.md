# 🌱 Complete Bioscope Database Setup Guide

This guide will help you complete all three steps to get your biodiversity risk assessment application fully functional with real data.

## 📋 Overview

You now have three essential files:
1. **`supabase_setup_complete.sql`** - Complete database schema setup
2. **`data_loader.py`** - Real data loading script  
3. This setup guide

## 🗂️ Step 1: Test Current Search Functionality

### Option A: Test via Railway Deployment (Recommended)

1. **Find your Railway URL**:
   ```powershell
   ./find_railway_url.ps1
   ```

2. **Test health endpoint**:
   ```bash
   curl https://YOUR_RAILWAY_URL/health
   ```

3. **Test database status**:
   ```bash
   curl https://YOUR_RAILWAY_URL/db-status
   ```

4. **Test search functionality**:
   ```bash
   curl -X POST https://YOUR_RAILWAY_URL/search \
        -H "Content-Type: application/json" \
        -d '{"input_text": "08540"}'
   ```

### Option B: Test Locally

Since Python isn't available in your PowerShell, you can check the deployment status from your Railway dashboard directly:

1. Go to https://railway.app
2. Sign into your account
3. Navigate to your bioscope project
4. Check the deployment status and logs

## 🗄️ Step 2: Setup Database Tables in Supabase

### Instructions:

1. **Open Supabase Dashboard**:
   - Go to https://supabase.com/dashboard
   - Sign in to your account
   - Select your bioscope project

2. **Open SQL Editor**:
   - In the left sidebar, click "SQL Editor"
   - Click "New query"

3. **Run the Setup Script**:
   - Copy the entire contents of `supabase_setup_complete.sql`
   - Paste into the SQL editor
   - Click "Run" button

4. **Verify Success**:
   - You should see success messages
   - Check the "Table Editor" tab to confirm tables are created
   - Verify sample data is inserted

### Expected Results:
```
✅ All tables created with sample data
✅ Indexes created for optimal performance  
✅ Ready for biodiversity risk assessment queries

Table Summary:
- users: 1 record
- invasive_species: 10 records
- iucn_data: 10 records  
- freshwater_risk: 10 records
- marine_hci: 10 records
- terrestrial_risk: 10 records
```

## 📊 Step 3: Load Comprehensive Data

### Prerequisites:
- Python 3.7+ installed
- psycopg2 library: `pip install psycopg2-binary`
- Your CSV files in `backend/database/` directory

### Instructions:

1. **Install Dependencies** (if needed):
   ```bash
   pip install psycopg2-binary
   ```

2. **Run Data Loader**:
   ```bash
   python data_loader.py
   ```

### What the Data Loader Does:

1. **Connects** to your Supabase database
2. **Clears** existing biodiversity data (keeps users)
3. **Loads real CSV data**:
   - Freshwater risk data from your CSV
   - Marine HCI data from your CSV  
4. **Creates comprehensive sample data**:
   - 21 invasive species records for New Jersey
   - 15 IUCN conservation status records
   - 15 terrestrial risk assessment records
5. **Filters data** to New Jersey geographic bounds
6. **Verifies** data loading with test queries

### Expected Output:
```
🚀 Bioscope Data Loader - Loading Real Biodiversity Data
============================================================
✅ Connected to Supabase database

🧹 Clearing existing biodiversity data...
✅ Tables cleared successfully

🌊 Loading freshwater risk data...
✅ Loaded 150+ freshwater risk records

🌊 Loading marine HCI data...  
✅ Loaded 200+ marine HCI records

🦎 Creating invasive species data...
✅ Loaded 21 invasive species records

🦅 Creating IUCN conservation data...
✅ Loaded 15 IUCN conservation records

🌲 Creating sample terrestrial risk data...
✅ Loaded 15 terrestrial risk records

🔍 Verifying data loading...
📊 Total biodiversity records: 400+

🧪 Testing sample search query...
✅ Search functionality verified with 25+ total results

🎉 Data loading completed successfully!
   Database is ready for biodiversity risk assessment
```

## ✅ Verification Steps

After completing all three steps:

### 1. Database Verification
In Supabase dashboard → Table Editor, check:
- `invasive_species`: Should have 21 records
- `iucn_data`: Should have 15 records
- `freshwater_risk`: Should have 150+ records
- `marine_hci`: Should have 200+ records
- `terrestrial_risk`: Should have 15 records

### 2. Application Testing
Test your frontend at https://bioscope-project.vercel.app:
- Enter New Jersey ZIP codes: `08540`, `07001`, `08902`
- Verify map renders with risk indicators
- Check that biodiversity data displays
- Confirm risk levels are calculated

### 3. API Testing
Test your backend search endpoint:
```bash
curl -X POST https://YOUR_RAILWAY_URL/search \
     -H "Content-Type: application/json" \
     -d '{"input_text": "40.0583,-74.4057"}'
```

Should return comprehensive biodiversity risk data.

## 🔧 Troubleshooting

### Database Connection Issues:
- Verify Supabase URL in `.env.railway`
- Check that database is running in Supabase dashboard
- Ensure SSL connection is enabled

### Data Loading Issues:
- Check that CSV files exist in `backend/database/`
- Verify Python dependencies are installed
- Run the setup SQL script first before data loading

### Search Returns No Results:
- Confirm data was loaded for New Jersey coordinates
- Check that your search coordinates are within NJ bounds
- Verify backend deployment is working

## 🎯 Success Criteria

Your setup is complete when:
- ✅ Database has 400+ biodiversity records
- ✅ Search API returns real data for NJ locations  
- ✅ Frontend displays interactive risk maps
- ✅ All 5 biodiversity tables are populated
- ✅ Test queries return expected results

## 📞 Next Steps

Once setup is complete:
1. Test with multiple New Jersey locations
2. Verify report generation functionality  
3. Check user registration and authentication
4. Deploy any additional features needed

Your Bioscope application will now provide comprehensive biodiversity risk assessments using real scientific data for the New Jersey region!
