# Railway Deployment Fix - Commit and Deploy
Write-Host "🚀 Railway Database Connection Fix" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Gray

# Check git status
Write-Host ""
Write-Host "📋 Current Git Status:" -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "📝 Adding changed files..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "💬 Committing changes..." -ForegroundColor Yellow  
git commit -m "Fix Railway database connection - improved SSL handling and direct URL connection"

Write-Host ""
Write-Host "🔄 Pushing to Railway..." -ForegroundColor Yellow
git push

Write-Host ""
Write-Host "✅ Changes pushed to Railway!" -ForegroundColor Green
Write-Host ""
Write-Host "🔍 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Check Railway deployment logs for success" -ForegroundColor White  
Write-Host "2. Test the database connection endpoint:" -ForegroundColor White
Write-Host "   https://bioscope-project-production.up.railway.app/db-status" -ForegroundColor Green
Write-Host ""
Write-Host "3. If still failing, update Railway environment variables:" -ForegroundColor White
Write-Host "   DATABASE_URL=postgresql://postgres.fxxxwgomogyzafrvrjio:rahul2002rahul@aws-0-us-east-2.pooler.supabase.com:6543/postgres?sslmode=require" -ForegroundColor Yellow

Write-Host ""
Write-Host "🎯 Railway Dashboard: https://railway.app/dashboard" -ForegroundColor Blue
