# Start Development Servers Script
# This script starts both the Python FastAPI server and the Next.js client app

$ErrorActionPreference = "Stop"

# Get the script's directory (project root)
$projectRoot = $PSScriptRoot
if (-not $projectRoot) {
    $projectRoot = Get-Location
}

Write-Host "Starting development servers from: $projectRoot" -ForegroundColor Cyan
Write-Host ""

# Function to check if a command exists
function Test-Command($command) {
    try {
        if (Get-Command $command -ErrorAction SilentlyContinue) {
            return $true
        }
    }
    catch {
        return $false
    }
    return $false
}

# Function to load .env file and return env vars as a hashtable
function Get-EnvVars($envFile) {
    $envVars = @{}
    if (Test-Path $envFile) {
        Get-Content $envFile | ForEach-Object {
            $line = $_.Trim()
            # Skip empty lines and comments
            if ($line -and -not $line.StartsWith('#')) {
                # Parse KEY = "VALUE" or KEY = VALUE format
                if ($line -match '^\s*([^=]+?)\s*=\s*"?([^"]*)"?\s*$') {
                    $key = $matches[1].Trim()
                    $value = $matches[2].Trim()
                    $envVars[$key] = $value
                }
            }
        }
    }
    return $envVars
}

# Check for required tools
if (-not (Test-Command "npm")) {
    Write-Host "ERROR: npm is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Load environment variables from .env file
$envFile = Join-Path $projectRoot ".env"
$envVars = Get-EnvVars $envFile

if ($envVars.Count -gt 0) {
    Write-Host "Loaded $($envVars.Count) environment variables from .env file" -ForegroundColor Green
} else {
    Write-Host "WARNING: No .env file found or it's empty" -ForegroundColor Yellow
}

# Build the environment variable setting commands for the Python script
$envSetCommands = ""
foreach ($key in $envVars.Keys) {
    $value = $envVars[$key]
    $envSetCommands += "`$env:$key = '$value'`n"
}

# Start Python server in a new terminal window
Write-Host "Starting Python FastAPI server on port 8888..." -ForegroundColor Green
$pythonScript = @"
cd '$projectRoot'
$envSetCommands
if (Test-Path '.venv\Scripts\Activate.ps1') {
    & '.venv\Scripts\Activate.ps1'
    Write-Host 'Virtual environment activated' -ForegroundColor Green
} else {
    Write-Host 'WARNING: No virtual environment found, using system Python' -ForegroundColor Yellow
}
Write-Host 'Environment variables loaded from .env' -ForegroundColor Green
Write-Host 'Starting FastAPI server...' -ForegroundColor Cyan
python server.py
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $pythonScript

# Give the Python server a moment to start
Start-Sleep -Seconds 2

# Start Next.js client in a new terminal window
Write-Host "Starting Next.js client on port 3000..." -ForegroundColor Green
$nextScript = @"
cd '$projectRoot\client'
Write-Host 'Installing dependencies if needed...' -ForegroundColor Cyan
npm install
Write-Host 'Starting Next.js development server...' -ForegroundColor Cyan
npm run dev
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $nextScript

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Development servers starting!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Python API:    http://localhost:8888" -ForegroundColor Yellow
Write-Host "API Docs:      http://localhost:8888/docs" -ForegroundColor Yellow
Write-Host "Next.js App:   http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Two new terminal windows have been opened." -ForegroundColor Cyan
Write-Host "Close those windows to stop the servers." -ForegroundColor Cyan
