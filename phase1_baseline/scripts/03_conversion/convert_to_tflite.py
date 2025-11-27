# phase1_baseline/scripts/03_conversion/convert_to_tflite.py
import tensorflow as tf
import numpy as np
from pathlib import Path
import argparse
import logging
import sys
import json

sys.path.append(str(Path(__file__).parent.parent.parent))
from config import CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TFLiteConverter:
    """Convert trained model to TFLite for edge deployment"""
    
    def __init__(self):
        self.conversion_results = {}
    
    def load_representative_data(self, npy_dir: Path, num_samples=100):
        """Load sample data for quantization calibration"""
        npy_files = list(npy_dir.rglob("*.npy"))
        selected_files = npy_files[:num_samples]
        
        def representative_dataset():
            for file_path in selected_files:
                try:
                    data = np.load(file_path, allow_pickle=True)
                    data = data.astype(np.float32)
                    data = data[np.newaxis, ..., np.newaxis]  # Add batch and channel dims
                    yield [data]
                except Exception as e:
                    logger.warning(f"Failed to load {file_path}: {e}")
                    continue
        
        return representative_dataset
    
    def convert_model(self, keras_model_path: Path, representative_data_dir: Path = None):
        """Convert Keras model to various TFLite formats"""
        
        logger.info("Starting TFLite Conversion")
        
        # Load the trained model
        model = tf.keras.models.load_model(keras_model_path)
        logger.info(f"Loaded model: {keras_model_path.name}")
        
        conversion_results = {}
        
        # 1. Float32 TFLite (baseline)
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        tflite_float32 = converter.convert()
        
        float32_path = CONFIG.paths.models_dir / "model_float32.tflite"
        with open(float32_path, 'wb') as f:
            f.write(tflite_float32)
        
        float32_size = float32_path.stat().st_size / 1024  # KB
        conversion_results['float32'] = {
            'size_kb': float32_size,
            'path': str(float32_path)
        }
        logger.info(f"Float32 model: {float32_size:.1f} KB")
        
        # 2. Dynamic range quantization (smaller, faster)
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        tflite_dynamic = converter.convert()
        
        dynamic_path = CONFIG.paths.models_dir / "model_dynamic.tflite"
        with open(dynamic_path, 'wb') as f:
            f.write(tflite_dynamic)
        
        dynamic_size = dynamic_path.stat().st_size / 1024
        conversion_results['dynamic'] = {
            'size_kb': dynamic_size,
            'path': str(dynamic_path)
        }
        logger.info(f"Dynamic quantized: {dynamic_size:.1f} KB")
        
        # 3. Full INT8 quantization (smallest, requires calibration)
        if representative_data_dir:
            try:
                converter = tf.lite.TFLiteConverter.from_keras_model(model)
                converter.optimizations = [tf.lite.Optimize.DEFAULT]
                converter.representative_dataset = self.load_representative_data(representative_data_dir)
                converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
                converter.inference_input_type = tf.uint8
                converter.inference_output_type = tf.uint8
                
                tflite_int8 = converter.convert()
                
                int8_path = CONFIG.paths.models_dir / "model_int8.tflite"
                with open(int8_path, 'wb') as f:
                    f.write(tflite_int8)
                
                int8_size = int8_path.stat().st_size / 1024
                conversion_results['int8'] = {
                    'size_kb': int8_size,
                    'path': str(int8_path)
                }
                logger.info(f"INT8 quantized: {int8_size:.1f} KB")
                
            except Exception as e:
                logger.warning(f"INT8 quantization failed: {e}")
        
        # Save conversion report
        report_path = CONFIG.paths.artifacts_dir / "conversion_report.json"
        with open(report_path, 'w') as f:
            json.dump(conversion_results, f, indent=2)
        
        logger.info(f"Conversion complete! Report saved to: {report_path}")
        return conversion_results

def main():
    parser = argparse.ArgumentParser(description="Convert Keras model to TFLite")
    parser.add_argument("--model", type=str, 
                       default=str(CONFIG.paths.models_dir / "fixed_model.h5"),
                       help="Input Keras model path")
    parser.add_argument("--calibration_data", type=str,
                       default=str(CONFIG.paths.data_processed),
                       help="Directory with data for quantization calibration")
    
    args = parser.parse_args()
    
    converter = TFLiteConverter()
    results = converter.convert_model(Path(args.model), Path(args.calibration_data))
    
    print(f"\n🎉 TFLITE CONVERSION COMPLETE!")
    for format_name, info in results.items():
        print(f"   {format_name.upper()}: {info['size_kb']:.1f} KB")

if __name__ == "__main__":
    main()