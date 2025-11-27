# Raspberry Pi Deployment Instructions

## 📋 Pre-Deployment Checklist

### Files Ready for Transfer:
- ✅ `real_time_infer.py` - Real-time inference script
- ✅ `benchmark_metrics.sh` - Performance benchmarking  
- ✅ `power_monitor.py` - Power consumption monitoring
- ✅ `models/model_int8.tflite` - Optimized model (76KB)
- ✅ `models/model_dynamic.tflite` - Balanced model (74KB)
- ✅ `models/model_float32.tflite` - Reference model (262KB)

## 🚀 Deployment Steps

### 1. Transfer Files to Raspberry Pi
```bash
# From your Windows machine, transfer the entire project:
scp -r C:\Users\dell\Projects\Edge-TinyML-Project\pi@raspberrypi.local:/home/pi/