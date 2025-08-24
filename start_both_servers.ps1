# Bioscope Project - Start Both Frontend and Backend Servers
Write-Host "🌿 BiodivProScope - Starting Full Stack Application" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host ""

# Step 1: Start Backend Server
Write-Host "🔥 Step 1: Starting Backend Server..." -ForegroundColor Yellow
Write-Host "Backend will run on: http://localhost:5001" -ForegroundColor Cyan

Set-Location "backend"
Start-Process -WindowStyle Normal -FilePath "venv\Scripts\python.exe" -ArgumentList "minimal_app.py"
Start-Sleep -Seconds 3

# Test backend health
try {
    $backendHealth = Invoke-RestMethod -Uri "http://localhost:5001/health" -Method GET
    Write-Host "✅ Backend Status: $($backendHealth.status)" -ForegroundColor Green
    Write-Host "✅ Backend Message: $($backendHealth.message)" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Backend health check failed - may need more time to start" -ForegroundColor Yellow
}

Set-Location ".."

# Step 2: Start Frontend Server  
Write-Host ""
Write-Host "🎨 Step 2: Starting Frontend Server..." -ForegroundColor Yellow
Write-Host "Frontend will run on: http://localhost:3000" -ForegroundColor Cyan

Set-Location "frontend"
Start-Process -WindowStyle Normal -FilePath "cmd.exe" -ArgumentList "/k", "npm start"
Set-Location ".."

# Final Instructions
Write-Host ""
Write-Host "🚀 Both servers are starting up!" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔗 Backend:  http://localhost:5001" -ForegroundColor Cyan
Write-Host "🔍 Backend Health: http://localhost:5001/health" -ForegroundColor Gray
Write-Host ""
Write-Host "📋 Current Configuration:" -ForegroundColor Yellow
Write-Host "  ✅ Backend running on port 5001" -ForegroundColor Green
Write-Host "  ✅ Frontend proxy configured for port 5001" -ForegroundColor Green
Write-Host "  ✅ API endpoints updated to match backend routes" -ForegroundColor Green
Write-Host "  ✅ CORS configured for localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "🔧 Available Mock Endpoints:" -ForegroundColor Yellow
Write-Host "  • POST /account/login - User authentication" -ForegroundColor Gray
Write-Host "  • POST /account/register - User registration" -ForegroundColor Gray  
Write-Host "  • POST /locations/search - Location risk search" -ForegroundColor Gray
Write-Host "  • GET /health - Server health check" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️ Note: Backend is running with mock data for testing." -ForegroundColor Yellow
Write-Host "   For full functionality, install complete dependencies." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
