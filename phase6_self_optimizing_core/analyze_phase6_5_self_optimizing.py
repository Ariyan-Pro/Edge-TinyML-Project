# analyze_phase6_5_self_optimizing.py
import os
import glob
from pathlib import Path

def analyze_phase6_5_structure():
    print("🔍 PHASE 6.5 - SELF-OPTIMIZING CORE ANALYSIS")
    print("=" * 70)
    
    python_files = glob.glob("scripts/*.py")
    python_files = sorted(python_files)
    
    print(f"📁 Found {len(python_files)} Python scripts:")
    
    categories = {
        "Core Optimization": [],
        "Scheduling Systems": [],
        "Resource Management": [],
        "Testing & Validation": [],
        "Configuration": []
    }
    
    for file in python_files:
        file_name = os.path.basename(file)
        size_kb = os.path.getsize(file) / 1024
        
        if "scheduler" in file_name.lower():
            categories["Scheduling Systems"].append((file_name, size_kb))
        elif "manager" in file_name.lower() or "monitor" in file_name.lower():
            categories["Resource Management"].append((file_name, size_kb))
        elif "benchmark" in file_name.lower() or "test" in file_name.lower():
            categories["Testing & Validation"].append((file_name, size_kb))
        elif "adaptive" in file_name.lower() or "optimized" in file_name.lower():
            categories["Core Optimization"].append((file_name, size_kb))
        else:
            categories["Configuration"].append((file_name, size_kb))
    
    total_size = 0
    for category, files in categories.items():
        if files:
            category_size = sum(f[1] for f in files)
            total_size += category_size
            print(f"\n📂 {category} ({len(files)} files, {category_size:.1f} KB):")
            for file, size in files:
                print(f"   • {file} ({size:.1f} KB)")
    
    print(f"\n📊 TOTAL: {len(python_files)} scripts, {total_size:.1f} KB")
    
    # Organization recommendations
    print("\n" + "=" * 70)
    print("🎯 ORGANIZATION ACTIONS NEEDED:")
    print("=" * 70)
    print("1. 🗑️  Remove redundant directories: scripts/cache/, scripts/models/")
    print("2. 🧹 Clean cache: scripts/__pycache__/")
    print("3. 📁 Organize into: core/, scheduling/, resources/, testing/, config/")
    print("4. 📋 Consolidate similar scheduler variants if needed")
    
    return categories

if __name__ == "__main__":
    analyze_phase6_5_structure()