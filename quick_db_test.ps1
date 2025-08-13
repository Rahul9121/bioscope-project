# Quick Database Test - Replace YOUR_RAILWAY_URL with your actual URL
param([string]$url = "REPLACE_WITH_YOUR_RAILWAY_URL")

if ($url -eq "REPLACE_WITH_YOUR_RAILWAY_URL") {
    Write-Host "❌ Please provide your Railway URL!" -ForegroundColor Red
    Write-Host "Usage: .\quick_db_test.ps1 -url 'https://your-railway-url.up.railway.app'" -ForegroundColor Yellow
    exit 1
}

Write-Host "🧪 Quick Database Connection Test" -ForegroundColor Green
Write-Host "Testing: $url" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "1. Testing Backend..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$url/health" -TimeoutSec 10
    Write-Host "   ✅ Backend is running: $($health.message)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Backend failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test 2: Database Status
Write-Host "2. Testing Database..." -ForegroundColor Yellow
try {
    $db = Invoke-RestMethod -Uri "$url/db-status" -TimeoutSec 10
    if ($db.status -eq "connected") {
        Write-Host "   ✅ Database connected!" -ForegroundColor Green
        Write-Host "   Users table exists: $($db.users_table_exists)" -ForegroundColor Cyan
        
        if ($db.users_table_exists) {
            Write-Host "   🎉 Everything looks good! Registration should work." -ForegroundColor Green
        } else {
            Write-Host "   ⚠️ Need to create users table in Supabase" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ❌ Database connection failed!" -ForegroundColor Red
        Write-Host "   Error: $($db.error)" -ForegroundColor Red
        Write-Host "   URL configured: $($db.database_url_configured)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ Database test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🏁 Test complete!" -ForegroundColor Green
