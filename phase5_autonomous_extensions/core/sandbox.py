import ast
import sys
import types
from typing import Dict, Any, List

class PluginSandbox:
    """Secure execution environment for plugins"""
    
    def __init__(self):
        self.allowed_modules = {
            'math', 'datetime', 'time', 'json', 're', 'random', 
            'collections', 'itertools', 'functools', 'operator'
        }
        self.restricted_builtins = {
            'open', 'file', 'exec', 'eval', 'compile', '__import__',
            'exit', 'quit', 'globals', 'locals', 'dir', 'input'
        }
        
    def safe_builtins(self) -> Dict[str, Any]:
        """Create safe builtins dictionary"""
        safe_builtins = {}
        for name in dir(__builtins__):
            if name not in self.restricted_builtins:
                safe_builtins[name] = getattr(__builtins__, name)
        return safe_builtins
    
    def validate_code(self, code: str) -> bool:
        """Validate code for safety"""
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                # Check for imports
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    module_name = node.module if isinstance(node, ast.ImportFrom) else node.names[0].name
                    if module_name and module_name.split('.')[0] not in self.allowed_modules:
                        return False
                
                # Check for dangerous function calls
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in self.restricted_builtins:
                            return False
            
            return True
        except:
            return False
    
    def execute_plugin(self, code: str, context: Dict[str, Any] = None) -> Any:
        """Execute plugin code in sandbox"""
        if not self.validate_code(code):
            raise SecurityError("Code validation failed")
        
        # Create execution context
        exec_globals = {
            '__builtins__': self.safe_builtins(),
            '__name__': '__plugin__'
        }
        
        if context:
            exec_globals.update(context)
        
        try:
            # Compile and execute
            compiled = compile(code, '<plugin>', 'exec')
            local_vars = {}
            exec(compiled, exec_globals, local_vars)
            
            return local_vars
        except Exception as e:
            raise PluginExecutionError(f"Plugin execution failed: {e}")

class SecurityError(Exception):
    """Security violation in plugin"""
    pass

class PluginExecutionError(Exception):
    """Plugin execution error"""
    pass
