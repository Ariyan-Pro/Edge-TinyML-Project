import psutil
import time
import threading
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class SystemMetrics:
    cpu_percent: float
    memory_percent: float
    memory_available_gb: float
    gpu_percent: float = 0.0  # Placeholder for GPU monitoring
    timestamp: float = 0.0

class ResourceMonitor:
    """Real-time system resource monitoring"""
    
    def __init__(self, update_interval: float = 2.0):
        self.update_interval = update_interval
        self.metrics_history: List[SystemMetrics] = []
        self.max_history_size = 100
        self.is_monitoring = False
        self.monitor_thread = None
        
        # Resource thresholds
        self.cpu_threshold_high = 80.0  # Switch to smaller model
        self.cpu_threshold_low = 40.0   # Switch to larger model
        self.memory_threshold_high = 85.0
        self.memory_threshold_low = 50.0
    
    def get_current_metrics(self) -> SystemMetrics:
        """Get current system metrics"""
        try:
            # CPU usage (average over 1 second for accuracy)
            cpu_percent = psutil.cpu_percent(interval=0.5)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available_gb = memory.available / (1024 ** 3)  # Convert to GB
            
            # GPU monitoring placeholder (would use GPUtil in real implementation)
            gpu_percent = 0.0
            
            return SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                memory_available_gb=memory_available_gb,
                gpu_percent=gpu_percent,
                timestamp=time.time()
            )
        except Exception as e:
            print(f"❌ Error getting system metrics: {e}")
            return SystemMetrics(0.0, 0.0, 0.0, 0.0, time.time())
    
    def start_monitoring(self):
        """Start continuous resource monitoring"""
        if self.is_monitoring:
            return
            
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        print("🔍 Resource monitoring started")
    
    def stop_monitoring(self):
        """Stop resource monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
        print("🛑 Resource monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            metrics = self.get_current_metrics()
            self.metrics_history.append(metrics)
            
            # Keep history size manageable
            if len(self.metrics_history) > self.max_history_size:
                self.metrics_history.pop(0)
            
            time.sleep(self.update_interval)
    
    def get_resource_status(self) -> Dict[str, any]:
        """Get current resource status and recommendations"""
        if not self.metrics_history:
            metrics = self.get_current_metrics()
        else:
            metrics = self.metrics_history[-1]
        
        # Determine if resources are constrained
        cpu_constrained = metrics.cpu_percent > self.cpu_threshold_high
        memory_constrained = metrics.memory_percent > self.memory_threshold_high
        
        # Model recommendation
        if cpu_constrained or memory_constrained:
            recommended_model = "tiny"  # Use smaller model
            reason = "High resource usage"
        else:
            recommended_model = "large"  # Use larger model
            reason = "Adequate resources available"
        
        return {
            "cpu_percent": metrics.cpu_percent,
            "memory_percent": metrics.memory_percent,
            "memory_available_gb": metrics.memory_available_gb,
            "gpu_percent": metrics.gpu_percent,
            "cpu_constrained": cpu_constrained,
            "memory_constrained": memory_constrained,
            "recommended_model": recommended_model,
            "reason": reason,
            "timestamp": metrics.timestamp
        }
    
    def get_metrics_summary(self, window_seconds: int = 60) -> Dict[str, any]:
        """Get metrics summary over time window"""
        if not self.metrics_history:
            return {}
        
        cutoff_time = time.time() - window_seconds
        recent_metrics = [m for m in self.metrics_history if m.timestamp > cutoff_time]
        
        if not recent_metrics:
            return {}
        
        avg_cpu = sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_percent for m in recent_metrics) / len(recent_metrics)
        min_memory_gb = min(m.memory_available_gb for m in recent_metrics)
        
        return {
            "window_seconds": window_seconds,
            "sample_count": len(recent_metrics),
            "avg_cpu_percent": avg_cpu,
            "avg_memory_percent": avg_memory,
            "min_memory_available_gb": min_memory_gb,
            "cpu_peak": max(m.cpu_percent for m in recent_metrics),
            "memory_peak": max(m.memory_percent for m in recent_metrics)
        }

# Test the resource monitor
if __name__ == "__main__":
    print("💻 RESOURCE MONITOR TEST")
    print("=" * 40)
    
    monitor = ResourceMonitor(update_interval=1.0)
    
    # Test single measurement
    status = monitor.get_resource_status()
    print(f"📊 Current Status:")
    print(f"   CPU: {status['cpu_percent']:.1f}%")
    print(f"   Memory: {status['memory_percent']:.1f}% ({status['memory_available_gb']:.1f}GB available)")
    print(f"   Recommended Model: {status['recommended_model']}")
    print(f"   Reason: {status['reason']}")
    
    # Test monitoring for a few seconds
    print("\n🔄 Starting monitoring for 5 seconds...")
    monitor.start_monitoring()
    time.sleep(5)
    monitor.stop_monitoring()
    
    # Show summary
    summary = monitor.get_metrics_summary(window_seconds=5)
    if summary:
        print(f"\n📈 5-second Summary:")
        print(f"   Average CPU: {summary['avg_cpu_percent']:.1f}%")
        print(f"   Average Memory: {summary['avg_memory_percent']:.1f}%")
        print(f"   Minimum Available Memory: {summary['min_memory_available_gb']:.1f}GB")
    
    print("\n✅ Resource Monitor is working!")
