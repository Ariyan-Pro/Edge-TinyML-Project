import os
import psutil
from model_manager import ModelManager, ModelConfig

class ConfiguredModelManager(ModelManager):
    """Model Manager configured for your existing TinyLlama model"""
    
    def _load_model_configs(self):
        """Load configurations for your existing models"""
        
        # Use your actual TinyLlama model path
        tinyllama_path = os.path.join(self.models_dir, "tinyllama-1.1b-chat-v1.0.Q4_0.gguf")
        
        self.model_configs = {
            "tinyllama": ModelConfig(
                name="tinyllama",
                file_path=tinyllama_path,
                model_type="tiny", 
                context_size=2048,
                estimated_memory_gb=1.5,  # Adjusted for Q4 quantization
                priority=2
            )
        }
        
        print(f"📚 Loaded {len(self.model_configs)} model configuration(s)")
        print(f"🔍 Found model: {tinyllama_path}")
        print(f"   Size: {os.path.getsize(tinyllama_path) / (1024**3):.2f} GB")
        print(f"   Exists: {os.path.exists(tinyllama_path)}")

# Test with your actual model
if __name__ == "__main__":
    print("🧠 CONFIGURED MODEL MANAGER TEST")
    print("=" * 45)
    
    manager = ConfiguredModelManager()
    
    # Show available memory
    available_memory = manager.get_available_memory()
    print(f"💾 Available Memory: {available_memory:.1f}GB")
    
    # Check if we can load TinyLlama
    can_load = manager.can_load_model("tinyllama")
    print(f"📦 Can Load TinyLlama: {can_load}")
    
    if can_load:
        print("�� Attempting to load TinyLlama...")
        success = manager.load_model("tinyllama")
        if success:
            print("✅ TinyLlama loaded successfully!")
            
            # Test inference
            print("\n🧪 Testing inference...")
            response = manager.generate_text("Hello! How are you today?")
            print(f"🤖 Model Response: {response}")
        else:
            print("❌ Failed to load TinyLlama")
    else:
        print("💡 Not enough memory to load TinyLlama")
        print("   Consider closing other applications to free up memory")
