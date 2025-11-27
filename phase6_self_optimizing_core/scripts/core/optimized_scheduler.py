import time
from configured_manager import ConfiguredModelManager
from resource_monitor import ResourceMonitor

class MemoryOptimizedScheduler:
    """Scheduler optimized for your system's memory constraints"""
    
    def __init__(self):
        self.resource_monitor = ResourceMonitor()
        self.model_manager = ConfiguredModelManager()
        self.current_model = None
        
    def start_optimized(self):
        """Start optimized scheduling for your system"""
        print("🚀 STARTING MEMORY-OPTIMIZED SCHEDULER")
        print("=" * 50)
        
        # Start resource monitoring
        self.resource_monitor.start_monitoring()
        
        # Get current system status
        status = self.resource_monitor.get_resource_status()
        available_memory = self.model_manager.get_available_memory()
        
        print(f"📊 System Analysis:")
        print(f"   Available Memory: {available_memory:.1f}GB")
        print(f"   Memory Usage: {status['memory_percent']:.1f}%")
        print(f"   CPU Usage: {status['cpu_percent']:.1f}%")
        
        # Try to load TinyLlama if possible
        if self.model_manager.can_load_model("tinyllama"):
            print("🎯 Loading TinyLlama (optimal for current resources)...")
            if self.model_manager.load_model("tinyllama"):
                self.current_model = "tinyllama"
                print("✅ TinyLlama successfully loaded!")
                return True
            else:
                print("❌ Failed to load TinyLlama")
                return False
        else:
            print("⚠️  Insufficient memory for TinyLlama")
            print("💡 Recommendations:")
            print("   - Close memory-intensive applications")
            print("   - Consider adding more RAM")
            print("   - Use smaller quantized models")
            return False
    
    def get_smart_recommendation(self):
        """Get smart model recommendations based on system state"""
        status = self.resource_monitor.get_resource_status()
        available_memory = self.model_manager.get_available_memory()
        
        recommendations = {
            "current_memory_gb": available_memory,
            "memory_percent": status["memory_percent"],
            "recommendations": []
        }
        
        if available_memory >= 2.0:
            recommendations["recommendations"].append("✅ Load TinyLlama - sufficient memory")
        elif available_memory >= 1.0:
            recommendations["recommendations"].append("⚠️  Borderline - try loading TinyLlama but monitor closely")
        else:
            recommendations["recommendations"].append("❌ Insufficient memory - need at least 1.0GB free")
            
        return recommendations
    
    def generate_response(self, prompt: str) -> str:
        """Generate response using current model"""
        if not self.current_model:
            return "❌ No model loaded. Check system memory."
        
        print(f"🤖 Generating response with {self.current_model}...")
        return self.model_manager.generate_text(prompt)
    
    def system_report(self):
        """Generate comprehensive system report"""
        resource_status = self.resource_monitor.get_resource_status()
        manager_status = self.model_manager.get_status()
        
        print("\n📈 SYSTEM REPORT")
        print("=" * 40)
        print(f"🧠 Current Model: {self.current_model or 'None'}")
        print(f"💾 Available Memory: {manager_status['available_memory_gb']:.1f}GB")
        print(f"📊 Memory Usage: {resource_status['memory_percent']:.1f}%")
        print(f"🔥 CPU Usage: {resource_status['cpu_percent']:.1f}%")
        print(f"🎯 Recommended: {resource_status['recommended_model']}")
        
        # Smart recommendations
        smart_rec = self.get_smart_recommendation()
        print(f"💡 Recommendations: {smart_rec['recommendations'][0]}")

# Test the optimized system
if __name__ == "__main__":
    scheduler = MemoryOptimizedScheduler()
    
    if scheduler.start_optimized():
        # Test with a simple prompt
        print("\n🧪 TESTING INFERENCE")
        print("=" * 30)
        
        response = scheduler.generate_response("What is machine learning in simple terms?")
        print(f"🤖 Response: {response}")
        
        # Show system report
        scheduler.system_report()
        
        # Stop monitoring
        scheduler.resource_monitor.stop_monitoring()
    else:
        print("\n💡 SYSTEM OPTIMIZATION REQUIRED")
        print("Your Phase 6.0 system is ready but needs more memory to operate.")
        print("Current models available:")
        print("   - tinyllama: 1.1B parameter model (requires ~1.5GB)")
