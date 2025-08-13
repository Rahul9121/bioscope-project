# Railway URL Discovery Script
# This script helps you find your Railway deployment URL

Write-Host "Railway URL Discovery Helper" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Gray

Write-Host ""
Write-Host "How to find your Railway URL:" -ForegroundColor Yellow
Write-Host "1. Go to https://railway.app" -ForegroundColor White
Write-Host "2. Sign in to your account" -ForegroundColor White
Write-Host "3. Select your bioscope project" -ForegroundColor White
Write-Host "4. Click on your backend service" -ForegroundColor White
Write-Host "5. Look for 'Settings > Domains' or 'Deployments' tab" -ForegroundColor White
Write-Host "6. Copy the URL that looks like:" -ForegroundColor White
Write-Host "   https://web-production-xxxx.up.railway.app" -ForegroundColor Green

Write-Host ""
Write-Host "Quick Health Test:" -ForegroundColor Green
$testUrl = Read-Host "Enter your Railway URL (or press Enter to skip)"

if (-not [string]::IsNullOrWhiteSpace($testUrl)) {
    Write-Host ""
    Write-Host "Testing: $testUrl/health" -ForegroundColor Cyan
    try {
        $response = Invoke-RestMethod -Uri "$testUrl/health" -Method GET -TimeoutSec 10
        Write-Host "SUCCESS! Your backend is running" -ForegroundColor Green
        Write-Host "Message: $($response.message)" -ForegroundColor White
        Write-Host "Status: $($response.status)" -ForegroundColor White
        Write-Host ""
        Write-Host "Update your scripts with this URL:" -ForegroundColor Yellow
        Write-Host "$testUrl" -ForegroundColor Green
    } catch {
        Write-Host "Failed to connect" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Double-check the URL and try again" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "Skipped URL test. Find your Railway URL and run this script again!" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Find your exact Railway URL from the dashboard" -ForegroundColor White
Write-Host "2. Run this script again to test the URL" -ForegroundColor White
Write-Host "3. Update test_deployment_verification.ps1 with the correct URL" -ForegroundColor White
Write-Host "4. Run the full verification test" -ForegroundColor White
