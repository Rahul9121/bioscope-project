# Railway URL Discovery Script
# This script helps you find and test your Railway deployment URL

Write-Host "🚂 Railway URL Discovery Helper" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

Write-Host "`n📋 How to find your Railway URL:" -ForegroundColor Yellow
Write-Host "1. Go to https://railway.app" -ForegroundColor White
Write-Host "2. Sign in to your account" -ForegroundColor White
Write-Host "3. Select your 'bioscope project'" -ForegroundColor White
Write-Host "4. Click on your backend service/deployment" -ForegroundColor White
Write-Host "5. Look for one of these sections:" -ForegroundColor White
Write-Host "   • 'Settings' > 'Domains'" -ForegroundColor Cyan
Write-Host "   • 'Deployments' tab" -ForegroundColor Cyan
Write-Host "   • 'Overview' page" -ForegroundColor Cyan
Write-Host "6. Copy the URL that looks like:" -ForegroundColor White
Write-Host "   https://web-production-xxxx.up.railway.app" -ForegroundColor Green
Write-Host "   https://backend-production-xxxx.up.railway.app" -ForegroundColor Green
Write-Host "   https://app-production-xxxx.up.railway.app" -ForegroundColor Green

Write-Host "`n🧪 Common Railway URL patterns to test:" -ForegroundColor Yellow

$commonPatterns = @(
    "https://bioscope-project-production.up.railway.app",
    "https://web-production-*.up.railway.app",
    "https://backend-production-*.up.railway.app",
    "https://app-production-*.up.railway.app",
    "https://bioscope-backend-*.up.railway.app"
)

foreach ($pattern in $commonPatterns) {
    Write-Host "• $pattern" -ForegroundColor Cyan
}

Write-Host "`n🔧 Test your Railway URL:" -ForegroundColor Yellow
Write-Host "Once you have the correct URL, replace it in these files:" -ForegroundColor White
Write-Host "• test_deployment_verification.ps1 (line 7)" -ForegroundColor Cyan
Write-Host "• Any other test scripts" -ForegroundColor Cyan

Write-Host "`n✅ Quick Health Test:" -ForegroundColor Green
$testUrl = Read-Host "Enter your Railway URL (or press Enter to skip)"

if ($testUrl -and $testUrl -ne "") {
    Write-Host "`n🔍 Testing: $testUrl/health" -ForegroundColor Cyan
    try {
        $response = Invoke-RestMethod -Uri "$testUrl/health" -Method GET -TimeoutSec 10
        Write-Host "✅ Success! Your backend is running" -ForegroundColor Green
        Write-Host "   Message: $($response.message)" -ForegroundColor White
        Write-Host "   Status: $($response.status)" -ForegroundColor White
        
        Write-Host "`n🎯 Update your scripts with this URL:" -ForegroundColor Yellow
        Write-Host "$testUrl" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to connect" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "   Double-check the URL and try again" -ForegroundColor Yellow
    }
} else {
    Write-Host "`nSkipped URL test. Find your Railway URL and run this script again!" -ForegroundColor Yellow
}

Write-Host "`n📝 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Find your exact Railway URL from the dashboard" -ForegroundColor White  
Write-Host "2. Run this script again to test the URL" -ForegroundColor White
Write-Host "3. Update test_deployment_verification.ps1 with the correct URL" -ForegroundColor White
Write-Host "4. Run the full verification test" -ForegroundColor White
