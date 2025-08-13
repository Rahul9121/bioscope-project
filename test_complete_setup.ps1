# Complete Setup Test Script
# Replace these URLs with your actual URLs

$backendUrl = "https://bioscope-project-production.up.railway.app"
$frontendUrl = "https://bioscope-project.vercel.app"

Write-Host "🧪 Complete Bioscope Setup Test" -ForegroundColor Green
Write-Host "=" * 50

Write-Host "Backend URL: $backendUrl" -ForegroundColor Cyan
Write-Host "Frontend URL: $frontendUrl" -ForegroundColor Cyan

# Test 1: Health Check
Write-Host "`n1. 🏥 Testing Backend Health..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-RestMethod -Uri "$backendUrl/health" -Method Get
    Write-Host "✅ Backend is running: $($healthResponse.message)" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend health check failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Check if Railway is deployed and running" -ForegroundColor Yellow
    exit 1
}

# Test 2: Database Connection
Write-Host "`n2. 🗄️ Testing Database Connection..." -ForegroundColor Yellow
try {
    $dbResponse = Invoke-RestMethod -Uri "$backendUrl/db-status" -Method Get
    if ($dbResponse.status -eq "connected") {
        Write-Host "✅ Database connected successfully!" -ForegroundColor Green
        Write-Host "   PostgreSQL version: $($dbResponse.postgres_version)" -ForegroundColor Cyan
        Write-Host "   Users table exists: $($dbResponse.users_table_exists)" -ForegroundColor Cyan
    } else {
        Write-Host "❌ Database connection failed: $($dbResponse.error)" -ForegroundColor Red
        Write-Host "   Check Railway environment variables" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "❌ Database status check failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test 3: Registration
Write-Host "`n3. 📝 Testing User Registration..." -ForegroundColor Yellow
$testUser = @{
    hotel_name = "Test Hotel Setup"
    email = "setup-test@example.com"
    password = "TestPass123!"
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
    "Origin" = $frontendUrl
}

try {
    $regResponse = Invoke-RestMethod -Uri "$backendUrl/register" -Method Post -Headers $headers -Body $testUser
    Write-Host "✅ Registration successful: $($regResponse.message)" -ForegroundColor Green
} catch {
    $statusCode = $_.Exception.Response.StatusCode
    Write-Host "❌ Registration failed with status: $statusCode" -ForegroundColor Red
    
    try {
        $errorStream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($errorStream)
        $errorBody = $reader.ReadToEnd()
        $errorJson = $errorBody | ConvertFrom-Json
        Write-Host "   Error: $($errorJson.error)" -ForegroundColor Red
    } catch {
        Write-Host "   Error details unavailable" -ForegroundColor Red
    }
    
    if ($statusCode -eq "BadRequest") {
        Write-Host "   This might be expected if user already exists" -ForegroundColor Yellow
    }
}

# Test 4: Frontend Access
Write-Host "`n4. 🌐 Testing Frontend Access..." -ForegroundColor Yellow
try {
    $frontendResponse = Invoke-WebRequest -Uri $frontendUrl -Method Head -UseBasicParsing
    if ($frontendResponse.StatusCode -eq 200) {
        Write-Host "✅ Frontend is accessible!" -ForegroundColor Green
        Write-Host "   You can now test registration at: $frontendUrl" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ Frontend not accessible: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Check Vercel deployment status" -ForegroundColor Yellow
}

Write-Host "`n🎉 Setup Test Complete!" -ForegroundColor Green
Write-Host "If all tests passed, your application should be working!" -ForegroundColor Green
