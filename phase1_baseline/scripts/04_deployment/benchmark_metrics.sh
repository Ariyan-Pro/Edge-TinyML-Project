#!/bin/bash
# Phase 2 Benchmark Automation Script
# Run on Raspberry Pi for performance measurement

echo "📊 Starting Edge AI Benchmark Suite"
echo "=========================================="

# Get system info
echo "🤖 System Information:"
echo "Model: $(cat /proc/device-tree/model | tr -d '\0')"
echo "CPU: $(lscpu | grep 'Model name' | cut -d: -f2 | xargs)"
echo "RAM: $(free -h | grep Mem | awk '{print $2}')"
echo "OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2 | tr -d '"')"

echo ""
echo "🔧 Performance Benchmarks:"
echo "------------------------------------------"

# Benchmark 1: Model loading time
echo "1. Model Loading Time:"
time python3 -c "
import tflite_runtime.interpreter as tflite
import time
start = time.time()
interpreter = tflite.Interpreter(model_path='../../models/model_int8.tflite')
interpreter.allocate_tensors()
load_time = (time.time() - start) * 1000
print(f'   Load time: {load_time:.2f} ms')
"

# Benchmark 2: Inference latency
echo ""
echo "2. Inference Latency (10 runs):"
python3 -c "
import tflite_runtime.interpreter as tflite
import numpy as np
import time

interpreter = tflite.Interpreter(model_path='../../models/model_int8.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()

# Create dummy input
dummy_input = np.random.random((1, 40, 99, 1)).astype(np.float32)

# Warm up
for _ in range(5):
    interpreter.set_tensor(input_details[0]['index'], dummy_input)
    interpreter.invoke()

# Benchmark
times = []
for _ in range(10):
    start = time.time()
    interpreter.set_tensor(input_details[0]['index'], dummy_input)
    interpreter.invoke()
    end = time.time()
    times.append((end - start) * 1000)

print(f'   Average: {np.mean(times):.2f} ms')
print(f'   Min: {np.min(times):.2f} ms')  
print(f'   Max: {np.max(times):.2f} ms')
print(f'   Std: {np.std(times):.2f} ms')
"

# Benchmark 3: System metrics
echo ""
echo "3. System Metrics:"
echo "   Temperature: $(vcgencmd measure_temp | cut -d= -f2)"
echo "   Voltage: $(vcgencmd measure_volts | cut -d= -f2)"
echo "   Clock: $(vcgencmd measure_clock arm | awk '{print \$2/1000000\" MHz\"}')"

# Benchmark 4: Memory usage
echo ""
echo "4. Memory Usage:"
python3 -c "
import resource
usage = resource.getrusage(resource.RUSAGE_SELF)
print(f'   Max RSS: {usage.ru_maxrss / 1024:.1f} MB')
"

echo ""
echo "✅ Benchmark completed!"