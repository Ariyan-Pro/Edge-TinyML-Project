# resource_monitor.py - PHASE 6.0 CORE COMPONENT
"""
PHASE 6.0: Resource Monitor - Essential for Autonomous Debugger Integration
"""

import psutil
import time
from typing import Dict, List

class ResourceMonitor:
    """
    Phase 6.0 Resource Monitoring System
    Provides the foundation for resource-aware autonomous debugging
    """
    
    def __init__(self):
        print("📊 INITIALIZING PHASE 6.0 RESOURCE MONITOR...")
        
        # Performance thresholds (aligned with project specs)
        self.thresholds = {
            'memory_mb': 500,           # Target: <500 MB RAM
            'cpu_percent': 80,          # Target: <80% CPU
            'model_load_memory_gb': 0.9, # Phase 6.0: Prevent loading if <0.9 GB available
            'system_stable_memory': 85   # System considered stable below 85% memory usage
        }
        
        # Monitoring history
        self.history = []
        self.alert_count = 0
        
        print("✅ RESOURCE MONITOR: PHASE 6.0 CORE OPERATIONAL")
        print(f"   🎯 Memory Threshold: {self.thresholds['memory_mb']} MB")
        print(f"   ⚡ CPU Threshold: {self.thresholds['cpu_percent']}%")
        print(f"   🤖 Model Load Protection: {self.thresholds['model_load_memory_gb']} GB")
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        try:
            # Memory usage
            memory = psutil.virtual_memory()
            memory_used_mb = memory.used / (1024 * 1024)
            memory_percent = memory.percent
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Disk usage (optional)
            disk = psutil.disk_usage('/')
            
            # Process-specific monitoring
            current_process = psutil.Process()
            process_memory = current_process.memory_info().rss / (1024 * 1024)
            
            # System stability assessment
            system_stable = (
                memory_used_mb < self.thresholds['memory_mb'] and
                cpu_percent < self.thresholds['cpu_percent'] and
                memory_percent < self.thresholds['system_stable_memory']
            )
            
            status = {
                'memory_used_mb': round(memory_used_mb, 2),
                'memory_percent': round(memory_percent, 2),
                'cpu_percent': round(cpu_percent, 2),
                'process_memory_mb': round(process_memory, 2),
                'system_stable': system_stable,
                'available_memory_gb': round(memory.available / (1024 * 1024 * 1024), 2),
                'timestamp': time.time()
            }
            
            # Log to history
            self.history.append(status)
            if len(self.history) > 100:  # Keep last 100 readings
                self.history.pop(0)
            
            # Check for alerts
            if not system_stable:
                self.alert_count += 1
                if self.alert_count == 1:  # Only log first alert to avoid spam
                    print(f"⚠️  RESOURCE ALERT: Memory {memory_used_mb:.0f}MB, CPU {cpu_percent:.0f}%")
            
            return status
            
        except Exception as e:
            print(f"❌ Resource monitoring error: {e}")
            return {
                'memory_used_mb': 0,
                'memory_percent': 0,
                'cpu_percent': 0,
                'process_memory_mb': 0,
                'system_stable': True,
                'available_memory_gb': 0,
                'timestamp': time.time(),
                'error': str(e)
            }
    
    def can_load_model(self, model_size_mb: float = 637) -> Dict:
        """
        Phase 6.0 Model Load Protection
        Prevents system crashes by checking resources before model loading
        """
        status = self.get_system_status()
        available_gb = status['available_memory_gb']
        required_gb = model_size_mb / 1024  # Convert MB to GB
        
        can_load = available_gb > self.thresholds['model_load_memory_gb']
        
        decision = {
            'can_load': can_load,
            'available_gb': available_gb,
            'required_gb': required_gb,
            'threshold_gb': self.thresholds['model_load_memory_gb'],
            'recommendation': 'SAFE_TO_LOAD' if can_load else 'DEFER_LOADING'
        }
        
        if not can_load:
            print(f"🛑 MODEL LOAD BLOCKED: {available_gb:.2f}GB available < {self.thresholds['model_load_memory_gb']}GB threshold")
        
        return decision
    
    def get_performance_report(self) -> Dict:
        """Generate performance report for autonomous debugger"""
        if not self.history:
            return {'error': 'No monitoring data available'}
        
        recent_readings = self.history[-10:]  # Last 10 readings
        
        avg_memory = sum(r['memory_used_mb'] for r in recent_readings) / len(recent_readings)
        avg_cpu = sum(r['cpu_percent'] for r in recent_readings) / len(recent_readings)
        
        return {
            'performance_metrics': {
                'average_memory_mb': round(avg_memory, 2),
                'average_cpu_percent': round(avg_cpu, 2),
                'memory_violations': sum(1 for r in recent_readings if r['memory_used_mb'] > self.thresholds['memory_mb']),
                'cpu_violations': sum(1 for r in recent_readings if r['cpu_percent'] > self.thresholds['cpu_percent']),
                'system_stability': sum(1 for r in recent_readings if r['system_stable']) / len(recent_readings)
            },
            'thresholds': self.thresholds,
            'monitoring_duration': f"{len(self.history)} readings",
            'alerts_triggered': self.alert_count
        }
    
    def continuous_monitoring(self, interval_seconds: int = 5):
        """Continuous monitoring mode for integration with autonomous systems"""
        print(f"📈 STARTING CONTINUOUS MONITORING ({interval_seconds}s intervals)...")
        
        try:
            while True:
                status = self.get_system_status()
                
                # Only print status if there are issues or first reading
                if not status['system_stable'] or len(self.history) == 1:
                    stability = "STABLE" if status['system_stable'] else "UNSTABLE"
                    print(f"   📊 Status: {stability} | Memory: {status['memory_used_mb']}MB | CPU: {status['cpu_percent']}%")
                
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print("\n🛑 CONTINUOUS MONITORING STOPPED")

if __name__ == "__main__":
    # Test the resource monitor
    monitor = ResourceMonitor()
    
    print("\n🧪 TESTING RESOURCE MONITOR...")
    
    # Single status check
    status = monitor.get_system_status()
    print(f"📊 SYSTEM STATUS: {status}")
    
    # Model load decision
    model_decision = monitor.can_load_model(637)  # TinyLlama model size
    print(f"🤖 MODEL LOAD DECISION: {model_decision}")
    
    # Performance report
    report = monitor.get_performance_report()
    print(f"📈 PERFORMANCE REPORT: {report}")
    
    print("\n✅ PHASE 6.0 RESOURCE MONITOR: OPERATIONAL")