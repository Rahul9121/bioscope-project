# DNS Restore Script
# This script restores original DNS settings

Write-Host "🔄 Restoring original DNS settings..." -ForegroundColor Yellow

# Get active network adapter
$adapter = Get-NetAdapter | Where-Object {$_.Status -eq "Up" -and $_.InterfaceType -eq 6} | Select-Object -First 1

if ($adapter) {
    Write-Host "📡 Found active adapter: $($adapter.Name)" -ForegroundColor Green
    
    # Restore to automatic DNS (DHCP)
    Write-Host "🔄 Restoring to automatic DNS..." -ForegroundColor Yellow
    Set-DnsClientServerAddress -InterfaceIndex $adapter.InterfaceIndex -ResetServerAddresses
    
    # Flush DNS cache
    Write-Host "🧹 Flushing DNS cache..." -ForegroundColor Yellow
    ipconfig /flushdns | Out-Null
    
    Write-Host "✅ DNS settings restored!" -ForegroundColor Green
} else {
    Write-Host "❌ Could not find active network adapter" -ForegroundColor Red
}
