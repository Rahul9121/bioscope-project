# PowerShell script to test the registration endpoint

$backendUrl = "https://bioscope-project-production.up.railway.app"
$frontendUrl = "https://bioscope-project.vercel.app"

Write-Host "🧪 Testing Registration Endpoint" -ForegroundColor Green
Write-Host "=" * 50

# Test data
$testUser = @{
    hotel_name = "Test Hotel PowerShell"
    email = "test-ps@example.com"
    password = "TestPass123!"
}

$headers = @{
    "Content-Type" = "application/json"
    "Origin" = $frontendUrl
}

Write-Host "Backend URL: $backendUrl"
Write-Host "Frontend Origin: $frontendUrl"
Write-Host "Test data: $($testUser | ConvertTo-Json)"

try {
    # Test health endpoint first
    Write-Host "`n1. Testing health endpoint..." -ForegroundColor Yellow
    $healthResponse = Invoke-RestMethod -Uri "$backendUrl/health" -Method Get
    Write-Host "✅ Health check successful: $($healthResponse.message)" -ForegroundColor Green
    
    # Test database status
    Write-Host "`n2. Testing database status..." -ForegroundColor Yellow
    $dbResponse = Invoke-RestMethod -Uri "$backendUrl/db-status" -Method Get
    Write-Host "✅ Database status: $($dbResponse.status)" -ForegroundColor Green
    Write-Host "Database URL configured: $($dbResponse.database_url_configured)"
    Write-Host "Users table exists: $($dbResponse.users_table_exists)"
    
    # Test registration
    Write-Host "`n3. Testing registration..." -ForegroundColor Yellow
    $body = $testUser | ConvertTo-Json
    $registrationResponse = Invoke-RestMethod -Uri "$backendUrl/register" -Method Post -Headers $headers -Body $body
    
    Write-Host "✅ Registration successful: $($registrationResponse.message)" -ForegroundColor Green
    
} catch {
    $statusCode = $_.Exception.Response.StatusCode
    $errorMessage = $_.Exception.Message
    
    Write-Host "❌ Request failed with status: $statusCode" -ForegroundColor Red
    Write-Host "Error message: $errorMessage" -ForegroundColor Red
    
    try {
        $errorResponse = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($errorResponse)
        $errorBody = $reader.ReadToEnd()
        $errorJson = $errorBody | ConvertFrom-Json
        Write-Host "Error details: $($errorJson.error)" -ForegroundColor Red
    } catch {
        Write-Host "Could not parse error response"
    }
}

Write-Host "`nTest completed!" -ForegroundColor Green
