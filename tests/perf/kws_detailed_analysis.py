import time
import numpy as np
import tensorflow as tf

def analyze_kws_performance():
    print('🔍 DETAILED KWS PERFORMANCE ANALYSIS')
    
    # Load model
    interpreter = tf.lite.Interpreter(model_path='phase1_baseline/models/production/model_int8.tflite')
    interpreter.allocate_tensors()
    
    # Warm-up runs
    print('🔥 Warming up...')
    for _ in range(10):
        fake_input = np.random.random((1, 49, 40, 1)).astype('float32')
        interpreter.invoke()
    
    # Detailed timing
    times = []
    print('⏱️  Benchmarking...')
    for i in range(100):
        fake_input = np.random.random((1, 49, 40, 1)).astype('float32')
        
        # Time just the inference
        t0 = time.perf_counter()
        interpreter.invoke()
        t1 = time.perf_counter()
        
        latency = (t1 - t0) * 1000
        times.append(latency)
    
    # Analysis
    avg_latency = np.mean(times)
    min_latency = np.min(times)
    max_latency = np.max(times)
    std_latency = np.std(times)
    
    print(f'📊 Performance Analysis:')
    print(f'   Average: {avg_latency:.2f}ms')
    print(f'   Minimum: {min_latency:.2f}ms')
    print(f'   Maximum: {max_latency:.2f}ms') 
    print(f'   Std Dev: {std_latency:.2f}ms')
    print(f'   Target:  ≤5ms')
    print(f'   Status:  {"✅ WITHIN TARGET" if avg_latency <= 5 else "❌ NEEDS OPTIMIZATION"}')
    
    # Check if we can optimize
    if avg_latency > 5:
        print(f'🚨 PERFORMANCE ISSUE: Current {avg_latency:.2f}ms vs Target 5ms')
        print(f'💡 Recommendations:')
        print(f'   - Use tflite_runtime instead of full TensorFlow')
        print(f'   - Check CPU affinity and background processes')
        print(f'   - Consider model quantization improvements')
    
    return avg_latency

if __name__ == '__main__':
    latency = analyze_kws_performance()
    if latency <= 5:
        print(f'🚀 KWS PERFORMANCE: OPTIMAL - {latency:.2f}ms')
    else:
        print(f'⚠️ KWS PERFORMANCE: SUBOPTIMAL - {latency:.2f}ms (Target: ≤5ms)')
