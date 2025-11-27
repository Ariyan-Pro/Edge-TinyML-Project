# analyze_scripts.py
import os
import glob
from pathlib import Path

def analyze_script_directory():
    """Analyze scripts and identify duplicates/unnecessary files"""
    print("🔍 ANALYZING SCRIPTS FOR CLEANUP")
    print("=" * 60)
    
    # Get all Python files
    python_files = glob.glob("**/*.py", recursive=True)
    python_files = sorted(python_files)
    
    print(f"📁 Found {len(python_files)} Python files:")
    for file in python_files:
        size_kb = os.path.getsize(file) / 1024
        print(f"   {file} ({size_kb:.1f} KB)")
    
    print("\n" + "=" * 60)
    print("🎯 CLEANUP RECOMMENDATIONS")
    print("=" * 60)
    
    # Identify potential duplicates/cleanup candidates
    cleanup_candidates = []
    keep_files = []
    
    # Essential files to ALWAYS keep
    essential_files = [
        "validate_phase1.py",
        "update_import_paths.py",
        "validate_paths_improved.py",
        "config.py"
    ]
    
    # Script analysis by directory
    script_categories = {}
    for file in python_files:
        dir_name = os.path.dirname(file)
        if dir_name not in script_categories:
            script_categories[dir_name] = []
        script_categories[dir_name].append(file)
    
    # Analyze each category
    for category, files in script_categories.items():
        print(f"\n📂 {category if category else 'root'}/")
        
        for file in files:
            file_name = os.path.basename(file)
            
            # Check if essential
            if file_name in essential_files or file in essential_files:
                print(f"   ✅ KEEP: {file_name} (essential)")
                keep_files.append(file)
                continue
            
            # Check for duplicates based on name patterns
            is_duplicate = False
            reason = ""
            
            # Duplicate patterns to identify
            duplicate_patterns = [
                ("train_baseline.py", "train_baseline_fixed.py", "Keep fixed version"),
                ("convert_tflite.py", "convert_to_tflite.py", "Keep convert_to_tflite.py"),
                ("validate_paths.py", "validate_paths_improved.py", "Keep improved version"),
            ]
            
            for pattern1, pattern2, advice in duplicate_patterns:
                if pattern1 in file_name or pattern2 in file_name:
                    if pattern2 in file_name:  # Prefer the "improved/fixed" versions
                        keep_files.append(file)
                        print(f"   ✅ KEEP: {file_name} ({advice})")
                    else:
                        cleanup_candidates.append((file, advice))
                        print(f"   🗑️  CLEANUP: {file_name} ({advice})")
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                # Check file size and content to decide
                size_kb = os.path.getsize(file) / 1024
                if size_kb < 1:  # Very small files might be incomplete
                    cleanup_candidates.append((file, "Very small file (<1KB)"))
                    print(f"   🗑️  CLEANUP: {file_name} ({size_kb:.1f} KB - very small)")
                else:
                    keep_files.append(file)
                    print(f"   ✅ KEEP: {file_name} ({size_kb:.1f} KB)")
    
    print("\n" + "=" * 60)
    print("📊 CLEANUP SUMMARY")
    print(f"✅ Files to keep: {len(keep_files)}")
    print(f"🗑️  Files to cleanup: {len(cleanup_candidates)}")
    
    if cleanup_candidates:
        print("\n🗑️  CLEANUP CANDIDATES:")
        for file, reason in cleanup_candidates:
            print(f"   • {file} ({reason})")
    
    # Generate cleanup script
    if cleanup_candidates:
        generate_cleanup_script(cleanup_candidates)
    
    return keep_files, cleanup_candidates

def generate_cleanup_script(cleanup_candidates):
    """Generate a PowerShell script to perform the cleanup"""
    print(f"\n📄 Generating cleanup script...")
    
    script_content = "# PHASE 1 SCRIPT CLEANUP SCRIPT\n"
    script_content += "# Generated automatically - review before running!\n\n"
    
    script_content += "Write-Host '🧹 PHASE 1 SCRIPT CLEANUP' -ForegroundColor Yellow\n"
    script_content += "Write-Host '=' * 50 -ForegroundColor Cyan\n\n"
    
    script_content += "# Files to be removed:\n"
    for file, reason in cleanup_candidates:
        script_content += f"# • {file} ({reason})\n"
    
    script_content += f"\nWrite-Host 'Files to remove: {len(cleanup_candidates)}' -ForegroundColor Yellow\n"
    
    # Add removal commands
    script_content += "\n# Removal commands:\n"
    for file, reason in cleanup_candidates:
        script_content += f"Write-Host 'Removing: {file}' -ForegroundColor Red\n"
        script_content += f"Remove-Item \"{file}\" -Force -ErrorAction SilentlyContinue\n"
    
    script_content += f"\nWrite-Host '✅ Cleanup completed!' -ForegroundColor Green\n"
    script_content += f"Write-Host 'Removed {len(cleanup_candidates)} files' -ForegroundColor Green\n"
    
    with open("cleanup_scripts.ps1", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("📄 Cleanup script generated: cleanup_scripts.ps1")
    print("⚠️  REVIEW THE SCRIPT BEFORE RUNNING!")
    print("   Run: .\cleanup_scripts.ps1")

if __name__ == "__main__":
    keep_files, cleanup_candidates = analyze_script_directory()