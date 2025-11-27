import time
import numpy as np
import tensorflow as tf
import os

def test_advanced_optimization():
    print('ADVANCED KWS PERFORMANCE OPTIMIZATION')
    
    # Set environment for better performance
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Reduce TensorFlow logging
    
    # Try different optimization strategies
    strategies = [
        {'num_threads': 1, 'name': 'Single Thread'},
        {'num_threads': 2, 'name': 'Dual Thread'},
    ]
    
    best_latency = float('inf')
    best_strategy = None
    
    for strategy in strategies:
        print(f'Testing: {strategy['name']}')
        
        try:
            interpreter = tf.lite.Interpreter(
                model_path='phase1_baseline/models/production/model_int8.tflite',
                num_threads=strategy['num_threads']
            )
            interpreter.allocate_tensors()
            
            # Pre-allocate and warm-up
            input_details = interpreter.get_input_details()
            input_data = np.random.random(input_details[0]['shape']).astype('float32')
            
            for _ in range(10):
                interpreter.set_tensor(input_details[0]['index'], input_data)
                interpreter.invoke()
            
            # Benchmark
            times = []
            for i in range(50):
                interpreter.set_tensor(input_details[0]['index'], input_data)
                t0 = time.perf_counter()
                interpreter.invoke()
                t1 = time.perf_counter()
                times.append((t1 - t0) * 1000)
            
            avg_latency = np.mean(times)
            print(f'  {strategy['name']}: {avg_latency:.2f}ms')
            
            if avg_latency < best_latency:
                best_latency = avg_latency
                best_strategy = strategy['name']
                
        except Exception as e:
            print(f'  {strategy['name']} failed: {e}')
    
    print(f'BEST PERFORMANCE: {best_latency:.2f}ms ({best_strategy})')
    print(f'TARGET: ≤5ms | STATUS: {'MET' if best_latency <= 5 else 'NOT MET'}')
    return best_latency

if __name__ == '__main__':
    latency = test_advanced_optimization()
    if latency <= 5:
        print('SUCCESS: Performance target achieved!')
    else:
        print(f'PERFORMANCE GAP: {latency:.2f}ms above target')
