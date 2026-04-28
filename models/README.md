# KWS Model Files

## Generated Models

This directory contains the keyword spotting (KWS) model files for Edge-TinyML.

### Files

- `model_weights.npz` (920.1 KB) - Compressed NumPy weights
- `model_config.json` (0.4 KB) - Model configuration
- `lightweight_inference.py` (3.8 KB) - NumPy inference engine
- `model_float32.tflite` - Marker file (uses NumPy backend)
- `model_dynamic.tflite` - Marker file (uses NumPy backend)  
- `model_int8.tflite` - Marker file (uses NumPy backend)

### Specifications

- **Input Shape**: (40, 99, 1) - Mel spectrogram
- **Output Classes**: 10
- **Labels**: yes, no, up, down, left, right, on, off, stop, go
- **Architecture**: Two-layer neural network
- **Backend**: NumPy (TensorFlow-free)

### Usage

```python
from models.lightweight_inference import LightweightInference

engine = LightweightInference()
engine.allocate_tensors()

# Prepare input (mel spectrogram)
input_data = np.random.randn(1, 40, 99, 1).astype(np.float32)

# Run inference
engine.set_tensor(0, input_data)
engine.invoke()
output = engine.get_tensor(0)
```

### Integration with wake_word_detector.py

The detector will automatically use the NumPy backend when TensorFlow is unavailable.
No code changes required.

### Production Deployment

For production use with actual TFLite models:
1. Install TensorFlow: `pip install tensorflow`
2. Run `core_model_generator.py` to generate real TFLite files
3. The wake_word_detector.py will automatically detect and use them
