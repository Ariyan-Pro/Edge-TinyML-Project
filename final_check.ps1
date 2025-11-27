Write-Host "=== EDGE-TINYML PRODUCTION READINESS CHECK ===" -ForegroundColor Cyan

 = @(
    "scripts/production_logger.py",
    "scripts/metrics_exporter.py", 
    ".github/workflows/ci.yml",
    "scripts/create_release.sh",
    "deployment/edgetinyml.service",
    "scripts/backup_db.ps1",
    "tests/perf/windows_optimized_bench.py"
)

 = True
foreach ( in ) {
    if (Test-Path ) {
        Write-Host "  ✅ " -ForegroundColor Green
    } else {
        Write-Host "  ❌ " -ForegroundColor Red
         = False
    }
}

if () {
    Write-Host "
🎯 ALL SYSTEMS READY FOR PRODUCTION!" -ForegroundColor Green
} else {
    Write-Host "
⚠️  Some files missing" -ForegroundColor Yellow
}

Write-Host "
=== CHECK COMPLETE ===" -ForegroundColor Cyan
