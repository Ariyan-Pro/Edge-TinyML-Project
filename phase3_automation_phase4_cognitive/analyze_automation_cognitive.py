# analyze_automation_cognitive.py
import os
import glob
from pathlib import Path

def analyze_automation_cognitive():
    """Analyze the hybrid automation/cognitive phase structure"""
    print("🔍 PHASE 3.75/4 - AUTOMATION & COGNITIVE ANALYSIS")
    print("=" * 70)
    
    # Get all Python files
    python_files = glob.glob("**/*.py", recursive=True)
    python_files = sorted(python_files)
    
    print(f"📁 Found {len(python_files)} Python files:")
    
    # Categorize by current structure and functionality
    categories = {
        "AI Core": [],
        "System Control": [],
        "Voice Interface": [],
        "Utilities": [],
        "Bridge/Connection": [],
        "Configuration": [],
        "Root Scripts": []
    }
    
    for file in python_files:
        file_name = os.path.basename(file)
        size_kb = os.path.getsize(file) / 1024
        dir_name = os.path.dirname(file)
        
        # Categorize based on directory and filename
        if "ai_core" in dir_name:
            categories["AI Core"].append((file, size_kb))
        elif "system_control" in dir_name:
            categories["System Control"].append((file, size_kb))
        elif "voice_interface" in dir_name:
            categories["Voice Interface"].append((file, size_kb))
        elif "utils" in dir_name:
            categories["Utilities"].append((file, size_kb))
        elif "config" in dir_name:
            categories["Configuration"].append((file, size_kb))
        elif "bridge" in file_name.lower() or "gemini" in file_name.lower():
            categories["Bridge/Connection"].append((file, size_kb))
        elif dir_name == "." or "scripts" in dir_name and dir_name.count(os.sep) <= 2:
            categories["Root Scripts"].append((file, size_kb))
        else:
            categories["Utilities"].append((file, size_kb))
    
    # Print analysis
    total_size = 0
    for category, files in categories.items():
        if files:
            category_size = sum(f[1] for f in files)
            total_size += category_size
            print(f"\n📂 {category} ({len(files)} files, {category_size:.1f} KB):")
            for file, size in files:
                print(f"   • {file} ({size:.1f} KB)")
    
    print(f"\n📊 TOTAL: {len(python_files)} files, {total_size:.1f} KB")
    
    print("\n" + "=" * 70)
    print("🎯 CLEANUP & ORGANIZATION RECOMMENDATIONS")
    print("=" * 70)
    
    # Identify cleanup opportunities
    recommendations = []
    
    # Bridge/Connection scripts analysis
    bridge_files = [f[0] for f in categories["Bridge/Connection"]]
    if len(bridge_files) > 3:
        recommendations.append(f"Multiple bridge/connection scripts ({len(bridge_files)}). Consider consolidation.")
    
    # Check for very small/unfinished files
    small_files = []
    for file, size in [(f[0], f[1]) for files in categories.values() for f in files]:
        if size < 0.5:  # Less than 0.5 KB
            small_files.append((file, size))
    
    if small_files:
        recommendations.append(f"Very small/unfinished files found: {len(small_files)}")
        for file, size in small_files:
            recommendations.append(f"  - {file} ({size:.1f} KB)")
    
    # Check for duplicate functionality
    gemini_files = [f for f in python_files if "gemini" in f.lower()]
    if len(gemini_files) > 2:
        recommendations.append(f"Multiple Gemini-related scripts ({len(gemini_files)}). May need consolidation.")
    
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
    """Generate organization plan for this hybrid phase"""
    print("\n" + "=" * 70)
    print("📋 PROPOSED ORGANIZATION PLAN")
    print("=" * 70)
    
    plan = """
## 🎯 PHASE 3.75/4 ORGANIZATION STRATEGY

### CURRENT STRUCTURE (Good foundation):
- ✅ AI Core: LLM interface, memory manager, hybrid assistant
- ✅ System Control: Automation core
- ✅ Voice Interface: Enhanced pipeline, emotional genius mode
- ✅ Utilities: Setup, cleanup, main system
- ⚠️ Bridge/Connection: Multiple Gemini bridge attempts

### PROPOSED CLEANUP:
1. **Consolidate Bridge Scripts**: Keep working versions, remove duplicates
2. **Organize Root Scripts**: Move to appropriate categories
3. **Clean Small Files**: Remove 0-byte or very small unfinished scripts
4. **Update Structure**: Minor refinements to existing good structure

### KEEP (Core Functionality):
- **AI Core**: hybrid_voice_assistant.py, memory_manager.py, working_llm_interface.py
- **System Control**: automation_core.py
- **Voice Interface**: enhanced_voice_pipeline.py, god_mode_emotional_genius.py
- **Utilities**: main.py, perform_cleanup.py, final_system_test.py

### EVALUATE (Potential cleanup):
- Multiple Gemini bridge scripts (consolidate to 1-2 working versions)
- Very small/unfinished files
- Duplicate configuration files

### FINAL ORGANIZED STRUCTURE:
scripts/
├── ai_core/           # LLM, memory, hybrid intelligence
├── automation/        # System control & automation
├── voice/            # Voice interface & processing
├── utils/            # Utilities & system management
├── bridges/          # External service connections
└── config/           # Configuration files
"""
    print(plan)
    
    # Save analysis report
    report_content = "# PHASE 3.75/4 AUTOMATION & COGNITIVE ANALYSIS REPORT\n\n"
    report_content += "## Current Script Inventory:\n"
    
    for category, files in categories.items():
        if files:
            report_content += f"\n### {category}:\n"
            for file, size in files:
                report_content += f"- {file} ({size:.1f} KB)\n"
    
    with open("AUTOMATION_COGNITIVE_ANALYSIS.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"\n📄 Analysis report saved: AUTOMATION_COGNITIVE_ANALYSIS.md")

if __name__ == "__main__":
    analyze_automation_cognitive()