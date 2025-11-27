# real_performance_benchmark.py
import time
import numpy as np
import sys
from pathlib import Path

def benchmark_real_models():
    print("🚀 REAL PERFORMANCE BENCHMARK")
    print("=" * 50)
    
    # Your actual model paths
    models = {
        'Float32': '../../models/development/model_float32.tflite',
        'Dynamic': '../../models/development/model_dynamic.tflite', 
        'INT8': '../../models/production/model_int8.tflite'
    }
    
    try:
        import tensorflow as tf
        
        results = []
        for name, path in models.items():
            model_path = Path(path)
            if model_path.exists():
                # Load model
                interpreter = tf.lite.Interpreter(model_path=str(model_path))
                interpreter.allocate_tensors()
                input_details = interpreter.get_input_details()
                
                # Create test input matching your model shape (1, 40, 99, 1)
                input_shape = input_details[0]['shape']
                dummy_input = np.random.random(input_shape).astype(np.float32)
                
                # Handle quantization for INT8
                if input_details[0]['dtype'] == np.uint8:
                    input_scale, input_zero_point = input_details[0]['quantization']
                    dummy_input = dummy_input / input_scale + input_zero_point
                    dummy_input = dummy_input.astype(np.uint8)
                
                # Warm up
                for _ in range(5):
                    interpreter.set_tensor(input_details[0]['index'], dummy_input)
                    interpreter.invoke()
                
                # Benchmark
                times = []
                for _ in range(100):
                    interpreter.set_tensor(input_details[0]['index'], dummy_input)
                    start_time = time.time()
                    interpreter.invoke()
                    end_time = time.time()
                    times.append((end_time - start_time) * 1000)  # ms
                
                avg_time = np.mean(times)
                model_size = model_path.stat().st_size / 1024  # KB
                
                print(f"📊 {name:12} | {model_size:6.1f} KB | {avg_time:7.2f} ms | {len(times):3} runs")
                results.append((name, model_size, avg_time))
                
            else:
                print(f"❌ {name} model not found: {path}")
        
        print("\n" + "=" * 50)
        print("🎯 PERFORMANCE SUMMARY")
        print("=" * 50)
        
        # Find best model
        if results:
            best_model = min(results, key=lambda x: x[2])
            print(f"🏆 BEST MODEL: {best_model[0]}")
            print(f"   Speed: {best_model[2]:.2f} ms")
            print(f"   Size: {best_model[1]:.1f} KB")
            
        return results
        
    except ImportError:
        print("❌ TensorFlow not available")
        return []

if __name__ == "__main__":
    benchmark_real_models()