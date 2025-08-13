# PowerShell script to verify environment variables

Write-Host "🔍 Environment Variable Verification" -ForegroundColor Green
Write-Host "=" * 50

# Read .env file
$envFile = ".\.env"

if (Test-Path $envFile) {
    Write-Host "✅ .env file found" -ForegroundColor Green
    Write-Host "`nEnvironment Variables:" -ForegroundColor Yellow
    
    Get-Content $envFile | ForEach-Object {
        if ($_ -match "^([^#].*)=(.*)`$") {
            $key = $matches[1]
            $value = $matches[2]
            
            # Mask sensitive information
            if ($key -like "*PASSWORD*" -or $key -like "*SECRET*" -or $key -like "*KEY*") {
                $maskedValue = $value.Substring(0, [Math]::Min(5, $value.Length)) + "*****"
                Write-Host "  $key = $maskedValue" -ForegroundColor Cyan
            } else {
                Write-Host "  $key = $value" -ForegroundColor Cyan
            }
        }
    }
} else {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "Please make sure you have a .env file in the current directory" -ForegroundColor Yellow
}

Write-Host "`nChecking database URL format..." -ForegroundColor Yellow

# Check if DATABASE_URL exists and has the right format
$databaseUrl = Select-String -Path $envFile -Pattern "DATABASE_URL=" | ForEach-Object { $_.Line }
if ($databaseUrl) {
    if ($databaseUrl -like "*postgresql://*") {
        Write-Host "✅ DATABASE_URL appears to be a valid PostgreSQL connection string" -ForegroundColor Green
    } else {
        Write-Host "❌ DATABASE_URL does not appear to be a valid PostgreSQL connection string" -ForegroundColor Red
    }
    
    if ($databaseUrl -like "*your-password*" -or $databaseUrl -like "*[YOUR-*") {
        Write-Host "❌ DATABASE_URL contains placeholder values - please update with real credentials" -ForegroundColor Red
    }
} else {
    Write-Host "❌ DATABASE_URL not found in .env file" -ForegroundColor Red
}

Write-Host "`nVerification completed!" -ForegroundColor Green
