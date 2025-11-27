# Save as fix_gemini_definitive.py
import os
import sys

def fix_gemini_bridge_completely():
    """Completely fix the Gemini bridge config paths"""
    bridge_path = "ai_core/free_gemini_bridge.py"
    
    if os.path.exists(bridge_path):
        with open(bridge_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the entire config loading section
        old_config_section = '''def _load_api_key(self) -> Optional[str]:
        """Load API key from config file"""
        config_paths = [
            'gemini_config.json',
            '../gemini_config.json',
            '../../gemini_config.json'
        ]'''
        
        new_config_section = '''def _load_api_key(self) -> Optional[str]:
        """Load API key from config file"""
        config_paths = [
            '../config/gemini_config.json',
            'config/gemini_config.json',
            '../../config/gemini_config.json',
            'gemini_config.json'
        ]'''
        
        content = content.replace(old_config_section, new_config_section)
        
        with open(bridge_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Completely fixed Gemini bridge config paths")
        
        # Test the fix
        print("🧪 Testing the fix...")
        os.system('cd voice_interface && python ../debug_gemini_connection.py')
    else:
        print(f"❌ Bridge file not found: {bridge_path}")

if __name__ == "__main__":
    fix_gemini_bridge_completely()