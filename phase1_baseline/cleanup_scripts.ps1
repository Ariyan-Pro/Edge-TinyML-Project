# PHASE 1 SCRIPT CLEANUP SCRIPT
# Generated automatically - review before running!

Write-Host '🧹 PHASE 1 SCRIPT CLEANUP' -ForegroundColor Yellow
Write-Host '=' * 50 -ForegroundColor Cyan

# Files to be removed:
# • validate_paths.py (Keep improved version)
# • scripts\02_model_training\train_baseline.py (Keep fixed version)
# • scripts\03_conversion\convert_tflite.py (Keep convert_to_tflite.py)

Write-Host 'Files to remove: 3' -ForegroundColor Yellow

# Removal commands:
Write-Host 'Removing: validate_paths.py' -ForegroundColor Red
Remove-Item "validate_paths.py" -Force -ErrorAction SilentlyContinue
Write-Host 'Removing: scripts\02_model_training\train_baseline.py' -ForegroundColor Red
Remove-Item "scripts\02_model_training\train_baseline.py" -Force -ErrorAction SilentlyContinue
Write-Host 'Removing: scripts\03_conversion\convert_tflite.py' -ForegroundColor Red
Remove-Item "scripts\03_conversion\convert_tflite.py" -Force -ErrorAction SilentlyContinue

Write-Host '✅ Cleanup completed!' -ForegroundColor Green
Write-Host 'Removed 3 files' -ForegroundColor Green
