import tensorflow as tf
import time
import numpy as np

def benchmark_windows_optimized():
    # Load model once
    interpreter = tf.lite.Interpreter(model_path='phase1_baseline/models/production/model_int8.tflite')
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    print(f"Model Input Details: {input_details[0]['dtype']}")
    print(f"Model Input Shape: {input_details[0]['shape']}")
    
    # Get correct input shape and type
    input_shape = input_details[0]['shape']
    input_dtype = input_details[0]['dtype']
    
    latencies = []
    
    for i in range(100):
        # Create input with CORRECT data type (UINT8 for INT8 quantized model)
        if input_dtype == np.uint8:
            test_input = np.random.randint(0, 255, input_shape, dtype=np.uint8)
        else:
            test_input = np.random.random(input_shape).astype(input_dtype)
        
        start_time = time.perf_counter()
        interpreter.set_tensor(input_details[0]['index'], test_input)
        interpreter.invoke()
        end_time = time.perf_counter()
        
        latency = (end_time - start_time) * 1000
        latencies.append(latency)
    
    print(f"Windows Optimized Performance:")
    print(f"Average: {np.mean(latencies):.2f}ms")
    print(f"Best: {np.min(latencies):.2f}ms") 
    print(f"Worst: {np.max(latencies):.2f}ms")
    print(f"P95: {np.percentile(latencies, 95):.2f}ms")
    print(f"Std Dev: {np.std(latencies):.2f}ms")

if __name__ == "__main__":
    benchmark_windows_optimized()
