import psutil
import os

class FixedMemoryCalculator:
    """Correct memory calculation for your system"""
    
    @staticmethod
    def get_real_memory_info():
        """Get accurate memory information"""
        memory = psutil.virtual_memory()
        
        print("🧠 REAL MEMORY ANALYSIS")
        print("=" * 40)
        print(f"Total RAM: {memory.total / (1024**3):.1f} GB")
        print(f"Available: {memory.available / (1024**3):.1f} GB") 
        print(f"Used: {memory.used / (1024**3):.1f} GB")
        print(f"Percentage: {memory.percent}%")
        print(f"Free: {memory.free / (1024**3):.1f} GB")
        
        return {
            "total_gb": memory.total / (1024**3),
            "available_gb": memory.available / (1024**3),
            "used_gb": memory.used / (1024**3),
            "percent": memory.percent,
            "free_gb": memory.free / (1024**3)
        }

# Test the fixed calculator
if __name__ == "__main__":
    real_memory = FixedMemoryCalculator.get_real_memory_info()
    
    print(f"\n🎯 TINYLLAMA REQUIREMENT CHECK:")
    print(f"Model Size: 0.59 GB")
    print(f"Available Memory: {real_memory['available_gb']:.1f} GB")
    print(f"Can Load Model: {real_memory['available_gb'] >= 0.7}")  # 0.7GB buffer
