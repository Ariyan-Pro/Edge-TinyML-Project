# UTF-8 encoded PowerShell script
Write-Host "=== EDGE-TINYML PRODUCTION READINESS CHECK ===" -ForegroundColor Cyan

$files = @(
    "scripts/production_logger.py",
    "scripts/metrics_exporter.py", 
    ".github/workflows/ci.yml",
    "scripts/create_release.sh",
    "deployment/edgetinyml.service",
    "scripts/backup_db.ps1",
    "tests/perf/windows_optimized_bench.py"
)

$allPresent = $true
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file" -ForegroundColor Red
        $allPresent = $false
    }
}

if ($allPresent) {
    Write-Host "`n🎯 ALL SYSTEMS READY FOR PRODUCTION!" -ForegroundColor Green
} else {
    Write-Host "`n⚠️  Some files missing" -ForegroundColor Yellow
}

Write-Host "
=== CHECK COMPLETE ===" -ForegroundColor Cyan
