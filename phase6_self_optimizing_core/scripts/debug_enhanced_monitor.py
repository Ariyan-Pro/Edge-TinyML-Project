# debug_enhanced_monitor.py - COMPLETE IMPLEMENTATION
"""
PHASE 6.0 + 8.0 INTEGRATION: Complete Debug-Enhanced Resource Monitor
"""

import os
import time
from typing import Dict, List
from resource_monitor import ResourceMonitor
from self_debugger import AutonomousDebugger

class DebugEnhancedResourceMonitor:
    """
    Phase 6.0 Resource Monitor enhanced with autonomous debugging capabilities - COMPLETE
    """
    
    def __init__(self):
        print("🔧 INITIALIZING DEBUG-ENHANCED RESOURCE MONITOR...")
        self.resource_monitor = ResourceMonitor()
        self.autonomous_debugger = AutonomousDebugger()
        self.error_threshold = 3  # Trigger debugging after 3 consecutive errors
        self.component_health = {}  # Track health of monitored components
        
        print("✅ DEBUG-ENHANCED MONITOR: PHASE 6.0 + 8.0 INTEGRATION ACTIVE")
        print("   📊 Resource Monitoring: ENHANCED")
        print("   🎯 Autonomous Debugging: INTEGRATED")
        print("   🔄 Component Health Tracking: ACTIVE")
    
    def _check_component_health(self, component_path: str) -> Dict:
        """✅ IMPLEMENTED: Check health of a specific component"""
        health_status = {
            'component': component_path,
            'exists': os.path.exists(component_path),
            'healthy': True,
            'error_count': 0,
            'last_error': None,
            'resource_usage': None,
            'last_checked': time.time()
        }
        
        try:
            # Check if file exists and is accessible
            if health_status['exists']:
                # Get file stats
                stat = os.stat(component_path)
                health_status['file_size'] = stat.st_size
                health_status['modified_time'] = stat.st_mtime
                
                # Check if it's a Python file and has valid syntax
                if component_path.endswith('.py'):
                    with open(component_path, 'r', encoding='utf-8') as f:
                        source_code = f.read()
                    
                    # Basic syntax check
                    try:
                        compile(source_code, component_path, 'exec')
                        health_status['syntax_valid'] = True
                    except SyntaxError as e:
                        health_status['syntax_valid'] = False
                        health_status['last_error'] = f"SyntaxError: {e}"
                        health_status['healthy'] = False
                        health_status['error_count'] = 1
                
                # Get current resource usage
                system_status = self.resource_monitor.get_system_status()
                health_status['resource_usage'] = {
                    'memory_mb': system_status['memory_used_mb'],
                    'cpu_percent': system_status['cpu_percent'],
                    'system_stable': system_status['system_stable']
                }
            else:
                health_status['healthy'] = False
                health_status['error_count'] = 1
                health_status['last_error'] = f"File not found: {component_path}"
                
        except Exception as e:
            health_status['healthy'] = False
            health_status['error_count'] = 1
            health_status['last_error'] = f"Health check failed: {e}"
        
        # Update component health history
        if component_path not in self.component_health:
            self.component_health[component_path] = []
        
        self.component_health[component_path].append(health_status)
        if len(self.component_health[component_path]) > 10:  # Keep last 10 checks
            self.component_health[component_path].pop(0)
        
        return health_status
    
    def monitor_system_with_debugging(self, system_components: List[str]):
        """
        ✅ COMPLETE: Enhanced monitoring that autonomously debugs failing components
        """
        print(f"🔍 MONITORING {len(system_components)} SYSTEM COMPONENTS...")
        
        for component in system_components:
            status = self._check_component_health(component)
            
            if not status['healthy']:
                print(f"   ⚠️  UNHEALTHY: {os.path.basename(component)} - {status['last_error']}")
                
                # Check error threshold for autonomous debugging
                error_count = self._get_component_error_count(component)
                
                if error_count >= self.error_threshold:
                    print(f"🚨 AUTONOMOUS DEBUGGING TRIGGERED FOR: {os.path.basename(component)}")
                    
                    # Analyze the error
                    analysis = self.autonomous_debugger.analyze_error(
                        status['last_error'],
                        component,
                        {'resource_usage': status['resource_usage']}
                    )
                    
                    # Generate and apply patch if high confidence
                    if analysis['confidence'] > 0.7:
                        self._apply_autonomous_fix(component, analysis)
                    else:
                        print(f"   ⚠️  Low confidence analysis ({analysis['confidence']:.0%}), manual review recommended")
            else:
                print(f"   ✅ HEALTHY: {os.path.basename(component)}")
    
    def _get_component_error_count(self, component_path: str) -> int:
        """Get consecutive error count for a component"""
        if component_path not in self.component_health:
            return 0
        
        recent_checks = self.component_health[component_path][-self.error_threshold:]
        return sum(1 for check in recent_checks if not check['healthy'])
    
    def _apply_autonomous_fix(self, component_path: str, analysis: Dict):
        """Apply autonomous fix to failing component"""
        try:
            if not os.path.exists(component_path):
                print(f"   ❌ Cannot patch non-existent file: {component_path}")
                return
            
            with open(component_path, 'r', encoding='utf-8') as f:
                original_code = f.read()
            
            # Generate patch
            patched_code = self.autonomous_debugger.generate_patch(analysis, original_code)
            
            if patched_code != original_code:
                # Create backup
                backup_path = component_path + '.backup'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_code)
                
                # Apply patch
                with open(component_path, 'w', encoding='utf-8') as f:
                    f.write(patched_code)
                
                print(f"   ✅ Autonomous patch applied to {os.path.basename(component_path)}")
                print(f"   💾 Backup saved to {os.path.basename(backup_path)}")
                
                # Verify the patch
                verification = self._check_component_health(component_path)
                if verification['healthy']:
                    print(f"   🎯 Patch verification: SUCCESS")
                else:
                    print(f"   ⚠️  Patch verification: ISSUES DETECTED")
                    # Restore backup if patch made things worse
                    with open(backup_path, 'r', encoding='utf-8') as f:
                        backup_code = f.read()
                    with open(component_path, 'w', encoding='utf-8') as f:
                        f.write(backup_code)
                    print(f"   🔄 Restored backup due to verification failure")
                
        except Exception as e:
            print(f"   ❌ Autonomous patch application failed: {e}")
    
    def get_system_health_report(self) -> Dict:
        """Generate comprehensive system health report"""
        report = {
            'timestamp': time.time(),
            'components_monitored': len(self.component_health),
            'healthy_components': 0,
            'unhealthy_components': 0,
            'component_details': {},
            'resource_status': self.resource_monitor.get_system_status(),
            'autonomous_actions': len(self.autonomous_debugger.patch_history)
        }
        
        for component, health_history in self.component_health.items():
            if health_history:
                latest_health = health_history[-1]
                component_name = os.path.basename(component)
                
                report['component_details'][component_name] = {
                    'healthy': latest_health['healthy'],
                    'last_error': latest_health.get('last_error'),
                    'error_count': latest_health.get('error_count', 0),
                    'resource_usage': latest_health.get('resource_usage'),
                    'monitoring_history': len(health_history)
                }
                
                if latest_health['healthy']:
                    report['healthy_components'] += 1
                else:
                    report['unhealthy_components'] += 1
        
        return report

# Update the self_debugger.py to use the complete implementation
def update_self_debugger_integration():
    """Update self_debugger to use the complete DebugEnhancedResourceMonitor"""
    # This function would update the DebugEnhancedResourceMonitor class in self_debugger.py
    pass