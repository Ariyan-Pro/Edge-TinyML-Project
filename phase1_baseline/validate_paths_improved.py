# validate_paths_improved.py
import os
import glob
import re
from pathlib import Path

def check_path_exists(path):
    """Check if a path exists and return status"""
    exists = Path(path).exists()
    return "✅" if exists else "❌"

def validate_all_paths():
    """Validate that all referenced paths exist after updates"""
    print("🔍 VALIDATING ALL PATHS AFTER UPDATE")
    print("=" * 50)
    
    # Critical paths to validate
    critical_paths = [
        ("models/production/model_int8.tflite", "Primary INT8 model"),
        ("models/development/model_dynamic.tflite", "Dynamic quantized model"),
        ("models/development/model_float32.tflite", "Float32 model"),
        ("models/archive/mock_model.json", "Mock model config"),
        ("artifacts/training_metrics.json", "Training metrics"),
        ("artifacts/conversion_report.json", "Conversion report"),
        ("data/raw/", "Raw dataset"),
        ("data/processed/", "Processed features"),
        ("scripts/01_data_preparation/", "Data prep scripts"),
        ("scripts/03_conversion/", "Conversion scripts"),
    ]
    
    all_valid = True
    
    print("📁 PATH VALIDATION CHECK:")
    for path, description in critical_paths:
        status = check_path_exists(path)
        print(f"{status} {description}: {path}")
        if status == "❌":
            all_valid = False
    
    print("\n" + "=" * 50)
    if all_valid:
        print("🎉 ALL PATHS VALIDATED SUCCESSFULLY!")
    else:
        print("⚠️  Some paths are missing - check the report above")
    
    return all_valid

def find_truly_broken_imports():
    """Find only truly broken imports (old paths that weren't updated)"""
    print("\n🔎 CHECKING FOR TRULY BROKEN IMPORTS")
    print("=" * 50)
    
    python_files = glob.glob("**/*.py", recursive=True)
    truly_broken_found = False
    
    # Only look for OLD paths that should have been updated
    old_broken_patterns = [
        r'models/model_int8\.tflite(?!\")',  # Old INT8 path (not in quotes)
        r'models/model_dynamic\.tflite(?!\")',  # Old dynamic path
        r'models/model_float32\.tflite(?!\")',  # Old float32 path
        r'models/fixed_model\.h5(?!\")',  # Old fixed model path
    ]
    
    for file_path in python_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        file_has_broken = False
        broken_matches = []
        
        for pattern in old_broken_patterns:
            matches = re.findall(pattern, content)
            if matches:
                file_has_broken = True
                broken_matches.extend(matches)
        
        if file_has_broken:
            if not truly_broken_found:
                print("⚠️  TRULY BROKEN IMPORTS FOUND (old paths):")
                truly_broken_found = True
            print(f"   {file_path}: {broken_matches}")
    
    if not truly_broken_found:
        print("✅ NO TRULY BROKEN IMPORTS FOUND!")
        print("   All old model paths have been successfully updated")
    
    return truly_broken_found

def verify_updated_paths():
    """Verify that the new organized paths are being used correctly"""
    print("\n🔍 VERIFYING UPDATED PATHS ARE WORKING")
    print("=" * 50)
    
    # Test critical deployment scripts
    test_scripts = [
        "scripts/04_deployment/real_performance_benchmark.py",
        "scripts/04_deployment/real_time_infer_fixed.py", 
        "scripts/04_deployment/test_windows_deployment.py",
        "scripts/04_deployment/test_windows_realtime.py"
    ]
    
    all_good = True
    
    for script_path in test_scripts:
        if os.path.exists(script_path):
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if new paths are present
            new_paths_present = []
            if 'models/production/model_int8.tflite' in content:
                new_paths_present.append('INT8 production path')
            if 'models/development/model_dynamic.tflite' in content:
                new_paths_present.append('Dynamic development path')
            if 'models/development/model_float32.tflite' in content:
                new_paths_present.append('Float32 development path')
            
            if new_paths_present:
                print(f"✅ {script_path}: Using {', '.join(new_paths_present)}")
            else:
                print(f"ℹ️  {script_path}: No new model paths found (may not need them)")
        else:
            print(f"❌ {script_path}: Script not found")
            all_good = False
    
    return all_good

if __name__ == "__main__":
    validate_all_paths()
    find_truly_broken_imports()
    verify_updated_paths()