# update_import_paths.py
import os
import re
from pathlib import Path
import glob
import datetime

def update_model_paths_in_file(file_path):
    """Update model paths in a single file"""
    print(f"🔧 Processing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Track changes
    changes_made = []
    
    # OLD PATTERNS -> NEW PATTERNS
    path_replacements = {
        # Old direct paths -> New organized paths
        r'models/model_int8\.tflite': 'models/production/model_int8.tflite',
        r'models/model_dynamic\.tflite': 'models/development/model_dynamic.tflite', 
        r'models/model_float32\.tflite': 'models/development/model_float32.tflite',
        r'models/fixed_model\.h5': 'models/archive/fixed_model.h5',
        
        # Relative path fixes
        r'\./models/production/model_int8': './models/production/model_int8',
        r'\./models/development/model_dynamic': './models/development/model_dynamic',
        r'\./models/development/model_float32': './models/development/model_float32',
        
        # Config file references
        r'artifacts/conversion_report\.json': 'artifacts/conversion_report.json',
        r'artifacts/training_metrics\.json': 'artifacts/training_metrics.json',
    }
    
    new_content = content
    for old_pattern, new_pattern in path_replacements.items():
        if re.search(old_pattern, new_content):
            new_content = re.sub(old_pattern, new_pattern, new_content)
            changes_made.append(f"  {old_pattern} → {new_pattern}")
    
    # Write back if changes were made
    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Updated {len(changes_made)} paths:")
        for change in changes_made:
            print(change)
    else:
        print("ℹ️  No path updates needed")
    
    return len(changes_made)

def update_all_scripts():
    """Update paths in all Python scripts in the project"""
    print("🚀 UPDATING IMPORT PATHS FOR NEW DIRECTORY STRUCTURE")
    print("=" * 60)
    
    # Find all Python scripts
    python_files = []
    search_patterns = [
        "*.py",
        "scripts/**/*.py", 
        "**/*.py"
    ]
    
    for pattern in search_patterns:
        python_files.extend(glob.glob(pattern, recursive=True))
    
    # Remove duplicates and sort
    python_files = sorted(list(set(python_files)))
    
    print(f"📁 Found {len(python_files)} Python files to check")
    print()
    
    total_changes = 0
    updated_files = []
    
    for file_path in python_files:
        if os.path.isfile(file_path):
            changes = update_model_paths_in_file(file_path)
            if changes > 0:
                total_changes += changes
                updated_files.append(file_path)
            print()
    
    # Summary report
    print("=" * 60)
    print("📊 UPDATE SUMMARY")
    print(f"✅ Files updated: {len(updated_files)}")
    print(f"✅ Total path changes: {total_changes}")
    
    if updated_files:
        print("\n📝 Updated files:")
        for file in updated_files:
            print(f"  • {file}")
    
    # Create update report
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_content = f"""# IMPORT PATH UPDATE REPORT

## Update performed on: {current_time}

## Changes Made:
- Updated model paths to reflect new organized directory structure
- Fixed {total_changes} path references across {len(updated_files)} files

## New Path Structure:
- Primary models: `models/production/model_int8.tflite`
- Development models: `models/development/model_*.tflite`  
- Archive models: `models/archive/`

## Files Updated:
{chr(10).join(f"- {file}" for file in updated_files)}

## Status: ✅ COMPLETE
All import paths updated to match new organized structure.
"""
    
    with open("PATH_UPDATE_REPORT.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"\n📄 Update report saved: PATH_UPDATE_REPORT.md")
    print("🎉 IMPORT PATH UPDATE COMPLETED!")

if __name__ == "__main__":
    update_all_scripts()