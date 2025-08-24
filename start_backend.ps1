# Start Backend Server
Write-Host "🚀 Starting Bioscope Backend Server..." -ForegroundColor Green

# Change to backend directory
Set-Location "backend"

# Start the Python server
Start-Process -WindowStyle Normal -FilePath "venv\Scripts\python.exe" -ArgumentList "minimal_app.py"

Write-Host "✅ Backend server started on port 5001" -ForegroundColor Green
Write-Host "🌐 Health check: http://localhost:5001/health" -ForegroundColor Cyan

# Wait a bit for server to start
Start-Sleep -Seconds 3

# Test the health endpoint
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5001/health" -Method GET
    Write-Host "✅ Backend health check successful:" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json) -ForegroundColor Yellow
} catch {
    Write-Host "⚠️ Backend not responding yet, may need a few more seconds to start" -ForegroundColor Yellow
}
