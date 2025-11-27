import tensorflow as tf
import time
import os

class OptimizedKWS:
    def __init__(self, model_path):
        # Set thread configuration before loading
        os.environ['TF_NUM_INTEROP_THREADS'] = '1'
        os.environ['TF_NUM_INTRAOP_THREADS'] = '1'
        
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        # Warm-up
        input_shape = self.input_details[0]['shape']
        dummy_input = tf.random.normal(input_shape, dtype=tf.float32)
        self.infer(dummy_input)
    
    def infer(self, input_data):
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        start_time = time.perf_counter()
        self.interpreter.invoke()
        end_time = time.perf_counter()
        output = self.interpreter.get_tensor(self.output_details[0]['index'])
        return output, (end_time - start_time) * 1000

# Benchmark optimized version
optimized_kws = OptimizedKWS('phase1_baseline/models/production/model_int8.tflite')
input_shape = optimized_kws.input_details[0]['shape']
test_input = tf.random.normal(input_shape, dtype=tf.float32)

latencies = []
for _ in range(100):
    _, latency = optimized_kws.infer(test_input)
    latencies.append(latency)

print(f"Optimized KWS Performance: {sum(latencies)/len(latencies):.2f}ms")
print(f"Best: {min(latencies):.2f}ms, Worst: {max(latencies):.2f}ms")
