# Save as debug_gemini_connection.py
import sys
import os

# Add the parent directory to Python path
sys.path.append('..')

try:
    from ai_core.free_gemini_bridge import FreeGeminiBridge
    print("🔍 Testing Gemini Bridge Connection...")
    
    # Test the bridge
    bridge = FreeGeminiBridge()
    print(f"🔑 API Key Status: {'LOADED' if bridge.is_available else 'MISSING'}")
    
    if bridge.is_available:
        print("🧪 Testing API call...")
        result = bridge.query("Say 'CONNECTION SUCCESSFUL' if you can hear me.")
        if result['success']:
            print(f"🎉 Gemini Response: {result['text']}")
        else:
            print(f"❌ API Error: {result['error']}")
    else:
        print("❌ API key not loaded. Checking config paths...")
        
        # Check config file locations
        config_paths = [
            '../config/gemini_config.json',
            '../../config/gemini_config.json', 
            'config/gemini_config.json'
        ]
        
        for path in config_paths:
            if os.path.exists(path):
                print(f"✅ Config found: {path}")
                with open(path, 'r') as f:
                    import json
                    config = json.load(f)
                    key_preview = config.get('api_key', '')[:10] + '...' if config.get('api_key') else 'MISSING'
                    print(f"   API Key: {key_preview}")
            else:
                print(f"❌ Config not found: {path}")
                
except Exception as e:
    print(f"💥 Error: {e}")
    import traceback
    traceback.print_exc()