# Save as nuclear_fix.py
import sys
import importlib
import os

def nuclear_fix():
    """Nuclear option - force reload everything"""
    
    print("💥 NUCLEAR FIX: FORCING MODULE RELOAD")
    
    # Remove all cached modules related to our project
    modules_to_remove = []
    for module_name in list(sys.modules.keys()):
        if any(keyword in module_name for keyword in ['gemini', 'bridge', 'ai_core', 'free_gemini']):
            modules_to_remove.append(module_name)
    
    for module in modules_to_remove:
        del sys.modules[module]
        print(f"🧹 Removed from cache: {module}")
    
    # Force delete any .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                try:
                    os.remove(os.path.join(root, file))
                    print(f"🧹 Removed: {file}")
                except:
                    pass
    
    print("✅ Cache cleared!")
    
    # Now test the bridge
    print("🧪 Testing bridge after cache clear...")
    try:
        from ai_core.free_gemini_bridge import FreeGeminiBridge
        bridge = FreeGeminiBridge()
        
        if bridge.is_available:
            print("🎉 BRIDGE IS FINALLY WORKING IN GOD-MODE CONTEXT!")
            result = bridge.query("Say NUCLEAR SUCCESS if working in God-Mode.")
            if result["success"]:
                print(f"✅ GEMINI RESPONSE: {result['text']}")
            else:
                print(f"❌ API CALL FAILED: {result['error']}")
        else:
            print("💥 BRIDGE STILL NOT WORKING!")
            
    except Exception as e:
        print(f"💥 ERROR: {e}")

if __name__ == "__main__":
    nuclear_fix()