# Database Connection Checker for Bioscope Project
# Replace the URL below with your actual Railway URL

param(
    [string]$BackendUrl = "https://your-actual-railway-url.up.railway.app"
)

Write-Host "🔍 Bioscope Database Connection Checker" -ForegroundColor Green
Write-Host "=" * 50

if ($BackendUrl -eq "https://your-actual-railway-url.up.railway.app") {
    Write-Host "❌ Please update the script with your actual Railway URL!" -ForegroundColor Red
    Write-Host "Usage: .\check_database_connection.ps1 -BackendUrl 'https://your-railway-url.up.railway.app'" -ForegroundColor Yellow
    exit 1
}

Write-Host "Testing backend: $BackendUrl" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "1. 🏥 Testing Backend Health..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-RestMethod -Uri "$BackendUrl/health" -Method Get -TimeoutSec 15
    if ($healthResponse.status -eq "healthy") {
        Write-Host "   ✅ Backend is running!" -ForegroundColor Green
        Write-Host "   Message: $($healthResponse.message)" -ForegroundColor Cyan
    } else {
        Write-Host "   ⚠️ Backend responded but status is not healthy" -ForegroundColor Yellow
        Write-Host "   Response: $($healthResponse | ConvertTo-Json)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ Backend is not accessible!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔧 Troubleshooting steps:" -ForegroundColor Yellow
    Write-Host "   1. Check if Railway service is deployed and running" -ForegroundColor Yellow
    Write-Host "   2. Verify the URL is correct in Railway dashboard" -ForegroundColor Yellow
    Write-Host "   3. Check Railway deployment logs for errors" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Test 2: Database Connection
Write-Host "2. 🗄️ Testing Database Connection..." -ForegroundColor Yellow
try {
    $dbResponse = Invoke-RestMethod -Uri "$BackendUrl/db-status" -Method Get -TimeoutSec 15
    
    Write-Host "   Database Status: $($dbResponse.status)" -ForegroundColor $(if ($dbResponse.status -eq "connected") { "Green" } else { "Red" })
    
    if ($dbResponse.status -eq "connected") {
        Write-Host "   ✅ Database connection successful!" -ForegroundColor Green
        Write-Host "   PostgreSQL Version: $($dbResponse.postgres_version)" -ForegroundColor Cyan
        Write-Host "   Database URL Configured: $($dbResponse.database_url_configured)" -ForegroundColor Cyan
        Write-Host "   Users Table Exists: $($dbResponse.users_table_exists)" -ForegroundColor Cyan
        
        if (-not $dbResponse.users_table_exists) {
            Write-Host "   ⚠️ WARNING: Users table doesn't exist!" -ForegroundColor Yellow
            Write-Host "   You need to run the database setup script in Supabase" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ❌ Database connection failed!" -ForegroundColor Red
        Write-Host "   Error: $($dbResponse.error)" -ForegroundColor Red
        Write-Host "   Database URL Configured: $($dbResponse.database_url_configured)" -ForegroundColor Yellow
        
        Write-Host ""
        Write-Host "🔧 Database Troubleshooting:" -ForegroundColor Yellow
        if (-not $dbResponse.database_url_configured) {
            Write-Host "   1. DATABASE_URL is not set in Railway environment variables!" -ForegroundColor Red
            Write-Host "   2. Go to Railway → Variables → Add DATABASE_URL" -ForegroundColor Yellow
        } else {
            Write-Host "   1. DATABASE_URL is set but connection failed" -ForegroundColor Yellow
            Write-Host "   2. Check if Supabase database is running" -ForegroundColor Yellow
            Write-Host "   3. Verify DATABASE_URL format is correct" -ForegroundColor Yellow
            Write-Host "   4. Check if SSL is required (Supabase needs SSL)" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "   ❌ Failed to check database status!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 3: Registration Test (if database is working)
if ($dbResponse.status -eq "connected" -and $dbResponse.users_table_exists) {
    Write-Host "3. 📝 Testing User Registration..." -ForegroundColor Yellow
    
    $testUser = @{
        hotel_name = "Database Test Hotel"
        email = "dbtest-$(Get-Date -Format 'yyyyMMddHHmmss')@example.com"
        password = "TestPass123!"
    } | ConvertTo-Json
    
    $headers = @{
        "Content-Type" = "application/json"
        "Origin" = "https://bioscope-project.vercel.app"
    }
    
    try {
        $regResponse = Invoke-RestMethod -Uri "$BackendUrl/register" -Method Post -Headers $headers -Body $testUser -TimeoutSec 15
        Write-Host "   ✅ Registration test successful!" -ForegroundColor Green
        Write-Host "   Message: $($regResponse.message)" -ForegroundColor Cyan
    } catch {
        $statusCode = $_.Exception.Response.StatusCode
        Write-Host "   Registration test failed with status: $statusCode" -ForegroundColor Red
        
        try {
            $errorStream = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($errorStream)
            $errorBody = $reader.ReadToEnd()
            $errorJson = $errorBody | ConvertFrom-Json
            Write-Host "   Error: $($errorJson.error)" -ForegroundColor Red
        } catch {
            Write-Host "   Error details unavailable" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "🎉 Database Connection Check Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
if ($dbResponse.status -eq "connected" -and $dbResponse.users_table_exists) {
    Write-Host "   ✅ Your database is working correctly!" -ForegroundColor Green
    Write-Host "   🌐 Test your frontend at: https://bioscope-project.vercel.app" -ForegroundColor Cyan
} else {
    Write-Host "   1. Fix the database connection issues above" -ForegroundColor Yellow
    Write-Host "   2. Set Railway environment variables if needed" -ForegroundColor Yellow
    Write-Host "   3. Run this script again to verify fixes" -ForegroundColor Yellow
}
