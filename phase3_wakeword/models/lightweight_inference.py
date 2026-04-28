#!/usr/bin/env python3
"""
Lightweight Inference Engine - NumPy-only KWS inference
Drop-in replacement for TFLite when TensorFlow is not available
"""

import numpy as np
from pathlib import Path
import json

class LightweightInference:
    """NumPy-based inference engine for KWS model"""
    
    def __init__(self, model_dir=None):
        if model_dir is None:
            model_dir = Path(__file__).parent.parent / "models"
        
        self.model_dir = Path(model_dir)
        self.weights = None
        self.config = None
        self.input_details = []
        self.output_details = []
        
        self.load_model()
    
    def load_model(self):
        """Load model weights and config"""
        weights_path = self.model_dir / "model_weights.npz"
        config_path = self.model_dir / "model_config.json"
        
        if not weights_path.exists():
            raise FileNotFoundError(f"Weights not found: {weights_path}")
        
        # Load weights
        data = np.load(weights_path)
        self.W1 = data['W1']
        self.b1 = data['b1']
        self.W2 = data['W2']
        self.b2 = data['b2']
        
        # Load config
        with open(config_path) as f:
            self.config = json.load(f)
        
        # Mock TFLite interface
        self.input_details = [{
            'index': 0,
            'shape': [1, 40, 99, 1],
            'dtype': np.uint8,
            'quantization': (0.007874015748031496, 0)  # Scale, zero_point
        }]
        
        self.output_details = [{
            'index': 1,
            'shape': [1, 10],
            'dtype': np.uint8,
            'quantization': (0.00390625, 0)
        }]
        
        print(f"✅ Model loaded from {self.model_dir}")
    
    def allocate_tensors(self):
        """Mock TFLite method"""
        pass
    
    def get_input_details(self):
        return self.input_details
    
    def get_output_details(self):
        return self.output_details
    
    def set_tensor(self, index, data):
        """Set input tensor"""
        self._input_data = data
    
    def invoke(self):
        """Run inference"""
        # Dequantize input if needed
        if self._input_data.dtype == np.uint8:
            scale, zero_point = self.input_details[0]['quantization']
            x = (self._input_data.astype(np.float32) - zero_point) * scale
        else:
            x = self._input_data.astype(np.float32)
        
        # Flatten for fully connected layers
        batch_size = x.shape[0]
        x = x.reshape(batch_size, -1)
        
        # Forward pass
        h = np.maximum(x @ self.W1 + self.b1, 0)  # ReLU
        out = h @ self.W2 + self.b2
        
        # Softmax
        exp_out = np.exp(out - out.max(axis=1, keepdims=True))
        self._output_data = exp_out / exp_out.sum(axis=1, keepdims=True)
    
    def get_tensor(self, index):
        """Get output tensor"""
        # Quantize output if needed
        scale, zero_point = self.output_details[0]['quantization']
        out_quant = np.round(self._output_data / scale + zero_point).astype(np.uint8)
        return out_quant


# Compatibility wrapper
class TFLiteInterpreterWrapper:
    """Wraps LightweightInference to match TFLite Interpreter API"""
    
    def __init__(self, model_path):
        model_dir = Path(model_path).parent
        self.engine = LightweightInference(model_dir)
    
    def allocate_tensors(self):
        self.engine.allocate_tensors()
    
    def get_input_details(self):
        return self.engine.get_input_details()
    
    def get_output_details(self):
        return self.engine.get_output_details()
    
    def set_tensor(self, index, data):
        self.engine.set_tensor(index, data)
    
    def invoke(self):
        self.engine.invoke()
    
    def get_tensor(self, index):
        return self.engine.get_tensor(index)
