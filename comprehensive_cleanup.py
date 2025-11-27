import os
import glob
import shutil

def comprehensive_cleanup():
    print('🧹 EXECUTING COMPREHENSIVE CLEANUP PROTOCOL')
    print('TARGET: Remove redundant phase directories and development artifacts')
    
    cleanup_actions = []
    
    # 1. Identify redundant phase directories (keeping only latest)
    phase_dirs = [
        'phase1_baseline',           # Keep - core models
        'phase3_wakeword',           # Redundant? 
        'phase3_automation_phase4_cognitive', # Keep - core logic
        'phase5_autonomous_extensions', # Redundant?
        'phase5_neural_reflex',      # Keep - emotion detection
        'phase6_self_optimizing_core', # Keep - autonomy
        'phase6_edgeos_integration', # Redundant?
        'phase7_autonomy_framework', # Redundant? 
        'phase_9-enhanced_intelligence' # Keep - latest
    ]
    
    # 2. Scan for development artifacts
    dev_artifacts = [
        '**/__pycache__',
        '**/*.pyc',
        '**/*.log',
        '**/test_*.py',
        '**/*_test.py',
        '**/backup_*',
        '**/temp_*',
        '**/*.bak',
        '**/*.old'
    ]
    
    print('\n📋 CLEANUP PLAN:')
    print('Phase directories to evaluate for consolidation...')
    
    cleaned_count = 0
    
    # Clean development artifacts first
    for pattern in dev_artifacts:
        for filepath in glob.glob(pattern, recursive=True):
            try:
                if os.path.isdir(filepath):
                    shutil.rmtree(filepath)
                else:
                    os.remove(filepath)
                cleaned_count += 1
                print(f'  🗑️ CLEANED: {filepath}')
            except Exception as e:
                print(f'  ⚠️ FAILED: {filepath} - {e}')
    
    print(f'\n📊 CLEANUP SUMMARY:')
    print(f'   Development artifacts cleaned: {cleaned_count}')
    print(f'   Phase directory consolidation needed: MANUAL REVIEW REQUIRED')
    
    return cleaned_count

if __name__ == '__main__':
    cleaned = comprehensive_cleanup()
    if cleaned > 0:
        print(f'\n✅ CLEANUP COMPLETE: {cleaned} items removed')
        print('⚠️  Phase directory consolidation requires manual decision')
    else:
        print(f'\n✅ SYSTEM ALREADY CLEAN: No development artifacts found')
        print('⚠️  But phase directory sprawl remains - consider consolidation')
