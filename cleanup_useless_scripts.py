import os
import glob

def cleanup_useless_scripts():
    print('🧹 EXECUTING SCRIPT CLEANUP PROTOCOL')
    
    # Define patterns for useless scripts (development, backup, temporary files)
    useless_patterns = [
        '**/*_backup.py',
        '**/*_old.py', 
        '**/*_temp.py',
        '**/*_test.py',
        '**/test_*.py',
        '**/backup_*.py',
        '**/temp_*.py',
        '**/*.py.bak',
        '**/*.py.old'
    ]
    
    cleaned_count = 0
    preserved_count = 0
    
    # Scan for useless files
    for pattern in useless_patterns:
        for filepath in glob.glob(pattern, recursive=True):
            # Skip critical production files
            if any(protected in filepath for protected in [
                'automation_core.py', 
                'memory_manager.py',
                'ultimate_strategic_wake_word.py',
                'hybrid_model_router_optimized.py',
                'final_optimized_assistant.py',
                'model_int8.tflite'
            ]):
                preserved_count += 1
                print(f'  🔒 PRESERVED: {filepath}')
                continue
                
            try:
                os.remove(filepath)
                cleaned_count += 1
                print(f'  🗑️ CLEANED: {filepath}')
            except Exception as e:
                print(f'  ⚠️ FAILED: {filepath} - {e}')
    
    print(f'\n📊 CLEANUP SUMMARY:')
    print(f'   Scripts cleaned: {cleaned_count}')
    print(f'   Scripts preserved: {preserved_count}')
    print(f'   Total processed: {cleaned_count + preserved_count}')
    
    return cleaned_count

if __name__ == '__main__':
    cleaned = cleanup_useless_scripts()
    if cleaned > 0:
        print(f'\n✅ CLEANUP COMPLETE: {cleaned} useless scripts removed')
    else:
        print(f'\n✅ SYSTEM ALREADY CLEAN: No useless scripts found')
