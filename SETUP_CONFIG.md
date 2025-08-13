# 🔧 Bioscope Project Configuration Guide

## 📋 URLs and Credentials Checklist

Fill in your actual values:

### Railway Backend URL:
```
https://[YOUR-RAILWAY-SUBDOMAIN].up.railway.app
```

### Vercel Frontend URL:
```
https://[YOUR-VERCEL-SUBDOMAIN].vercel.app
```

### Supabase Database URL:
```
postgresql://postgres.[PROJECT_ID]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

## ⚙️ Railway Environment Variables

Set these in Railway Dashboard → Variables:

```
DATABASE_URL=postgresql://postgres.[PROJECT_ID]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
FLASK_ENV=production
SECRET_KEY=bioscope-super-secret-key-2024-production
ALLOWED_ORIGINS=http://localhost:3000,https://[YOUR-VERCEL-SUBDOMAIN].vercel.app
PORT=5001
```

## 🌐 Vercel Environment Variables

Set these in Vercel Dashboard → Settings → Environment Variables:

```
REACT_APP_API_URL=https://[YOUR-RAILWAY-SUBDOMAIN].up.railway.app
```

## 🧪 Test URLs

### Health Check:
```
https://[YOUR-RAILWAY-SUBDOMAIN].up.railway.app/health
```

### Database Status:
```
https://[YOUR-RAILWAY-SUBDOMAIN].up.railway.app/db-status
```

### Registration Test:
```
https://[YOUR-VERCEL-SUBDOMAIN].vercel.app
```

## ✅ Verification Steps

1. Visit health check URL - should return: `{"status": "healthy", "message": "Bioscope API is running"}`
2. Visit database status URL - should return: `{"status": "connected", "users_table_exists": true}`
3. Visit your frontend URL and try to register a new user
