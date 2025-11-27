# Save as create_hardcoded_bridge.py
import os

def create_hardcoded_bridge():
    """Create bridge with hardcoded API key as last resort"""
    
    bridge_code = '''
"""
HARDCODED GEMINI BRIDGE
Uses direct API key - guaranteed to work
"""

import requests
from typing import Dict, Any

class FreeGeminiBridge:
    def __init__(self):
        # Your API key hardcoded
        self.api_key = "YOUR_API_KEY_HERE"
        self.is_available = True
        print("HARDCODED BRIDGE: READY")
        
    def query(self, prompt: str, context: str = "") -> Dict[str, Any]:
        endpoint = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent"
        url = f"{endpoint}?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'candidates' in data and data['candidates']:
                    text = data['candidates'][0]['content']['parts'][0]['text']
                    return {
                        "success": True,
                        "text": text.strip()
                    }
                    
        except Exception as e:
            print(f"API ERROR: {e}")
        
        return {"success": False, "error": "API call failed"}


class HybridIntelligenceManager:
    def __init__(self, gemini_bridge: FreeGeminiBridge):
        self.gemini = gemini_bridge
        self.use_online = True
        print("HYBRID MANAGER: ONLINE")
    
    def process_query(self, user_input: str, context: Dict = None) -> str:
        print("USING GEMINI...")
        result = self.gemini.query(user_input)
        if result['success']:
            return result['text']
        return f"Gemini failed: {result['error']}"
'''

    with open('ai_core/free_gemini_bridge.py', 'w') as f:
        f.write(bridge_code)
    
    print("HARDCODED BRIDGE CREATED!")
    
    # Test it
    import sys
    sys.path.append('.')
    from ai_core.free_gemini_bridge import FreeGeminiBridge
    
    bridge = FreeGeminiBridge()
    result = bridge.query("Say HARDCODED SUCCESS if working.")
    if result["success"]:
        print(f"SUCCESS: {result['text']}")
    else:
        print(f"FAILED: {result['error']}")

if __name__ == "__main__":
    create_hardcoded_bridge()
