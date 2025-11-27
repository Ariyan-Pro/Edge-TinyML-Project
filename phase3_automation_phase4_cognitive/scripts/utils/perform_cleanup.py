# scripts/perform_cleanup.py
import os
import shutil

def perform_cleanup():
    """Remove redundant files and organize the codebase"""
    
    # Files to KEEP (core operational files)
    keep_files = {
        'automation_core.py',          # Original proven automation
        'working_llm_interface.py',    # PROVEN WORKING GGUF interface  
        'final_voice_integration.py',  # TESTED Phase 3→4 bridge
        'gui_integration.py',          # Main GUI
        'memory_manager.py',           # SQLite memory system
        'test_commands.py',            # Debug utility
        'voice_bridge.py',             # Phase bridge
        'phase4_final_demo.py',        # Demo script
        'rag_indexer.py',              # Future RAG capability
        '00_setup.sh',                 # Setup script
        
        # New organized files
        'automation_engine.py',
        'cognitive_engine.py', 
        'main.py'
    }
    
    # Files to REMOVE (redundant/consolidated)
    remove_files = {
        'cognitive_layer.py',          # Consolidated into cognitive_engine
        'simple_cognitive.py',         # Redundant with working_llm_interface
        'llm_interface.py',            # Broken version
        'optimized_llm_interface.py',  # Alternative (keep for now)
        'ultimate_assistant.py',       # Consolidated into main.py
        'final_cognitive_test.py',     # Test file (keep for now)
        '03_gui_integration.py'        # Duplicate GUI file
    }
    
    current_dir = os.path.dirname(__file__)
    removed_count = 0
    kept_count = 0
    
    print("🧹 PERFORMING STRATEGIC CLEANUP")
    print("=" * 50)
    
    # Check and remove redundant files
    for filename in remove_files:
        filepath = os.path.join(current_dir, filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"🗑️  REMOVED: {filename}")
                removed_count += 1
            except Exception as e:
                print(f"⚠️  Could not remove {filename}: {e}")
        else:
            print(f"📭 NOT FOUND: {filename}")
    
    # Report kept files
    print("\n✅ KEPT CORE FILES:")
    for filename in sorted(keep_files):
        filepath = os.path.join(current_dir, filename)
        if os.path.exists(filepath):
            print(f"   ✅ {filename}")
            kept_count += 1
    
    print(f"\n📊 CLEANUP SUMMARY:")
    print(f"   Removed: {removed_count} redundant files")
    print(f"   Kept: {kept_count} core operational files")
    print(f"   Total: {removed_count + kept_count} files processed")
    
    # Create organized directories if they don't exist
    directories = ['core', 'llm', 'gui', 'tests']
    for dir_name in directories:
        dir_path = os.path.join(current_dir, dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"📁 CREATED: {dir_name}/ directory")
    
    print("\n🎉 CLEANUP COMPLETE! System is now organized and efficient.")

if __name__ == "__main__":
    perform_cleanup()
