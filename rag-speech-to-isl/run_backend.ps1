# Run ISL Avatar Studio Backend & Web Application
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Starting ISL Avatar Studio on http://127.0.0.1:8000 ..." -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$scriptDir\backend"
$env:PYTHONPATH = "$scriptDir\backend"

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
