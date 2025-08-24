# Start Frontend Server
Write-Host "🚀 Starting Bioscope Frontend Server..." -ForegroundColor Green

# Change to frontend directory
Set-Location "frontend"

# Start the React development server
Write-Host "📦 Starting npm development server on port 3000..." -ForegroundColor Cyan
Start-Process -WindowStyle Normal -FilePath "cmd.exe" -ArgumentList "/k", "npm start"

Write-Host "✅ Frontend server should start on port 3000" -ForegroundColor Green
Write-Host "🌐 Frontend URL: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔗 Backend URL: http://localhost:5001" -ForegroundColor Cyan
Write-Host "⚠️ Make sure backend is running on port 5001" -ForegroundColor Yellow
