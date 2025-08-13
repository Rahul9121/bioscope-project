# Bioscope Deployment Verification Script
# This script tests backend health, database connectivity, and full registration flow

Write-Host "🔍 Bioscope Deployment Verification Started" -ForegroundColor Cyan

# Configuration - Update these URLs based on your actual deployments
$FRONTEND_URL = "https://bioscope-project.vercel.app"
$BACKEND_URL = "https://bioscope-project-production.up.railway.app"

# Alternative common Railway URL patterns to try if the above doesn't work
$RAILWAY_URL_PATTERNS = @(
    "https://web-production-*.up.railway.app",
    "https://bioscope-backend-*.up.railway.app", 
    "https://backend-production-*.up.railway.app",
    "https://app-production-*.up.railway.app"
)

Write-Host "`n📝 Testing Configuration:" -ForegroundColor Yellow
Write-Host "   Frontend: $FRONTEND_URL" -ForegroundColor White
Write-Host "   Backend:  $BACKEND_URL" -ForegroundColor White

# Test 1: Backend Health Check
Write-Host "`n🏥 Testing Backend Health..." -ForegroundColor Green
try {
    $healthResponse = Invoke-RestMethod -Uri "$BACKEND_URL/health" -Method GET -TimeoutSec 10
    Write-Host "✅ Backend Health: $($healthResponse.message)" -ForegroundColor Green
    Write-Host "   Status: $($healthResponse.status)" -ForegroundColor White
} catch {
    Write-Host "❌ Backend Health Check Failed!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    
    Write-Host "`n🔄 Trying common Railway URL patterns..." -ForegroundColor Yellow
    # Note: In a real scenario, you'd need to get the actual URL from Railway dashboard
    Write-Host "   Please check your Railway dashboard under 'Deployments' or 'Settings' > 'Domains'" -ForegroundColor Yellow
    Write-Host "   Look for a URL like: https://web-production-xxxx.up.railway.app" -ForegroundColor Yellow
    return
}

# Test 2: Database Status Check
Write-Host "`n🗄️ Testing Database Connection..." -ForegroundColor Green
try {
    $dbResponse = Invoke-RestMethod -Uri "$BACKEND_URL/db-status" -Method GET -TimeoutSec 15
    Write-Host "✅ Database Status: $($dbResponse.status)" -ForegroundColor Green
    Write-Host "   PostgreSQL Version: $($dbResponse.postgres_version)" -ForegroundColor White
    Write-Host "   Users Table Exists: $($dbResponse.users_table_exists)" -ForegroundColor White
    Write-Host "   Database URL Configured: $($dbResponse.database_url_configured)" -ForegroundColor White
} catch {
    Write-Host "❌ Database Connection Failed!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Check your DATABASE_URL in Railway environment variables" -ForegroundColor Yellow
    return
}

# Test 3: CORS Check with Frontend URL
Write-Host "`n🌐 Testing CORS Configuration..." -ForegroundColor Green
$headers = @{
    "Origin" = $FRONTEND_URL
    "Content-Type" = "application/json"
}

try {
    # Test CORS preflight for registration
    $corsResponse = Invoke-WebRequest -Uri "$BACKEND_URL/register" -Method OPTIONS -Headers $headers -TimeoutSec 10
    $corsHeaders = $corsResponse.Headers
    Write-Host "✅ CORS Preflight Successful" -ForegroundColor Green
    Write-Host "   Access-Control-Allow-Origin: $($corsHeaders.'Access-Control-Allow-Origin')" -ForegroundColor White
    Write-Host "   Access-Control-Allow-Credentials: $($corsHeaders.'Access-Control-Allow-Credentials')" -ForegroundColor White
} catch {
    Write-Host "⚠️ CORS Check Warning: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Test 4: Registration Flow Test
Write-Host "`n👤 Testing User Registration..." -ForegroundColor Green
$testUser = @{
    hotel_name = "Test Hotel Deployment $(Get-Date -Format 'yyyyMMdd-HHmmss')"
    email = "test-deploy-$(Get-Date -Format 'yyyyMMdd-HHmmss')@example.com"
    password = "TestPass123!"
} | ConvertTo-Json

try {
    $regResponse = Invoke-RestMethod -Uri "$BACKEND_URL/register" -Method POST -Body $testUser -ContentType "application/json" -Headers $headers -TimeoutSec 15
    Write-Host "✅ Registration Successful: $($regResponse.message)" -ForegroundColor Green
} catch {
    $errorDetail = $_.Exception.Message
    if ($_.Exception.Response) {
        try {
            $errorStream = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($errorStream)
            $errorDetail = $reader.ReadToEnd()
        } catch {}
    }
    Write-Host "❌ Registration Failed!" -ForegroundColor Red
    Write-Host "   Error: $errorDetail" -ForegroundColor Red
}

# Test 5: Frontend Accessibility
Write-Host "`n🖥️ Testing Frontend Accessibility..." -ForegroundColor Green
try {
    $frontendResponse = Invoke-WebRequest -Uri $FRONTEND_URL -Method GET -TimeoutSec 10
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✅ Frontend Accessible" -ForegroundColor Green
        Write-Host "   Status Code: $($frontendResponse.StatusCode)" -ForegroundColor White
    }
} catch {
    Write-Host "❌ Frontend Not Accessible!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Summary and Next Steps
Write-Host "`n📋 Verification Summary:" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "Backend URL: $BACKEND_URL" -ForegroundColor White
Write-Host "Frontend URL: $FRONTEND_URL" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. If backend health fails, verify the Railway URL in your dashboard" -ForegroundColor White
Write-Host "2. If database fails, check DATABASE_URL in Railway environment" -ForegroundColor White  
Write-Host "3. If registration fails, check CORS and database permissions" -ForegroundColor White
Write-Host "4. Test the actual frontend registration form manually" -ForegroundColor White

Write-Host "`n🎯 Manual Test URLs:" -ForegroundColor Cyan
Write-Host "Backend Health: $BACKEND_URL/health" -ForegroundColor White
Write-Host "Database Status: $BACKEND_URL/db-status" -ForegroundColor White
Write-Host "Frontend App: $FRONTEND_URL" -ForegroundColor White

Write-Host "`n✅ Verification Complete!" -ForegroundColor Green
