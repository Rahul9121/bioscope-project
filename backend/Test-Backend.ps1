# Bioscope Backend Testing Script - PowerShell Version
# Tests all API endpoints and functionality

param(
    [string]$BackendUrl = "https://bioscope-project-production.up.railway.app"
)

# Test results storage
$TestResults = @()
$PassedTests = 0
$FailedTests = 0

# Function to log test results
function Log-Test {
    param(
        [string]$TestName,
        [bool]$Success,
        [string]$Message,
        [object]$Details = $null
    )
    
    $result = @{
        Test = $TestName
        Success = $Success
        Message = $Message
        Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Details = $Details
    }
    
    $script:TestResults += $result
    
    if ($Success) {
        Write-Host "✅ PASS | ${TestName}: $Message" -ForegroundColor Green
        $script:PassedTests++
    } else {
        Write-Host "❌ FAIL | ${TestName}: $Message" -ForegroundColor Red
        $script:FailedTests++
    }
    
    if ($Details) {
        Write-Host "    Details: $($Details | ConvertTo-Json -Compress)" -ForegroundColor Gray
    }
    Write-Host ""
}

# Function to make HTTP requests with error handling
function Invoke-SafeRestMethod {
    param(
        [string]$Uri,
        [string]$Method = "GET",
        [hashtable]$Body = $null,
        [hashtable]$Headers = @{"Content-Type" = "application/json"}
    )
    
    try {
        $params = @{
            Uri = $Uri
            Method = $Method
            Headers = $Headers
            UseBasicParsing = $true
            TimeoutSec = 30
        }
        
        if ($Body -and $Method -in @("POST", "PUT", "PATCH")) {
            $params.Body = ($Body | ConvertTo-Json -Depth 10)
        }
        
        $response = Invoke-RestMethod @params
        return @{ Success = $true; Data = $response; StatusCode = 200 }
    }
    catch {
        $errorMessage = $_.Exception.Message
        $statusCode = if ($_.Exception.Response) { $_.Exception.Response.StatusCode } else { "NetworkError" }
        return @{ Success = $false; Error = $errorMessage; StatusCode = $statusCode }
    }
}

# Test 1: Health Check
function Test-HealthCheck {
    Write-Host "📡 TESTING BASIC CONNECTIVITY" -ForegroundColor Yellow
    Write-Host "------------------------------"
    
    $result = Invoke-SafeRestMethod -Uri "$BackendUrl/health"
    
    if ($result.Success) {
        if ($result.Data.status -eq "healthy") {
            Log-Test "Health Check" $true "Backend is healthy" $result.Data
        } else {
            Log-Test "Health Check" $false "Unexpected health status" $result.Data
        }
    } else {
        Log-Test "Health Check" $false "Request failed: $($result.Error)" @{ StatusCode = $result.StatusCode }
    }
}

# Test 2: Database Status
function Test-DatabaseStatus {
    $result = Invoke-SafeRestMethod -Uri "$BackendUrl/db-status"
    
    if ($result.Success) {
        if ($result.Data.database -eq "connected") {
            Log-Test "Database Status" $true "Database connected successfully" $result.Data
        } else {
            Log-Test "Database Status" $false "Database not connected" $result.Data
        }
    } else {
        Log-Test "Database Status" $false "Request failed: $($result.Error)" @{ StatusCode = $result.StatusCode }
    }
}

# Test 3: User Registration
function Test-UserRegistration {
    Write-Host "🔐 TESTING USER AUTHENTICATION" -ForegroundColor Yellow
    Write-Host "------------------------------"
    
    $randomSuffix = Get-Random -Maximum 100000
    $testUser = @{
        email = "test$randomSuffix@example.com"
        password = "TestPassword123!"
        confirm_password = "TestPassword123!"
        hotel_name = "Test Hotel $randomSuffix"
    }
    
    $script:TestUserEmail = $testUser.email
    $script:TestUserPassword = $testUser.password
    
    $result = Invoke-SafeRestMethod -Uri "$BackendUrl/register" -Method "POST" -Body $testUser
    
    if ($result.Success) {
        if ($result.Data.message -like "*successful*") {
            Log-Test "User Registration" $true "User registered successfully" $result.Data
        } else {
            Log-Test "User Registration" $false "Registration failed" $result.Data
        }
    } else {
        Log-Test "User Registration" $false "Request failed: $($result.Error)" @{ StatusCode = $result.StatusCode }
    }
}

