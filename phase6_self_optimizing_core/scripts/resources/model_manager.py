import os
import time
import json
from typing import Dict, Optional, List
from dataclasses import dataclass
import psutil

try:
    from llama_cpp import Llama
except ImportError:
    print("⚠️  llama-cpp-python not available, using mock implementation")
    # Mock implementation for testing
    class Llama:
        def __init__(self, model_path, **kwargs):
            self.model_path = model_path
            self.n_ctx = kwargs.get('n_ctx', 512)
            print(f"Mock: Loading model {model_path}")
        
        def create_chat_completion(self, messages, **kwargs):
            return {"choices": [{"message": {"content": f"Mock response from {self.model_path}"}}]}

@dataclass
class ModelConfig:
    name: str
    file_path: str
    model_type: str  # 'tiny', 'medium', 'large'
    context_size: int
    estimated_memory_gb: float
    priority: int  # Higher priority = better quality

class ModelManager:
    """Dynamic model loading and management"""
    
    def __init__(self, models_dir: str = "models", cache_dir: str = "cache"):
        self.models_dir = models_dir
        self.cache_dir = cache_dir
        self.loaded_models: Dict[str, Llama] = {}
        self.model_configs: Dict[str, ModelConfig] = {}
        self.current_model: Optional[str] = None
        self.model_metrics: Dict[str, Dict] = {}
        
        # Create directories if they don't exist
        os.makedirs(models_dir, exist_ok=True)
        os.makedirs(cache_dir, exist_ok=True)
        
        # Load model configurations
        self._load_model_configs()
    
    def _load_model_configs(self):
        """Load or create model configurations"""
        # This would typically load from a config file
        # For now, define some example configurations
        
        self.model_configs = {
            "tiny": ModelConfig(
                name="tiny",
                file_path=os.path.join(self.models_dir, "tiny_model.gguf"),
                model_type="tiny",
                context_size=2048,
                estimated_memory_gb=1.0,
                priority=1
            ),
            "large": ModelConfig(
                name="large", 
                file_path=os.path.join(self.models_dir, "large_model.gguf"),
                model_type="large",
                context_size=8192,
                estimated_memory_gb=8.0,
                priority=3
            )
        }
        
        print(f"�� Loaded {len(self.model_configs)} model configurations")
    
    def load_model(self, model_name: str) -> bool:
        """Load a specific model"""
        if model_name not in self.model_configs:
            print(f"❌ Unknown model: {model_name}")
            return False
        
        config = self.model_configs[model_name]
        
        # Check if model file exists
        if not os.path.exists(config.file_path):
            print(f"❌ Model file not found: {config.file_path}")
            print("💡 Please download model files to the models directory")
            return False
        
        try:
            # Unload current model if different
            if self.current_model and self.current_model != model_name:
                self.unload_model(self.current_model)
            
            print(f"🔄 Loading model: {model_name}")
            start_time = time.time()
            
            # Load the model
            model = Llama(
                model_path=config.file_path,
                n_ctx=config.context_size,
                verbose=False
            )
            
            load_time = time.time() - start_time
            
            self.loaded_models[model_name] = model
            self.current_model = model_name
            
            # Record metrics
            self.model_metrics[model_name] = {
                "load_time": load_time,
                "last_loaded": time.time(),
                "inference_count": 0
            }
            
            print(f"✅ Loaded {model_name} in {load_time:.2f}s")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load model {model_name}: {e}")
            return False
    
    def unload_model(self, model_name: str):
        """Unload a model to free memory"""
        if model_name in self.loaded_models:
            del self.loaded_models[model_name]
            print(f"✅ Unloaded model: {model_name}")
            
            if self.current_model == model_name:
                self.current_model = None
    
    def get_available_memory(self) -> float:
        """Get available system memory in GB"""
        memory = psutil.virtual_memory()
        return memory.available / (1024 ** 3)  # Convert to GB
    
    def can_load_model(self, model_name: str) -> bool:
        """Check if there's enough memory to load a model"""
        if model_name not in self.model_configs:
            return False
        
        config = self.model_configs[model_name]
        available_memory = self.get_available_memory()
        
        # Add some buffer for system operations
        required_memory = config.estimated_memory_gb * 1.2
        
        return available_memory >= required_memory
    
    def get_recommended_model(self, available_memory_gb: float) -> str:
        """Get the best model that fits available memory"""
        best_model = "tiny"  # Default fallback
        best_priority = -1
        
        for name, config in self.model_configs.items():
            required_memory = config.estimated_memory_gb * 1.2
            
            if (available_memory_gb >= required_memory and 
                config.priority > best_priority):
                best_model = name
                best_priority = config.priority
        
        return best_model
    
    def generate_text(self, prompt: str, max_tokens: int = 100) -> str:
        """Generate text using current model"""
        if not self.current_model:
            print("❌ No model loaded")
            return "Error: No model loaded"
        
        try:
            model = self.loaded_models[self.current_model]
            
            # Record inference start
            start_time = time.time()
            
            # Generate response
            response = model.create_chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            inference_time = time.time() - start_time
            
            # Update metrics
            if self.current_model in self.model_metrics:
                self.model_metrics[self.current_model]["inference_count"] += 1
                self.model_metrics[self.current_model]["last_inference_time"] = inference_time
            
            content = response["choices"][0]["message"]["content"]
            return content
            
        except Exception as e:
            print(f"❌ Inference error: {e}")
            return f"Error: {e}"
    
    def get_status(self) -> Dict:
        """Get current manager status"""
        available_memory = self.get_available_memory()
        recommended_model = self.get_recommended_model(available_memory)
        
        return {
            "current_model": self.current_model,
            "available_memory_gb": available_memory,
            "recommended_model": recommended_model,
            "loaded_models": list(self.loaded_models.keys()),
            "can_load_recommended": self.can_load_model(recommended_model)
        }

# Test the model manager
if __name__ == "__main__":
    print("🧠 MODEL MANAGER TEST")
    print("=" * 40)
    
    manager = ModelManager()
    
    # Show available memory
    available_memory = manager.get_available_memory()
    recommended = manager.get_recommended_model(available_memory)
    
    print(f"💾 Available Memory: {available_memory:.1f}GB")
    print(f"🎯 Recommended Model: {recommended}")
    print(f"📦 Can Load Recommended: {manager.can_load_model(recommended)}")
    
    # Show status
    status = manager.get_status()
    print(f"\n�� Manager Status:")
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n✅ Model Manager is ready!")
    print("💡 Note: Actual model loading requires GGUF model files in the models directory")
