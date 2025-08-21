# DNS Fix Script for Railway Access
# This script temporarily changes DNS settings to Google DNS

Write-Host "🔧 Fixing DNS for Railway Access..." -ForegroundColor Yellow

# Get active network adapter
$adapter = Get-NetAdapter | Where-Object {$_.Status -eq "Up" -and $_.InterfaceType -eq 6} | Select-Object -First 1

if ($adapter) {
    Write-Host "📡 Found active adapter: $($adapter.Name)" -ForegroundColor Green
    
    # Set DNS to Google DNS temporarily
    Write-Host "🌍 Setting DNS to Google DNS (8.8.8.8, 8.8.4.4)..." -ForegroundColor Yellow
    Set-DnsClientServerAddress -InterfaceIndex $adapter.InterfaceIndex -ServerAddresses "8.8.8.8", "8.8.4.4"
    
    # Flush DNS cache
    Write-Host "🧹 Flushing DNS cache..." -ForegroundColor Yellow
    ipconfig /flushdns | Out-Null
    
    Write-Host "✅ DNS settings updated!" -ForegroundColor Green
    Write-Host "📝 Try accessing your backend now: https://bioscope-project-production.up.railway.app/health" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⚠️ IMPORTANT: Run 'Restore-DNS.ps1' when done to restore original settings" -ForegroundColor Red
} else {
    Write-Host "❌ Could not find active network adapter" -ForegroundColor Red
}
