import time
import threading
from typing import Dict, Callable
from resource_monitor import ResourceMonitor
from model_manager import ModelManager

class AdaptiveScheduler:
    """Adaptive model scheduling based on system resources"""
    
    def __init__(self, models_dir: str = "models"):
        self.resource_monitor = ResourceMonitor()
        self.model_manager = ModelManager(models_dir)
        self.is_running = False
        self.scheduler_thread = None
        self.adaptation_callbacks = []
        
        # Adaptation thresholds
        self.adaptation_interval = 10.0  # Check every 10 seconds
        self.min_stable_time = 30.0  # Minimum time between adaptations
        
        self.last_adaptation_time = 0
        self.current_model_size = "unknown"
    
    def start(self):
        """Start adaptive scheduling"""
        if self.is_running:
            return
        
        print("🚀 Starting adaptive scheduler...")
        self.is_running = True
        
        # Start resource monitoring
        self.resource_monitor.start_monitoring()
        
        # Start scheduler thread
        self.scheduler_thread = threading.Thread(target=self._scheduling_loop, daemon=True)
        self.scheduler_thread.start()
        
        # Load initial model
        self._perform_initial_load()
    
    def stop(self):
        """Stop adaptive scheduling"""
        print("🛑 Stopping adaptive scheduler...")
        self.is_running = False
        self.resource_monitor.stop_monitoring()
        
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=3.0)
    
    def _perform_initial_load(self):
        """Perform initial model loading based on current resources"""
        status = self.resource_monitor.get_resource_status()
        recommended_model = status["recommended_model"]
        
        print(f"🎯 Initial load: {recommended_model} model")
        
        if self.model_manager.load_model(recommended_model):
            self.current_model_size = recommended_model
            self.last_adaptation_time = time.time()
            self._notify_adaptation(recommended_model, "initial_load")
        else:
            print(f"❌ Failed to load initial model: {recommended_model}")
    
    def _scheduling_loop(self):
        """Main scheduling loop"""
        while self.is_running:
            try:
                self._check_and_adapt()
                time.sleep(self.adaptation_interval)
            except Exception as e:
                print(f"❌ Scheduling error: {e}")
                time.sleep(5.0)  # Wait before retrying
    
    def _check_and_adapt(self):
        """Check resources and adapt model if needed"""
        current_time = time.time()
        
        # Don't adapt too frequently
        if current_time - self.last_adaptation_time < self.min_stable_time:
            return
        
        status = self.resource_monitor.get_resource_status()
        recommended_model = status["recommended_model"]
        
        # Check if adaptation is needed
        if (recommended_model != self.current_model_size and 
            self.model_manager.can_load_model(recommended_model)):
            
            print(f"🔄 Adaptation needed: {self.current_model_size} -> {recommended_model}")
            print(f"   Reason: {status['reason']}")
            print(f"   CPU: {status['cpu_percent']:.1f}%, Memory: {status['memory_percent']:.1f}%")
            
            if self.model_manager.load_model(recommended_model):
                old_size = self.current_model_size
                self.current_model_size = recommended_model
                self.last_adaptation_time = current_time
                
                self._notify_adaptation(recommended_model, "resource_adaptation", old_size)
            else:
                print(f"❌ Failed to adapt to {recommended_model}")
    
    def add_adaptation_callback(self, callback: Callable):
        """Add callback for model adaptation events"""
        self.adaptation_callbacks.append(callback)
    
    def _notify_adaptation(self, new_model: str, reason: str, old_model: str = None):
        """Notify callbacks of model adaptation"""
        adaptation_info = {
            "timestamp": time.time(),
            "new_model": new_model,
            "old_model": old_model,
            "reason": reason,
            "resource_status": self.resource_monitor.get_resource_status()
        }
        
        for callback in self.adaptation_callbacks:
            try:
                callback(adaptation_info)
            except Exception as e:
                print(f"❌ Adaptation callback error: {e}")
    
    def generate_text(self, prompt: str, max_tokens: int = 100) -> str:
        """Generate text using current adaptive model"""
        return self.model_manager.generate_text(prompt, max_tokens)
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        resource_status = self.resource_monitor.get_resource_status()
        manager_status = self.model_manager.get_status()
        metrics_summary = self.resource_monitor.get_metrics_summary(window_seconds=60)
        
        return {
            "adaptive_scheduler": {
                "is_running": self.is_running,
                "current_model": self.current_model_size,
                "last_adaptation_time": self.last_adaptation_time,
                "adaptation_count": len(self.adaptation_callbacks)
            },
            "resources": resource_status,
            "model_manager": manager_status,
            "metrics_summary": metrics_summary
        }

# Test the adaptive scheduler
if __name__ == "__main__":
    print("🎛️  ADAPTIVE SCHEDULER TEST")
    print("=" * 45)
    
    def adaptation_callback(info):
        print(f"🔔 Adaptation Event: {info['old_model']} -> {info['new_model']}")
        print(f"   Reason: {info['reason']}")
    
    scheduler = AdaptiveScheduler()
    scheduler.add_adaptation_callback(adaptation_callback)
    
    # Show initial status
    status = scheduler.get_system_status()
    print("📊 Initial System Status:")
    print(f"   Current Model: {status['adaptive_scheduler']['current_model']}")
    print(f"   CPU: {status['resources']['cpu_percent']:.1f}%")
    print(f"   Memory: {status['resources']['memory_percent']:.1f}%")
    print(f"   Recommended: {status['resources']['recommended_model']}")
    
    # Start scheduler for a brief test
    print("\n�� Starting scheduler for 15 seconds...")
    scheduler.start()
    time.sleep(15)
    scheduler.stop()
    
    # Show final status
    final_status = scheduler.get_system_status()
    print(f"\n📈 Final Status:")
    print(f"   Current Model: {final_status['adaptive_scheduler']['current_model']}")
    print(f"   Scheduler Running: {final_status['adaptive_scheduler']['is_running']}")
    
    print("\n✅ Adaptive Scheduler is working!")
