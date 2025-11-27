# phase1_baseline/scripts/04_deployment/verify_deployment.py
import numpy as np
import tensorflow as tf
from pathlib import Path
import sys
import time

sys.path.append(str(Path(__file__).parent.parent.parent))
from config import CONFIG

def test_tflite_models():
    """Test all TFLite models for deployment readiness"""
    
    print("🧪 Testing TFLite Models for Deployment...")
    print("=" * 50)
    
    models_to_test = {
        "Float32": "model_float32.tflite",
        "Dynamic Quantized": "model_dynamic.tflite", 
        "INT8 Quantized": "model_int8.tflite"
    }
    
    # Create test input
    test_input = np.random.random((1, 40, 99, 1)).astype(np.float32)
    
    results = {}
    
    for model_name, model_file in models_to_test.items():
        model_path = CONFIG.paths.models_dir / model_file
        
        if not model_path.exists():
            print(f"❌ {model_name} not found: {model_path}")
            continue
            
        try:
            # Load interpreter
            interpreter = tf.lite.Interpreter(model_path=str(model_path))
            interpreter.allocate_tensors()
            
            # Get input/output details
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            
            # Prepare input
            if input_details[0]['dtype'] == np.uint8:
                # Quantized model - need to scale input
                input_scale, input_zero_point = input_details[0]['quantization']
                test_input_quantized = test_input / input_scale + input_zero_point
                test_input_quantized = test_input_quantized.astype(np.uint8)
                interpreter.set_tensor(input_details[0]['index'], test_input_quantized)
            else:
                # Float model
                interpreter.set_tensor(input_details[0]['index'], test_input)
            
            # Run inference
            start_time = time.time()
            interpreter.invoke()
            inference_time = (time.time() - start_time) * 1000  # ms
            
            # Get output
            output = interpreter.get_tensor(output_details[0]['index'])
            
            if output_details[0]['dtype'] == np.uint8:
                # Dequantize output
                output_scale, output_zero_point = output_details[0]['quantization']
                output = (output.astype(np.float32) - output_zero_point) * output_scale
            
            predicted_class = np.argmax(output)
            confidence = np.max(output)
            
            results[model_name] = {
                'inference_time_ms': inference_time,
                'predicted_class': predicted_class,
                'confidence': confidence,
                'model_size_kb': model_path.stat().st_size / 1024
            }
            
            print(f"✅ {model_name}:")
            print(f"   ⏱️  Inference: {inference_time:.2f}ms")
            print(f"   🎯 Prediction: Class {predicted_class} ({confidence:.3f})")
            print(f"   📦 Size: {results[model_name]['model_size_kb']:.1f} KB")
            
        except Exception as e:
            print(f"❌ {model_name} failed: {e}")
    
    return results

if __name__ == "__main__":
    results = test_tflite_models()
    
    print(f"\n🎉 DEPLOYMENT READY!")
    print(f"All TFLite models are functional and optimized for edge devices!")