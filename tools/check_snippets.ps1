# Parses every shipped PowerShell snippet with the PowerShell language parser.
# Offline syntax gate: no tenant, no execution, just "does this parse".
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File tools\check_snippets.ps1
$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$dataFile = Join-Path $root "data\data-ps.js"
if (-not (Test-Path $dataFile)) { Write-Host "no data-ps.js; nothing to check"; exit 0 }

$text = Get-Content $dataFile -Raw
$json = $text.Substring($text.IndexOf('=[') + 1)
$json = $json.Substring(0, $json.LastIndexOf(']') + 1)
$snippets = $json | ConvertFrom-Json

$failed = 0
foreach ($s in $snippets) {
    $errors = $null
    $null = [System.Management.Automation.Language.Parser]::ParseInput($s.code, [ref]$null, [ref]$errors)
    if ($errors -and $errors.Count -gt 0) {
        $failed++
        Write-Host ("PARSE FAIL {0}: {1}" -f $s.id, $errors[0].Message) -ForegroundColor Red
        continue
    }
    # A snippet that parses but references an unknown verb-noun is still suspect.
    if ($s.code -notmatch '^[A-Za-z][\w\.\\-]*(\s|$)') {
        $failed++
        Write-Host ("SUSPECT START {0}: {1}" -f $s.id, $s.code.Substring(0, 40)) -ForegroundColor Red
    }
}
if ($failed -gt 0) {
    Write-Host ("PowerShell snippet check: {0} FAILURES of {1}" -f $failed, $snippets.Count) -ForegroundColor Red
    exit 1
}
Write-Host ("PowerShell snippet check: all {0} snippets parse" -f $snippets.Count) -ForegroundColor Green
exit 0
