import importlib.util
import os
import json
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path

class PluginLoader:
    """Dynamic plugin loader and manager"""
    
    def __init__(self, plugins_dir: str = "plugins", registry_file: str = "plugin_registry.json"):
        self.plugins_dir = Path(plugins_dir)
        self.registry_file = Path(registry_file)
        self.loaded_plugins: Dict[str, Any] = {}
        self.plugin_registry: List[Dict] = []
        
        # Create plugins directory if it doesn't exist
        self.plugins_dir.mkdir(exist_ok=True)
        
        # Load or create registry
        self.load_registry()
    
    def load_registry(self):
        """Load plugin registry from JSON file"""
        if self.registry_file.exists():
            with open(self.registry_file, 'r') as f:
                self.plugin_registry = json.load(f).get('plugins', [])
        else:
            self.plugin_registry = []
            self.save_registry()
    
    def save_registry(self):
        """Save plugin registry to JSON file"""
        registry_data = {'plugins': self.plugin_registry}
        with open(self.registry_file, 'w') as f:
            json.dump(registry_data, f, indent=2)
    
    def discover_plugins(self) -> List[str]:
        """Discover all .py files in plugins directory"""
        plugin_files = []
        for file_path in self.plugins_dir.glob("*.py"):
            if file_path.name != "__init__.py":
                plugin_files.append(file_path.name)
        return plugin_files
    
    def load_plugin(self, plugin_file: str) -> Optional[Any]:
        """Dynamically load a plugin module"""
        try:
            plugin_path = self.plugins_dir / plugin_file
            
            if not plugin_path.exists():
                print(f"❌ Plugin file not found: {plugin_file}")
                return None
            
            # Create module spec
            module_name = plugin_path.stem
            spec = importlib.util.spec_from_file_location(module_name, plugin_path)
            
            if spec is None or spec.loader is None:
                print(f"❌ Failed to create spec for: {plugin_file}")
                return None
            
            # Create and load module
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            # Register plugin
            self.loaded_plugins[module_name] = module
            
            # Update registry if needed
            self._update_registry(module_name, plugin_file, module)
            
            print(f"✅ Loaded plugin: {module_name}")
            return module
            
        except Exception as e:
            print(f"❌ Failed to load plugin {plugin_file}: {e}")
            return None
    
    def _update_registry(self, plugin_name: str, plugin_file: str, module: Any):
        """Update registry with plugin metadata"""
        # Check if plugin already in registry
        existing = next((p for p in self.plugin_registry if p['name'] == plugin_name), None)
        
        if not existing:
            # Extract metadata from module
            description = getattr(module, '__description__', 'No description provided')
            safety_level = getattr(module, '__safety_level__', 'unknown')
            version = getattr(module, '__version__', '1.0')
            author = getattr(module, '__author__', 'Unknown')
            
            plugin_info = {
                'name': plugin_name,
                'description': description,
                'safety_level': safety_level,
                'file': plugin_file,
                'version': version,
                'author': author
            }
            
            self.plugin_registry.append(plugin_info)
            self.save_registry()
    
    def load_all_plugins(self) -> Dict[str, Any]:
        """Load all discovered plugins"""
        plugin_files = self.discover_plugins()
        print(f"🔍 Discovered {len(plugin_files)} plugin files")
        
        for plugin_file in plugin_files:
            self.load_plugin(plugin_file)
        
        return self.loaded_plugins
    
    def get_plugin(self, plugin_name: str) -> Optional[Any]:
        """Get loaded plugin by name"""
        return self.loaded_plugins.get(plugin_name)
    
    def list_plugins(self) -> List[Dict]:
        """List all available plugins with metadata"""
        return self.plugin_registry
    
    def unload_plugin(self, plugin_name: str):
        """Unload a plugin"""
        if plugin_name in self.loaded_plugins:
            del self.loaded_plugins[plugin_name]
            if plugin_name in sys.modules:
                del sys.modules[plugin_name]
            print(f"✅ Unloaded plugin: {plugin_name}")
    
    def reload_plugin(self, plugin_name: str) -> Optional[Any]:
        """Reload a plugin"""
        plugin_info = next((p for p in self.plugin_registry if p['name'] == plugin_name), None)
        if plugin_info:
            self.unload_plugin(plugin_name)
            return self.load_plugin(plugin_info['file'])
        return None
