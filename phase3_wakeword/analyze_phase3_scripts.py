# analyze_phase3_scripts.py
import os
import glob
from pathlib import Path

def analyze_phase3_structure():
    """Analyze Phase 3 structure and identify organization opportunities"""
    print("🔍 PHASE 3 STRUCTURE ANALYSIS")
    print("=" * 60)
    
    # Get all Python files
    python_files = glob.glob("**/*.py", recursive=True)
    python_files = sorted(python_files)
    
    print(f"📁 Found {len(python_files)} Python files:")
    
    # Categorize scripts by functionality
    categories = {
        "GUI": [],
        "Wake Word": [],
        "Assistant": [], 
        "Testing": [],
        "Launch/Utility": []
    }
    
    # Pattern matching for categorization
    for file in python_files:
        file_name = os.path.basename(file)
        size_kb = os.path.getsize(file) / 1024
        
        if "gui" in file_name.lower():
            categories["GUI"].append((file, size_kb))
        elif "wake" in file_name.lower() or "strategic" in file_name.lower():
            categories["Wake Word"].append((file, size_kb))
        elif "assistant" in file_name.lower() or "command" in file_name.lower():
            categories["Assistant"].append((file, size_kb))
        elif "test" in file_name.lower() or "debug" in file_name.lower():
            categories["Testing"].append((file, size_kb))
        else:
            categories["Launch/Utility"].append((file, size_kb))
    
    # Print categorized analysis
    for category, files in categories.items():
        print(f"\n📂 {category} ({len(files)} files):")
        for file, size in files:
            print(f"   • {file} ({size:.1f} KB)")
    
    print("\n" + "=" * 60)
    print("🎯 ORGANIZATION RECOMMENDATIONS")
    print("=" * 60)
    
    # Identify duplicates and recommendations
    recommendations = []
    
    # GUI scripts analysis
    gui_files = [f[0] for f in categories["GUI"]]
    if len(gui_files) > 1:
        recommendations.append(f"Multiple GUI scripts found: {len(gui_files)}. Consider consolidation.")
    
    # Wake word scripts analysis  
    wake_files = [f[0] for f in categories["Wake Word"]]
    if len(wake_files) > 1:
        recommendations.append(f"Multiple wake word scripts: {len(wake_files)}. 'ultimate_strategic_wake_word.py' likely the main one.")
    
    # Assistant scripts analysis
    assistant_files = [f[0] for f in categories["Assistant"]]
    if len(assistant_files) > 1:
        recommendations.append(f"Multiple assistant scripts: {len(assistant_files)}. May have overlapping functionality.")
    
    # Print recommendations
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
    else:
        print("✅ Structure looks good! Minimal cleanup needed.")
    
    # Generate organization plan
    generate_organization_plan(categories)
    
    return categories

def generate_organization_plan(categories):
    """Generate a detailed organization plan"""
    print("\n" + "=" * 60)
    print("📋 PROPOSED ORGANIZATION PLAN")
    print("=" * 60)
    
    plan = """
## 🎯 PHASE 3 ORGANIZATION STRATEGY

### KEEP (Core Functionality):
- **Primary Wake Word**: ultimate_strategic_wake_word.py
- **Primary GUI**: final_strategic_gui.py  
- **Command Listener**: command_listener.py
- **Essential Utilities**: phase3_launcher.py, stream_fixed_launcher.py

### CONSOLIDATE (Duplicates):
- GUI scripts: Keep final_strategic_gui.py as primary
- Assistant scripts: Evaluate which has most complete functionality
- Wake word scripts: ultimate_strategic_wake_word.py appears to be the main

### ORGANIZE STRUCTURE:
scripts/
├── core/           # Primary functionality
├── gui/           # GUI applications  
├── utilities/     # Launch and helper scripts
└── testing/       # Debug and test scripts

### NEXT STEPS:
1. Run detailed script analysis to identify true duplicates
2. Create organized directory structure
3. Move scripts to appropriate categories
4. Update any import paths if needed
5. Remove truly redundant scripts
"""
    print(plan)
    
    # Save analysis report
    report_content = "# PHASE 3 SCRIPT ANALYSIS REPORT\n\n"
    report_content += "## Current Script Inventory:\n"
    
    for category, files in categories.items():
        report_content += f"\n### {category}:\n"
        for file, size in files:
            report_content += f"- {file} ({size:.1f} KB)\n"
    
    with open("PHASE3_ANALYSIS_REPORT.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"\n📄 Analysis report saved: PHASE3_ANALYSIS_REPORT.md")

if __name__ == "__main__":
    analyze_phase3_structure()