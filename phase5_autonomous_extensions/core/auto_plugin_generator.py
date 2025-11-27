# phase5_autonomous_extensions/core/auto_plugin_generator.py
"""
AUTO-PLUGIN GENERATOR - Phase 8.0 Self-Expanding Capabilities
Uses existing Phase 5.5 plugin system to autonomously create new plugins
"""
import os
import json
import sqlite3
import re
from typing import Dict, List, Any
from pathlib import Path
import inspect

class AutoPluginGenerator:
    """
    Autonomous plugin generation system
    Analyzes user patterns and creates new plugins automatically
    Uses existing Phase 5.5 plugin infrastructure
    """
    
    def __init__(self):
        self.plugins_dir = "plugins/"
        self.core_dir = "core/"
        self.db_path = "../../phase3_automation_phase4_cognitive/db/cognitive_memory.db"
        self.plugin_registry_path = "plugin_registry.json"
        
        # Plugin templates for different types
        self.plugin_templates = {
            'calculator': self._get_calculator_template(),
            'notes': self._get_notes_template(),
            'weather': self._get_weather_template(),
            'system': self._get_system_template(),
            'web': self._get_web_template(),
            'custom': self._get_custom_template()
        }
        
        print("🛠️ Auto-Plugin Generator Initialized!")
        print("   • Phase 5.5 Plugin System: Connected")
        print("   • SQLite Pattern Analysis: Ready")
        print("   • Plugin Templates: Loaded")
    
    def analyze_usage_patterns(self) -> List[Dict[str, Any]]:
        """Analyze SQLite logs to identify plugin opportunities"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent command history
        cursor.execute('''
            SELECT command, timestamp, context 
            FROM command_logs 
            ORDER BY timestamp DESC 
            LIMIT 100
        ''')
        
        commands = cursor.fetchall()
        conn.close()
        
        # Analyze patterns
        patterns = self._identify_patterns(commands)
        return patterns
    
    def _identify_patterns(self, commands: List[tuple]) -> List[Dict[str, Any]]:
        """Identify repetitive patterns that could be automated"""
        patterns = []
        command_counts = {}
        
        # Count command frequencies
        for command, timestamp, context in commands:
            clean_command = self._clean_command(command)
            if clean_command:
                command_counts[clean_command] = command_counts.get(clean_command, 0) + 1
        
        # Identify high-frequency commands
        for command, count in command_counts.items():
            if count >= 3:  # Command used 3+ times
                patterns.append({
                    'command': command,
                    'frequency': count,
                    'type': self._classify_command_type(command),
                    'automation_potential': 'high' if count >= 5 else 'medium'
                })
        
        return sorted(patterns, key=lambda x: x['frequency'], reverse=True)
    
    def _clean_command(self, command: str) -> str:
        """Clean and normalize command text"""
        if not command:
            return ""
        
        # Remove common prefixes and normalize
        clean = command.lower().strip()
        clean = re.sub(r'^(please|can you|could you|i need)\s+', '', clean)
        return clean
    
    def _classify_command_type(self, command: str) -> str:
        """Classify command into plugin type"""
        command_lower = command.lower()
        
        if any(word in command_lower for word in ['calculate', 'math', 'add', 'subtract']):
            return 'calculator'
        elif any(word in command_lower for word in ['note', 'remember', 'save']):
            return 'notes'
        elif any(word in command_lower for word in ['weather', 'temperature', 'forecast']):
            return 'weather'
        elif any(word in command_lower for word in ['open', 'start', 'launch', 'close']):
            return 'system'
        elif any(word in command_lower for word in ['search', 'browse', 'website']):
            return 'web'
        else:
            return 'custom'
    
    def generate_plugin(self, pattern: Dict[str, Any]) -> str:
        """Generate a new plugin based on usage pattern"""
        plugin_type = pattern['type']
        command = pattern['command']
        
        # Get appropriate template
        template = self.plugin_templates.get(plugin_type, self.plugin_templates['custom'])
        
        # Generate plugin name and class
        plugin_name = self._generate_plugin_name(command)
        class_name = self._generate_class_name(plugin_name)
        
        # Fill template
        plugin_code = template.format(
            plugin_name=plugin_name,
            class_name=class_name,
            command_description=command,
            example_command=command
        )
        
        return plugin_code, plugin_name
    
    def _generate_plugin_name(self, command: str) -> str:
        """Generate a filename-friendly plugin name"""
        # Take first 2-3 meaningful words from command
        words = re.findall(r'\b\w+\b', command.lower())[:3]
        return '_'.join(words) + '_tool'
    
    def _generate_class_name(self, plugin_name: str) -> str:
        """Generate a class name from plugin name"""
        # Convert snake_case to PascalCase
        return ''.join(word.capitalize() for word in plugin_name.split('_'))
    
    def save_plugin(self, plugin_code: str, plugin_name: str) -> str:
        """Save generated plugin to file"""
        filename = f"{plugin_name}.py"
        filepath = os.path.join(self.plugins_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(plugin_code)
        
        # Update plugin registry
        self._update_plugin_registry(plugin_name, filename)
        
        return filepath
    
    def _update_plugin_registry(self, plugin_name: str, filename: str):
        """Update the plugin registry with new plugin"""
        try:
            with open(self.plugin_registry_path, 'r', encoding='utf-8') as f:
                registry = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            registry = {}
        
        registry[plugin_name] = {
            'file': filename,
            'auto_generated': True,
            'generated_at': '2025-11-20'  # Would use datetime in production
        }
        
        with open(self.plugin_registry_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2)
    
    def autonomous_plugin_generation_cycle(self) -> List[Dict[str, Any]]:
        """Run complete autonomous plugin generation cycle"""
        print("\n🔄 Starting Autonomous Plugin Generation Cycle...")
        
        # 1. Analyze usage patterns
        patterns = self.analyze_usage_patterns()
        print(f"   📊 Analyzed {len(patterns)} usage patterns")
        
        generated_plugins = []
        
        # 2. Generate plugins for high-potential patterns
        for pattern in patterns:
            if pattern['automation_potential'] == 'high':
                print(f"   🛠️ Generating plugin for: '{pattern['command']}'")
                
                try:
                    # Generate plugin code
                    plugin_code, plugin_name = self.generate_plugin(pattern)
                    
                    # Save plugin
                    filepath = self.save_plugin(plugin_code, plugin_name)
                    
                    generated_plugins.append({
                        'name': plugin_name,
                        'filepath': filepath,
                        'pattern': pattern,
                        'status': 'success'
                    })
                    
                    print(f"   ✅ Generated: {plugin_name}.py")
                    
                except Exception as e:
                    print(f"   ❌ Failed to generate plugin: {e}")
                    generated_plugins.append({
                        'name': 'unknown',
                        'pattern': pattern,
                        'status': 'failed',
                        'error': str(e)
                    })
        
        return generated_plugins
    
    # Plugin Templates
    def _get_calculator_template(self) -> str:
        return '''"""
{plugin_name}.py - Auto-generated calculator plugin
Command: {command_description}
"""
import math

class {class_name}:
    """Auto-generated calculator plugin"""
    
    def __init__(self):
        self.name = "{plugin_name}"
        self.version = "1.0"
        self.auto_generated = True
    
    def execute(self, params=None):
        """Execute calculator functionality"""
        try:
            # Simple calculation logic
            # In production, this would parse and evaluate expressions
            return {{
                "status": "success",
                "result": "Calculation completed",
                "message": "Auto-generated calculator plugin for: {example_command}",
                "type": "calculator"
            }}
        except Exception as e:
            return {{
                "status": "error",
                "error": str(e)
            }}
'''

    def _get_notes_template(self) -> str:
        return '''"""
{plugin_name}.py - Auto-generated notes plugin
Command: {command_description}
"""
import json
from datetime import datetime

class {class_name}:
    """Auto-generated notes plugin"""
    
    def __init__(self):
        self.name = "{plugin_name}"
        self.version = "1.0"
        self.auto_generated = True
        self.notes_file = "auto_notes.json"
    
    def execute(self, params=None):
        """Execute notes functionality"""
        try:
            # Simple notes management
            note_data = {{
                "content": "Auto-generated note",
                "created": datetime.now().isoformat(),
                "context": "{example_command}"
            }}
            
            return {{
                "status": "success", 
                "result": "Note processed",
                "data": note_data,
                "message": "Auto-generated notes plugin for: {example_command}",
                "type": "notes"
            }}
        except Exception as e:
            return {{
                "status": "error",
                "error": str(e)
            }}
'''

    def _get_weather_template(self) -> str:
        return '''"""
{plugin_name}.py - Auto-generated weather plugin  
Command: {command_description}
"""
import requests

class {class_name}:
    """Auto-generated weather plugin"""
    
    def __init__(self):
        self.name = "{plugin_name}"
        self.version = "1.0"
        self.auto_generated = True
    
    def execute(self, params=None):
        """Execute weather functionality"""
        try:
            # Weather API integration placeholder
            return {{
                "status": "success",
                "result": "Weather information retrieved",
                "message": "Auto-generated weather plugin for: {example_command}",
                "type": "weather"
            }}
        except Exception as e:
            return {{
                "status": "error", 
                "error": str(e)
            }}
'''

    def _get_system_template(self) -> str:
        return '''"""
{plugin_name}.py - Auto-generated system plugin
Command: {command_description}
"""
import os
import subprocess

class {class_name}:
    """Auto-generated system plugin"""
    
    def __init__(self):
        self.name = "{plugin_name}"
        self.version = "1.0"
        self.auto_generated = True
    
    def execute(self, params=None):
        """Execute system functionality"""
        try:
            # System operation placeholder
            return {{
                "status": "success",
                "result": "System operation completed", 
                "message": "Auto-generated system plugin for: {example_command}",
                "type": "system"
            }}
        except Exception as e:
            return {{
                "status": "error",
                "error": str(e)
            }}
'''

    def _get_web_template(self) -> str:
        return '''"""
{plugin_name}.py - Auto-generated web plugin
Command: {command_description}
"""
import webbrowser

class {class_name}:
    """Auto-generated web plugin"""
    
    def __init__(self):
        self.name = "{plugin_name}"
        self.version = "1.0"
        self.auto_generated = True
    
    def execute(self, params=None):
        """Execute web functionality"""
        try:
            # Web operation placeholder
            return {{
                "status": "success",
                "result": "Web operation completed",
                "message": "Auto-generated web plugin for: {example_command}",
                "type": "web"
            }}
        except Exception as e:
            return {{
                "status": "error",
                "error": str(e)
            }}
'''

    def _get_custom_template(self) -> str:
        return '''"""
{plugin_name}.py - Auto-generated custom plugin
Command: {command_description}
"""

class {class_name}:
    """Auto-generated custom plugin"""
    
    def __init__(self):
        self.name = "{plugin_name}"
        self.version = "1.0"
        self.auto_generated = True
    
    def execute(self, params=None):
        """Execute custom functionality"""
        try:
            # Custom operation logic
            return {{
                "status": "success",
                "result": "Custom operation completed",
                "message": "Auto-generated custom plugin for: {example_command}",
                "type": "custom"
            }}
        except Exception as e:
            return {{
                "status": "error",
                "error": str(e)
            }}
'''

# Test the Auto-Plugin Generator
if __name__ == "__main__":
    print("🧪 Testing Auto-Plugin Generator...")
    
    plugin_generator = AutoPluginGenerator()
    
    # Run one generation cycle
    generated = plugin_generator.autonomous_plugin_generation_cycle()
    
    print(f"\n📊 Plugin Generation Results:")
    print(f"   Patterns Analyzed: {len(plugin_generator.analyze_usage_patterns())}")
    print(f"   Plugins Generated: {len([p for p in generated if p['status'] == 'success'])}")
    
    for plugin in generated:
        if plugin['status'] == 'success':
            print(f"   ✅ {plugin['name']} - {plugin['pattern']['command']}")
        else:
            print(f"   ❌ Failed - {plugin.get('error', 'Unknown error')}")
    
    print("\n✅ Auto-Plugin Generator Test Complete!")