# Test 4: User Login
function Test-UserLogin {
    if (-not $script:TestUserEmail) {
        Log-Test "User Login" $false "Cannot test login - no test user created"
        return
    }
    
    $loginData = @{
        email = $script:TestUserEmail
        password = $script:TestUserPassword
    }
    
    $result = Invoke-SafeRestMethod -Uri "$BackendUrl/login" -Method "POST" -Body $loginData
    
    if ($result.Success) {
        if ($result.Data.message -like "*successful*") {
            Log-Test "User Login" $true "User logged in successfully" $result.Data
        } else {
            Log-Test "User Login" $false "Login failed" $result.Data
        }
    } else {
        Log-Test "User Login" $false "Request failed: $($result.Error)" @{ StatusCode = $result.StatusCode }
    }
}

# Test 5: Search Functionality
function Test-LocationSearch {
    Write-Host "🔍 TESTING SEARCH FUNCTIONALITY" -ForegroundColor Yellow
    Write-Host "------------------------------"
    
    $testLocations = @(
        @{ lat = 40.7128; lng = -74.0060; name = "New York City" },
        @{ lat = 40.3573; lng = -74.6672; name = "Princeton, NJ" },
        @{ lat = 39.3643; lng = -74.4229; name = "Atlantic City, NJ" }
    )
    
    foreach ($location in $testLocations) {
        $searchData = @{
            latitude = $location.lat
            longitude = $location.lng
            radius = 50
        }
        
        $result = Invoke-SafeRestMethod -Uri "$BackendUrl/search" -Method "POST" -Body $searchData
        
        if ($result.Success) {
            if ($result.Data.success) {
                $risks = $result.Data.risks
                $speciesCount = if ($result.Data.species) { $result.Data.species.Count } else { 0 }
                Log-Test "Search $($location.name)" $true "Found $speciesCount species, Risk levels: $($risks | ConvertTo-Json -Compress)" @{ species_count = $speciesCount; risks = $risks }
            } else {
                Log-Test "Search $($location.name)" $false "Search failed" $result.Data
            }
        } else {
            Log-Test "Search $($location.name)" $false "Request failed: $($result.Error)" @{ StatusCode = $result.StatusCode }
        }
        
        Start-Sleep -Seconds 1  # Rate limiting
    }
}

# Test 6: Address Autocomplete
function Test-AddressAutocomplete {
    $testQueries = @("New York", "Princeton, NJ", "Newark", "Atlantic City")
    
    foreach ($query in $testQueries) {
        $result = Invoke-SafeRestMethod -Uri "$BackendUrl/autocomplete?q=$([uri]::EscapeDataString($query))"
        
        if ($result.Success) {
            if ($result.Data -is [array] -and $result.Data.Count -gt 0) {
                Log-Test "Autocomplete '$query'" $true "Found $($result.Data.Count) suggestions" ($result.Data | Select-Object -First 2)
            } else {
                Log-Test "Autocomplete '$query'" $false "No suggestions found" $result.Data
            }
        } else {
            Log-Test "Autocomplete '$query'" $false "Request failed: $($result.Error)" @{ StatusCode = $result.StatusCode }
        }
        
        Start-Sleep -Milliseconds 500  # Rate limiting
    }
}

