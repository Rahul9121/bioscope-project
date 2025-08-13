# Simple Railway Backend Test
$BACKEND_URL = "https://bioscope-project-production.up.railway.app"
$FRONTEND_URL = "https://bioscope-project.vercel.app"

Write-Host "Testing Bioscope Deployment" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Gray
Write-Host "Backend: $BACKEND_URL" -ForegroundColor White
Write-Host "Frontend: $FRONTEND_URL" -ForegroundColor White
Write-Host ""

# Test 1: Backend Health
Write-Host "1. Testing Backend Health..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$BACKEND_URL/health" -Method GET -TimeoutSec 10
    Write-Host "   SUCCESS! Backend is running" -ForegroundColor Green
    Write-Host "   Message: $($health.message)" -ForegroundColor White
    Write-Host "   Status: $($health.status)" -ForegroundColor White
} catch {
    Write-Host "   FAILED! Backend not accessible" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possible issues:" -ForegroundColor Yellow
    Write-Host "- Railway deployment failed" -ForegroundColor White
    Write-Host "- Environment variables missing" -ForegroundColor White
    Write-Host "- Build errors in Railway logs" -ForegroundColor White
    return
}

Write-Host ""

# Test 2: Database Connection
Write-Host "2. Testing Database Connection..." -ForegroundColor Yellow
try {
    $db = Invoke-RestMethod -Uri "$BACKEND_URL/db-status" -Method GET -TimeoutSec 15
    Write-Host "   SUCCESS! Database connected" -ForegroundColor Green
    Write-Host "   Status: $($db.status)" -ForegroundColor White
    Write-Host "   Users table exists: $($db.users_table_exists)" -ForegroundColor White
    Write-Host "   Database URL configured: $($db.database_url_configured)" -ForegroundColor White
} catch {
    Write-Host "   FAILED! Database connection error" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check Railway environment variables:" -ForegroundColor Yellow
    Write-Host "- DATABASE_URL should be your Supabase connection string" -ForegroundColor White
    return
}

Write-Host ""

# Test 3: Frontend
Write-Host "3. Testing Frontend..." -ForegroundColor Yellow
try {
    $frontend = Invoke-WebRequest -Uri $FRONTEND_URL -Method GET -TimeoutSec 10
    Write-Host "   SUCCESS! Frontend accessible" -ForegroundColor Green
    Write-Host "   Status Code: $($frontend.StatusCode)" -ForegroundColor White
} catch {
    Write-Host "   FAILED! Frontend not accessible" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 4: Simple Registration Test
Write-Host "4. Testing Registration Endpoint..." -ForegroundColor Yellow
$testData = @{
    hotel_name = "Test Hotel $(Get-Date -Format 'MMddHHmm')"
    email = "test$(Get-Date -Format 'MMddHHmm')@example.com"
    password = "TestPass123"
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
    "Origin" = $FRONTEND_URL
}

try {
    $reg = Invoke-RestMethod -Uri "$BACKEND_URL/register" -Method POST -Body $testData -Headers $headers -TimeoutSec 15
    Write-Host "   SUCCESS! Registration works" -ForegroundColor Green
    Write-Host "   Message: $($reg.message)" -ForegroundColor White
} catch {
    Write-Host "   FAILED! Registration error" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Test Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Manual test URLs:" -ForegroundColor Yellow
Write-Host "Backend Health: $BACKEND_URL/health" -ForegroundColor White
Write-Host "Database Status: $BACKEND_URL/db-status" -ForegroundColor White
Write-Host "Frontend: $FRONTEND_URL" -ForegroundColor White
