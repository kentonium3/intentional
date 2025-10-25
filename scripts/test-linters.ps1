# PowerShell script to compare Obsidian Linter and markdownlint-cli2 outputs
# Usage: .\scripts\test-linters.ps1 [file_or_directory]

param(
    [string]$Target = "docs"
)

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$ReportDir = "linter-reports"

# Create report directory
New-Item -ItemType Directory -Force -Path $ReportDir | Out-Null

Write-Host "========================================"
Write-Host "Linter Comparison Test"
Write-Host "========================================"
Write-Host "Target: $Target"
Write-Host "Timestamp: $Timestamp"
Write-Host ""

# Run markdownlint-cli2
Write-Host "Running markdownlint-cli2..."
$ReportFile = "$ReportDir\markdownlint-$Timestamp.txt"
npx markdownlint-cli2 "$Target/**/*.md" 2>&1 | Out-File -FilePath $ReportFile

# Count errors
Write-Host ""
Write-Host "========================================"
Write-Host "markdownlint-cli2 Summary"
Write-Host "========================================"

$Content = Get-Content $ReportFile -Raw
$ErrorLines = $Content -split "`n" | Where-Object { $_ -match "MD\d+" }
$TotalErrors = $ErrorLines.Count

Write-Host "Total errors: $TotalErrors"
Write-Host ""

# Top violations
Write-Host "Top 10 violations:"
$ErrorLines | ForEach-Object {
    if ($_ -match '(MD\d+/[a-z-]+)') {
        $matches[1]
    }
} | Group-Object | Sort-Object Count -Descending | Select-Object -First 10 | Format-Table Count, Name -AutoSize

# Files with most errors
Write-Host "Files with most errors:"
$ErrorLines | ForEach-Object {
    if ($_ -match '(docs/[^:]+)') {
        $matches[1]
    }
} | Group-Object | Sort-Object Count -Descending | Select-Object -First 10 | Format-Table Count, Name -AutoSize

Write-Host "========================================"
Write-Host "Obsidian Linter Status"
Write-Host "========================================"

$LinterConfig = Get-Content "docs\.obsidian\plugins\obsidian-linter\data.json" -Raw | ConvertFrom-Json
$EnabledCount = ($LinterConfig.ruleConfigs.PSObject.Properties | Where-Object { $_.Value.enabled -eq $true }).Count

Write-Host "Total enabled rules: $EnabledCount"
Write-Host ""

Write-Host "Phase 1 critical rules:"
Write-Host "  - heading-blank-lines: $($LinterConfig.ruleConfigs.'heading-blank-lines'.enabled)"
Write-Host "  - trailing-spaces: $($LinterConfig.ruleConfigs.'trailing-spaces'.enabled)"
Write-Host "  - consecutive-blank-lines: $($LinterConfig.ruleConfigs.'consecutive-blank-lines'.enabled)"
Write-Host "  - empty-line-around-code-fences: $($LinterConfig.ruleConfigs.'empty-line-around-code-fences'.enabled)"
Write-Host "  - empty-line-around-tables: $($LinterConfig.ruleConfigs.'empty-line-around-tables'.enabled)"
Write-Host "  - empty-line-around-blockquotes: $($LinterConfig.ruleConfigs.'empty-line-around-blockquotes'.enabled)"
Write-Host "  - unordered-list-style: $($LinterConfig.ruleConfigs.'unordered-list-style'.enabled)"
Write-Host "  - line-break-at-document-end: $($LinterConfig.ruleConfigs.'line-break-at-document-end'.enabled)"
Write-Host "  - remove-trailing-punctuation-in-heading: $($LinterConfig.ruleConfigs.'remove-trailing-punctuation-in-heading'.enabled)"
Write-Host ""

Write-Host "========================================"
Write-Host "Reports saved to:"
Write-Host "  $ReportFile"
Write-Host "========================================"
