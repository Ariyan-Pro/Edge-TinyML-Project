import time
import json
import statistics
from typing import List, Dict
from model_manager import ModelManager

class BenchmarkTool:
    """Performance benchmarking for model comparison"""
    
    def __init__(self, models_dir: str = "models"):
        self.model_manager = ModelManager(models_dir)
        self.benchmark_results = {}
    
    def benchmark_model(self, model_name: str, test_prompts: List[str], 
                       iterations: int = 3) -> Dict:
        """Benchmark a specific model"""
        if not self.model_manager.load_model(model_name):
            return {"error": f"Failed to load model: {model_name}"}
        
        print(f"🧪 Benchmarking {model_name}...")
        
        results = {
            "model": model_name,
            "timestamp": time.time(),
            "iterations": iterations,
            "prompt_count": len(test_prompts),
            "load_time": self.model_manager.model_metrics.get(model_name, {}).get("load_time", 0),
            "inference_times": [],
            "tokens_per_second": [],
            "memory_usage_mb": []
        }
        
        for i in range(iterations):
            iteration_times = []
            
            for prompt in test_prompts:
                start_time = time.time()
                
                # Generate response
                response = self.model_manager.generate_text(prompt, max_tokens=50)
                
                inference_time = time.time() - start_time
                iteration_times.append(inference_time)
                
                # Estimate tokens per second (rough approximation)
                if len(response) > 0:
                    tokens_approx = len(response.split())  # Rough token count
                    tps = tokens_approx / inference_time if inference_time > 0 else 0
                    results["tokens_per_second"].append(tps)
            
            results["inference_times"].extend(iteration_times)
        
        # Calculate statistics
        if results["inference_times"]:
            results["avg_inference_time"] = statistics.mean(results["inference_times"])
            results["min_inference_time"] = min(results["inference_times"])
            results["max_inference_time"] = max(results["inference_times"])
            results["std_inference_time"] = statistics.stdev(results["inference_times"]) if len(results["inference_times"]) > 1 else 0
        
        if results["tokens_per_second"]:
            results["avg_tokens_per_second"] = statistics.mean(results["tokens_per_second"])
            results["min_tokens_per_second"] = min(results["tokens_per_second"])
            results["max_tokens_per_second"] = max(results["tokens_per_second"])
        
        self.benchmark_results[model_name] = results
        return results
    
    def compare_models(self, model_names: List[str], test_prompts: List[str] = None) -> Dict:
        """Compare multiple models"""
        if test_prompts is None:
            test_prompts = [
                "Explain artificial intelligence in one sentence.",
                "What is the capital of France?",
                "Calculate 15 * 8 + 3.",
                "Tell me a short joke."
            ]
        
        comparison = {
            "timestamp": time.time(),
            "test_prompts": test_prompts,
            "models_compared": model_names,
            "results": {}
        }
        
        for model_name in model_names:
            print(f"\n📊 Comparing {model_name}...")
            result = self.benchmark_model(model_name, test_prompts)
            comparison["results"][model_name] = result
        
        # Determine best model based on performance
        comparison["recommendations"] = self._generate_recommendations(comparison)
        
        return comparison
    
    def _generate_recommendations(self, comparison: Dict) -> Dict:
        """Generate model recommendations based on benchmark results"""
        models_data = comparison["results"]
        recommendations = {}
        
        # Find fastest model
        fastest_model = None
        fastest_time = float('inf')
        
        # Find most efficient model (tokens per second)
        most_efficient = None
        best_efficiency = 0
        
        for model_name, data in models_data.items():
            if "avg_inference_time" in data and data["avg_inference_time"] < fastest_time:
                fastest_time = data["avg_inference_time"]
                fastest_model = model_name
            
            if "avg_tokens_per_second" in data and data["avg_tokens_per_second"] > best_efficiency:
                best_efficiency = data["avg_tokens_per_second"]
                most_efficient = model_name
        
        recommendations["fastest_model"] = fastest_model
        recommendations["most_efficient_model"] = most_efficient
        recommendations["fastest_inference_time"] = fastest_time
        recommendations["best_efficiency"] = best_efficiency
        
        return recommendations
    
    def save_benchmark_results(self, filename: str = "benchmark_results.json"):
        """Save benchmark results to file"""
        with open(filename, 'w') as f:
            json.dump(self.benchmark_results, f, indent=2)
        print(f"💾 Saved benchmark results to {filename}")
    
    def load_benchmark_results(self, filename: str = "benchmark_results.json"):
        """Load benchmark results from file"""
        try:
            with open(filename, 'r') as f:
                self.benchmark_results = json.load(f)
            print(f"📂 Loaded benchmark results from {filename}")
        except FileNotFoundError:
            print(f"❌ Benchmark results file not found: {filename}")

# Test the benchmark tool
if __name__ == "__main__":
    print("📊 BENCHMARK TOOL TEST")
    print("=" * 40)
    
    benchmark = BenchmarkTool()
    
    # Test prompts
    test_prompts = [
        "What is machine learning?",
        "Explain neural networks briefly.",
        "What are the benefits of AI?"
    ]
    
    # Note: This will use mock models since we don't have actual GGUF files
    print("🔍 Note: Using mock models for demonstration")
    print("💡 Actual benchmarking requires GGUF model files")
    
    # Show available models from manager
    status = benchmark.model_manager.get_status()
    print(f"\n📚 Available models: {status['loaded_models']}")
    
    # Test with mock models
    try:
        # This would normally benchmark real models
        print("\n🧪 Running mock benchmark...")
        
        # Create mock results for demonstration
        mock_results = {
            "tiny": {
                "model": "tiny",
                "avg_inference_time": 0.15,
                "avg_tokens_per_second": 45.2,
                "load_time": 1.2
            },
            "large": {
                "model": "large", 
                "avg_inference_time": 0.8,
                "avg_tokens_per_second": 28.7,
                "load_time": 8.5
            }
        }
        
        print("📈 Mock Benchmark Results:")
        for model, results in mock_results.items():
            print(f"\n   {model.upper()} Model:")
            print(f"     Avg Inference Time: {results['avg_inference_time']:.2f}s")
            print(f"     Tokens/Second: {results['avg_tokens_per_second']:.1f}")
            print(f"     Load Time: {results['load_time']:.1f}s")
        
        print("\n✅ Benchmark Tool is ready!")
        print("💡 To use with real models, add GGUF files to the models directory")
        
    except Exception as e:
        print(f"❌ Benchmark test failed: {e}")