# Test 7: Report Generation
function Test-ReportGeneration {
    Write-Host "📊 TESTING REPORT GENERATION" -ForegroundColor Yellow
    Write-Host "------------------------------"
    
    $reportData = @{
        location = "Princeton, NJ"
        latitude = 40.3573
        longitude = -74.6672
        risks = @{
            invasive_species = "Medium"
            freshwater = "Low"
            marine = "Low"
            terrestrial = "Medium"
            iucn_species = "High"
        }
        species = @(
            @{ common_name = "Norway Maple"; scientific_name = "Acer platanoides"; threat_level = "Medium" },
            @{ common_name = "House Sparrow"; scientific_name = "Passer domesticus"; threat_level = "Low" }
        )
    }
    
    try {
        $response = Invoke-WebRequest -Uri "$BackendUrl/generate-report" -Method POST -Body ($reportData | ConvertTo-Json -Depth 10) -ContentType "application/json" -UseBasicParsing -TimeoutSec 30
        
        if ($response.StatusCode -eq 200) {
            $contentType = $response.Headers["Content-Type"]
            if ($contentType -like "*application/pdf*") {
                $pdfSize = $response.Content.Length
                Log-Test "Report Generation" $true "PDF generated successfully ($pdfSize bytes)"
            } else {
                # Try to parse as JSON
                try {
                    $data = $response.Content | ConvertFrom-Json
                    if ($data.success) {
                        Log-Test "Report Generation" $true "Report generated" $data
                    } else {
                        Log-Test "Report Generation" $false "Report generation failed" $data
                    }
                } catch {
                    Log-Test "Report Generation" $false "Unexpected response format" @{ ContentType = $contentType }
                }
            }
        } else {
            Log-Test "Report Generation" $false "HTTP $($response.StatusCode)" $response.Content
        }
    } catch {
        Log-Test "Report Generation" $false "Request failed: $($_.Exception.Message)" @{ Error = $_.Exception.Message }
    }
}

# Main execution
function Start-BackendTests {
    Write-Host "🚀 Starting Comprehensive Backend Testing..." -ForegroundColor Cyan
    Write-Host "Backend URL: $BackendUrl"
    Write-Host "============================================================"
    Write-Host ""
    
    # Initialize counters
    $script:PassedTests = 0
    $script:FailedTests = 0
    $script:TestResults = @()
    
    # Run tests
    Test-HealthCheck
    Test-DatabaseStatus
    Test-UserRegistration  
    Test-UserLogin
    Test-AddressAutocomplete
    Test-LocationSearch
    Test-ReportGeneration
    
    # Print Summary
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "📋 TEST SUMMARY" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    
    $totalTests = $PassedTests + $FailedTests
    $successRate = if ($totalTests -gt 0) { ($PassedTests / $totalTests) * 100 } else { 0 }
    
    Write-Host "Total Tests: $totalTests"
    Write-Host "Passed: $PassedTests ✅" -ForegroundColor Green
    Write-Host "Failed: $FailedTests ❌" -ForegroundColor Red
    Write-Host "Success Rate: $($successRate.ToString('F1'))%"
    Write-Host ""
    
    if ($FailedTests -gt 0) {
        Write-Host "❌ FAILED TESTS:" -ForegroundColor Red
        Write-Host "--------------------"
        $TestResults | Where-Object { -not $_.Success } | ForEach-Object {
            Write-Host "  • $($_.Test): $($_.Message)" -ForegroundColor Red
        }
        Write-Host ""
    }
    
    Write-Host "✅ PASSED TESTS:" -ForegroundColor Green
    Write-Host "--------------------"
    $TestResults | Where-Object { $_.Success } | ForEach-Object {
        Write-Host "  • $($_.Test): $($_.Message)" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "🎉 Testing Complete!" -ForegroundColor Cyan
    
    # Save results to file
    $TestResults | ConvertTo-Json -Depth 10 | Out-File "backend_test_results.json" -Encoding UTF8
    Write-Host "📁 Detailed results saved to: backend_test_results.json"
}

# Run the tests
Start-BackendTests
