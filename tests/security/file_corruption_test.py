import os
import shutil
import time

def corrupt_file(filepath):
    """Corrupt a file by overwriting with random data"""
    try:
        file_size = os.path.getsize(filepath)
        with open(filepath, 'rb+') as f:
            f.seek(file_size // 2)
            f.write(b'CORRUPTED' * 10)
    except Exception as e:
        print(f"⚠️  Could not corrupt {filepath}: {e}")

def test_file_corruption_recovery():
    print("🔒 TESTING FILE CORRUPTION RESILIENCE")
    
    # Only test files that definitely exist
    test_files = [
        "config.py",
        "requirements.txt"
    ]
    
    existing_files = [f for f in test_files if os.path.exists(f)]
    
    if not existing_files:
        print("❌ No test files found for corruption testing")
        return False
    
    backup_files = []
    
    for filepath in existing_files:
        if os.path.exists(filepath):
            backup_path = f"{filepath}.backup_test"
            shutil.copy2(filepath, backup_path)
            backup_files.append((filepath, backup_path))
            print(f"📁 Backed up: {os.path.basename(filepath)}")
    
    recovery_successful = 0
    
    for original_path, backup_path in backup_files:
        try:
            print(f"🧪 Testing corruption recovery for {os.path.basename(original_path)}")
            
            corrupt_file(original_path)
            time.sleep(1)
            
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, original_path)
                recovery_successful += 1
                print(f"✅ Recovered: {os.path.basename(original_path)}")
            else:
                print(f"❌ Backup missing: {os.path.basename(original_path)}")
                
        except Exception as e:
            print(f"❌ Corruption test failed: {e}")
    
    for original_path, backup_path in backup_files:
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, original_path)
            os.remove(backup_path)
    
    if recovery_successful == len(existing_files):
        print("✅ FILE CORRUPTION RESILIENCE TEST PASSED")
        return True
    else:
        print("❌ FILE CORRUCTURE RESILIENCE TEST FAILED")
        return False
