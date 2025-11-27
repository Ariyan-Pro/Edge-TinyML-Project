import os
import sys
import json

# Add the core directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from plugin_loader import PluginLoader
from sandbox import PluginSandbox

class AutonomousInterface:
    """LLM interface for plugin management and execution"""
    
    def __init__(self, plugins_dir: str = None):
        if plugins_dir is None:
            plugins_dir = os.path.join(os.path.dirname(__file__), '..', 'plugins')
        
        self.plugins_dir = plugins_dir
        self.plugin_loader = PluginLoader(plugins_dir)
        self.sandbox = PluginSandbox()
        self.loaded_plugins = {}
        
        # Load all plugins at startup
        self.load_all_plugins()
    
    def load_all_plugins(self):
        """Load all available plugins"""
        print("🔄 Loading plugins...")
        self.loaded_plugins = self.plugin_loader.load_all_plugins()
        print(f"✅ Loaded {len(self.loaded_plugins)} plugins")
    
    def list_plugins(self):
        """List all available plugins for LLM"""
        plugins_info = self.plugin_loader.list_plugins()
        
        # Format for LLM consumption
        formatted_plugins = []
        for plugin in plugins_info:
            formatted_plugins.append({
                "name": plugin["name"],
                "description": plugin["description"],
                "safety_level": plugin["safety_level"],
                "available_commands": self._get_plugin_commands(plugin["name"])
            })
        
        return {
            "success": True,
            "plugins": formatted_plugins,
            "total_count": len(formatted_plugins)
        }
    
    def _get_plugin_commands(self, plugin_name: str):
        """Get available commands for a plugin"""
        command_map = {
            "weather_tool": ["get_weather", "get_forecast"],
            "notes_tool": ["add_note", "list_notes", "delete_note"],
            "calculator_tool": ["calculate", "convert_units"]
        }
        return command_map.get(plugin_name, [])
    
    def run_plugin(self, plugin_name: str, command: str, parameters = None):
        """Execute a plugin command"""
        if parameters is None:
            parameters = {}
        
        print(f"🔧 Executing: {plugin_name}.{command} with {parameters}")
        
        try:
            # Get the plugin module
            plugin_module = self.plugin_loader.get_plugin(plugin_name)
            if not plugin_module:
                return {"success": False, "error": f"Plugin not found: {plugin_name}"}
            
            # Execute the plugin command
            if hasattr(plugin_module, 'execute'):
                result = plugin_module.execute(command, parameters)
                
                # Log the activity
                self._log_activity(plugin_name, command, parameters, result)
                
                return result
            else:
                return {"success": False, "error": "Plugin missing execute function"}
                
        except Exception as e:
            error_result = {"success": False, "error": str(e)}
            self._log_activity(plugin_name, command, parameters, error_result)
            return error_result
    
    def _log_activity(self, plugin_name: str, command: str, parameters, result):
        """Log plugin activity"""
        import datetime
        
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "plugin": plugin_name,
            "command": command,
            "parameters": parameters,
            "result": result
        }
        
        log_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'plugin_activity.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def process_llm_request(self, request: str):
        """Process LLM request and route to appropriate plugin"""
        request_lower = request.lower()
        
        # Route to appropriate plugin based on keywords
        if any(word in request_lower for word in ['weather', 'temperature', 'forecast']):
            return self._handle_weather_request(request)
        elif any(word in request_lower for word in ['note', 'reminder', 'todo']):
            return self._handle_notes_request(request)
        elif any(word in request_lower for word in ['calculate', 'math', 'convert']):
            return self._handle_calculator_request(request)
        else:
            return {"success": False, "error": "No suitable plugin found for request"}
    
    def _handle_weather_request(self, request: str):
        """Handle weather-related requests"""
        location = "London"  # Default
        if "in" in request:
            location = request.split("in")[-1].strip()
        
        return self.run_plugin("weather_tool", "get_weather", {"location": location})
    
    def _handle_notes_request(self, request: str):
        """Handle notes-related requests"""
        if "list" in request.lower() or "show" in request.lower():
            return self.run_plugin("notes_tool", "list_notes")
        else:
            content = request
            return self.run_plugin("notes_tool", "add_note", {"content": content})
    
    def _handle_calculator_request(self, request: str):
        """Handle calculator requests"""
        import re
        numbers = re.findall(r'\d+', request)
        if numbers and ('+' in request or '-' in request or '*' in request or '/' in request):
            return self.run_plugin("calculator_tool", "calculate", {"expression": request})
        else:
            return {"success": False, "error": "No valid calculation found in request"}

def main():
    """Main test function"""
    print("🧠 AUTONOMOUS EXTENSIONS SYSTEM - TEST")
    print("=" * 50)
    
    interface = AutonomousInterface()
    
    # Test plugin listing
    print("\n📋 Available Plugins:")
    plugins_result = interface.list_plugins()
    for plugin in plugins_result["plugins"]:
        print(f"   • {plugin['name']}: {plugin['description']}")
        print(f"     Commands: {', '.join(plugin['available_commands'])}")
    
    # Test plugin execution
    print("\n🔧 Testing Plugin Execution:")
    
    # Test weather plugin
    print("\n🌤️  Testing Weather Plugin:")
    weather_result = interface.run_plugin("weather_tool", "get_weather", {"location": "London"})
    print(f"   Result: {weather_result}")
    
    # Test notes plugin  
    print("\n📝 Testing Notes Plugin:")
    notes_result = interface.run_plugin("notes_tool", "add_note", {"content": "Test note from autonomous system"})
    print(f"   Add Note: {notes_result}")
    
    list_result = interface.run_plugin("notes_tool", "list_notes", {})
    print(f"   List Notes: {list_result}")
    
    # Test calculator plugin
    print("\n🧮 Testing Calculator Plugin:")
    calc_result = interface.run_plugin("calculator_tool", "calculate", {"expression": "2 + 2 * 3"})
    print(f"   Calculation: {calc_result}")
    
    # Test autonomous request processing
    print("\n�� Testing Autonomous Request Processing:")
    auto_weather = interface.process_llm_request("What's the weather in Paris?")
    print(f"   Auto Weather: {auto_weather}")
    
    auto_note = interface.process_llm_request("Add a reminder to buy groceries")
    print(f"   Auto Note: {auto_note}")
    
    auto_calc = interface.process_llm_request("Calculate 15 * 4 + 10")
    print(f"   Auto Calc: {auto_calc}")
    
    print("\n📊 Checking logs...")
    log_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'plugin_activity.log')
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            log_count = len(f.readlines())
        print(f"   Log entries: {log_count}")
    
    print("\n🎉 Autonomous Extensions System Ready!")
    print("🚀 Phase 5.5 'Autonomous Extensions' - COMPLETE!")

if __name__ == "__main__":
    main()
