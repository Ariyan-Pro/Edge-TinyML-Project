# analyze_phase5_neural_reflex.py
import os
import glob
from pathlib import Path

def analyze_phase5_structure():
    """Analyze Phase 5 Neural Reflex structure"""
    print("🔍 PHASE 5 - NEURAL REFLEX ANALYSIS")
    print("=" * 70)
    
    # Get all Python files
    python_files = glob.glob("**/*.py", recursive=True)
    python_files = sorted(python_files)
    
    print(f"📁 Found {len(python_files)} Python files:")
    
    # Categorize by functionality
    categories = {
        "Core Emotion Detection": [],
        "Training & Models": [],
        "Testing & Validation": [],
        "Dataset Processing": [],
        "Integration & Reflex": [],
        "Root Verification": []
    }
    
    for file in python_files:
        file_name = os.path.basename(file)
        size_kb = os.path.getsize(file) / 1024
        
        # Categorize based on filename patterns
        if "emotion" in file_name.lower() and "detector" in file_name.lower():
            categories["Core Emotion Detection"].append((file, size_kb))
        elif "train" in file_name.lower() or "model" in file_name.lower():
            categories["Training & Models"].append((file, size_kb))
        elif "test" in file_name.lower() or "valid" in file_name.lower():
            categories["Testing & Validation"].append((file, size_kb))
        elif "dataset" in file_name.lower() or "data" in file_name.lower():
            categories["Dataset Processing"].append((file, size_kb))
        elif "integrated" in file_name.lower() or "reflex" in file_name.lower():
            categories["Integration & Reflex"].append((file, size_kb))
        elif "verify" in file_name.lower() or "complete" in file_name.lower():
            categories["Root Verification"].append((file, size_kb))
        else:
            categories["Testing & Validation"].append((file, size_kb))  # Default
    
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
    print("🎯 ORGANIZATION RECOMMENDATIONS")
    print("=" * 70)
    
    # Identify cleanup opportunities
    recommendations = []
    
    # Testing scripts analysis
    test_files = [f[0] for f in categories["Testing & Validation"]]
    if len(test_files) > 5:
        recommendations.append(f"Multiple testing scripts ({len(test_files)}). May have duplicates.")
    
    # Check for very small files
    small_files = []
    for file, size in [(f[0], f[1]) for files in categories.values() for f in files]:
        if size < 1.0:  # Less than 1 KB
            small_files.append((file, size))
    
    if small_files:
        recommendations.append(f"Very small files found: {len(small_files)}")
        for file, size in small_files:
            recommendations.append(f"  - {file} ({size:.1f} KB)")
    
    # Check for similar functionality
    simple_test_files = [f for f in python_files if "simple" in f.lower() and "test" in f.lower()]
    if len(simple_test_files) > 2:
        recommendations.append(f"Multiple 'simple test' scripts ({len(simple_test_files)}). Consider consolidation.")
    
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
    """Generate organization plan for Phase 5"""
    print("\n" + "=" * 70)
    print("📋 PROPOSED ORGANIZATION PLAN")
    print("=" * 70)
    
    plan = """
## 🎯 PHASE 5 NEURAL REFLEX ORGANIZATION STRATEGY

### CURRENT STRUCTURE ANALYSIS:
- ✅ Core emotion detection systems
- ✅ Training pipelines for emotion models
- ✅ Extensive testing and validation suite
- ✅ Dataset processing utilities
- ✅ Integration and reflex systems
- ⚠️ Multiple similar test scripts

### PROPOSED ORGANIZATION:
1. **Consolidate Testing**: Keep most comprehensive test scripts
2. **Organize by Function**: Clear separation of core vs test code
3. **Clean Small Files**: Evaluate very small scripts
4. **Create Logical Structure**: Core, training, testing, integration

### KEEP (Core Functionality):
- **Emotion Detection**: emotion_detector.py, emotion_detector_production.py
- **Training**: train_ravdess_model.py, train_memory_optimized.py
- **Integration**: integrated_reflex_loop.py
- **Dataset**: dataset_processor.py
- **Verification**: Root verification scripts

### EVALUATE (Potential consolidation):
- Multiple simple test variations
- Very small utility scripts
- Similar validation scripts

### FINAL ORGANIZED STRUCTURE:
scripts/
├── core/              # Core emotion detection
├── training/          # Model training pipelines
├── integration/       # Reflex systems & integration
├── datasets/          # Data processing
├── testing/           # Comprehensive test suite
└── utils/             # Utilities & helpers
"""
    print(plan)
    
    # Save analysis report
    report_content = "# PHASE 5 NEURAL REFLEX ANALYSIS REPORT\n\n"
    report_content += "## Current Script Inventory:\n"
    
    for category, files in categories.items():
        if files:
            report_content += f"\n### {category}:\n"
            for file, size in files:
                report_content += f"- {file} ({size:.1f} KB)\n"
    
    with open("PHASE5_ANALYSIS_REPORT.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"\n📄 Analysis report saved: PHASE5_ANALYSIS_REPORT.md")

if __name__ == "__main__":
    analyze_phase5_structure()