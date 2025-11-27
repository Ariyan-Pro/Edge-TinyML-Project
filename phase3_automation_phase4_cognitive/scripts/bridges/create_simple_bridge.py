# Save as create_simple_bridge.py
import os

def create_simple_bridge():
    """Create a simple, guaranteed-working bridge without encoding issues"""
    
    bridge_code = '''
"""
SIMPLE WORKING GEMINI BRIDGE
No fancy characters, guaranteed to work
"""

import os
import json
import requests
from typing import Optional, Dict, Any

class FreeGeminiBridge:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or self._load_api_key_simple()
        self.is_available = bool(self.api_key)
        print("BRIDGE STATUS: READY" if self.is_available else "BRIDGE STATUS: FAILED")
        
    def _load_api_key_simple(self) -> Optional[str]:
        """Simple API key loader"""
        print("SEARCHING FOR API KEY...")
        
        # Try config file in config directory
        config_path = "config/gemini_config.json"
        if os.path.exists(config_path):
            print("CONFIG FOUND: config/gemini_config.json")
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    api_key = config.get('api_key', '').strip()
                    if api_key:
                        print("API KEY LOADED SUCCESSFULLY")
                        return api_key
            except Exception as e:
                print(f"ERROR READING CONFIG: {e}")
        
        print("NO API KEY FOUND")
        return None
    
    def query(self, prompt: str, context: str = "") -> Dict[str, Any]:
        """Query Gemini API"""
        if not self.is_available:
            return {"success": False, "error": "API not configured"}
        
        endpoint = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent"
        url = f"{endpoint}?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            print(f"API CALL TO: {endpoint}")
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'candidates' in data and data['candidates']:
                    text = data['candidates'][0]['content']['parts'][0]['text']
                    return {
                        "success": True,
                        "text": text.strip()
                    }
            else:
                print(f"API FAILED: {response.status_code}")
                
        except Exception as e:
            print(f"API ERROR: {e}")
        
        return {"success": False, "error": "API call failed"}


class HybridIntelligenceManager:
    def __init__(self, gemini_bridge: FreeGeminiBridge):
        self.gemini = gemini_bridge
        self.use_online = gemini_bridge.is_available
        print(f"HYBRID MANAGER: {'ONLINE' if self.use_online else 'OFFLINE'}")
    
    def process_query(self, user_input: str, context: Dict = None) -> str:
        if self.use_online:
            print("USING GEMINI...")
            result = self.gemini.query(user_input)
            if result['success']:
                return result['text']
            else:
                print(f"GEMINI FAILED: {result['error']}")
        
        return f"Local response: {user_input}"
'''

    # Write the simple bridge
    with open('ai_core/free_gemini_bridge.py', 'w') as f:
        f.write(bridge_code)
    
    print("SIMPLE BRIDGE CREATED!")
    
    # Test it
    print("TESTING BRIDGE...")
    import sys
    sys.path.append('.')
    
    try:
        from ai_core.free_gemini_bridge import FreeGeminiBridge
        bridge = FreeGeminiBridge()
        
        if bridge.is_available:
            print("BRIDGE IS WORKING!")
            result = bridge.query("Say SUCCESS if connected.")
            if result["success"]:
                print(f"GEMINI RESPONSE: {result['text']}")
            else:
                print(f"API CALL FAILED: {result['error']}")
        else:
            print("BRIDGE FAILED - CHECK CONFIG FILE")
            
    except Exception as e:
        print(f"BRIDGE TEST ERROR: {e}")

if __name__ == "__main__":
    create_simple_bridge()