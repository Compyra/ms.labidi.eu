# Runs the full test suite: Python pipeline tests + browser selftest via headless Edge.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File tests\run-tests.ps1
$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

Write-Host "== python unit tests ==" -ForegroundColor Cyan
# unittest writes verbose progress to stderr; do not let PS treat that as failure
$ErrorActionPreference = "Continue"
& python -m unittest discover -s tests 2>&1 | ForEach-Object { "$_" }
$pyExit = $LASTEXITCODE
$ErrorActionPreference = "Stop"
if ($pyExit -ne 0) { Write-Host "PYTHON TESTS FAILED" -ForegroundColor Red; exit 1 }

Write-Host "== powershell snippet parse gate ==" -ForegroundColor Cyan
& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $root "tools\check_snippets.ps1")
if ($LASTEXITCODE -ne 0) { Write-Host "SNIPPET PARSE GATE FAILED" -ForegroundColor Red; exit 1 }

Write-Host "== browser selftest (headless Edge) ==" -ForegroundColor Cyan
$port = 8907
$server = Start-Process python -ArgumentList "-m", "http.server", "$port", "--bind", "127.0.0.1" `
    -WorkingDirectory $root -PassThru -WindowStyle Hidden
try {
    Start-Sleep -Seconds 2
    $profile = Join-Path $env:TEMP ("mshub-selftest-" + [guid]::NewGuid())
    $dump = Join-Path $env:TEMP "mshub-selftest-dump.html"
    $edge = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
    if (-not (Test-Path $edge)) { $edge = "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe" }
    Start-Process $edge -ArgumentList "--headless=new", "--disable-gpu", "--no-sandbox",
        "--user-data-dir=$profile", "--virtual-time-budget=20000",
        "--dump-dom", "http://127.0.0.1:$port/dev/selftest.html" `
        -RedirectStandardOutput $dump -Wait -WindowStyle Hidden
    $summary = Select-String -Path $dump -Pattern "SELFTEST: [^<]+" |
        ForEach-Object { $_.Matches[0].Value } | Select-Object -First 1
    if (-not $summary) { Write-Host "SELFTEST PRODUCED NO SUMMARY" -ForegroundColor Red; exit 1 }
    if ($summary -match "FAILURES") {
        Write-Host $summary -ForegroundColor Red
        Select-String -Path $dump -Pattern "FAIL  [^<]+" |
            ForEach-Object { $_.Matches[0].Value } | ForEach-Object { Write-Host $_ -ForegroundColor Red }
        exit 1
    }
    Write-Host $summary -ForegroundColor Green
} finally {
    if ($server -and -not $server.HasExited) { Stop-Process -Id $server.Id -Force }
}
exit 0
