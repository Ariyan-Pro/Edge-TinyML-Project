# phase1_baseline/scripts/evaluate_and_bench.py
import numpy as np
import time
import json
import logging
from pathlib import Path
import argparse
from typing import Dict, List, Tuple
import sys
import psutil
import gc

# Import configuration
sys.path.append(str(Path(__file__).parent.parent))
from config import CONFIG

# Try to import TFLite runtime, fallback to TensorFlow
try:
    import tflite_runtime.interpreter as tflite
    TFLITE_RUNTIME = True
except ImportError:
    import tensorflow as tf
    tflite = tf.lite
    TFLITE_RUNTIME = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedModelEvaluator:
    """Comprehensive model evaluation and benchmarking"""
    
    def __init__(self):
        self.benchmark_results = {}
        self.memory_tracker = MemoryTracker()
    
    def load_test_data(self, npy_dir: Path, max_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """Load test data for evaluation"""
        
        npy_files = list(npy_dir.rglob("*.npy"))
        selected_files = npy_files[:max_samples]
        
        X, y = [], []
        for file_path in selected_files:
            try:
                spectrogram = np.load(file_path)
                X.append(spectrogram)
                # Extract class from path
                class_name = file_path.parent.name
                y.append(class_name)
            except Exception as e:
                logger.warning(f"Failed to load {file_path}: {str(e)}")
        
        X = np.array(X)
        y = np.array(y)
        
        logger.info(f"Loaded {len(X)} test samples")
        return X, y
    
    def setup_interpreter(self, model_path: Path) -> any:
        """Setup TFLite interpreter with optimization"""
        
        try:
            interpreter = tflite.Interpreter(model_path=str(model_path))
            interpreter.allocate_tensors()
            return interpreter
        except Exception as e:
            logger.error(f"Failed to setup interpreter for {model_path}: {str(e)}")
            return None
    
    def run_inference_benchmark(self, interpreter, input_data: np.ndarray, num_runs: int = 100) -> Dict:
        """Run comprehensive inference benchmarking"""
        
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        # Warm-up runs
        for _ in range(10):
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
        
        # Main benchmarking
        latencies = []
        for _ in range(num_runs):
            start_time = time.perf_counter()
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            end_time = time.perf_counter()
            latencies.append((end_time - start_time) * 1000)  # Convert to ms
        
        return {
            'mean_latency_ms': np.mean(latencies),
            'std_latency_ms': np.std(latencies),
            'min_latency_ms': np.min(latencies),
            'max_latency_ms': np.max(latencies),
            'p95_latency_ms': np.percentile(latencies, 95),
            'throughput_fps': 1000 / np.mean(latencies)  # Frames per second
        }
    
    def evaluate_accuracy(self, interpreter, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """Evaluate model accuracy on test set"""
        
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        predictions = []
        actual = []
        
        for i in range(len(X_test)):
            # Prepare input
            input_data = np.expand_dims(X_test[i], axis=0).astype(np.float32)
            
            # Handle quantization if needed
            if input_details[0]['dtype'] == np.uint8:
                input_scale, input_zero_point = input_details[0]['quantization']
                input_data = input_data / input_scale + input_zero_point
                input_data = input_data.astype(np.uint8)
            
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            
            # Get output
            output_data = interpreter.get_tensor(output_details[0]['index'])
            
            if output_details[0]['dtype'] == np.uint8:
                output_scale, output_zero_point = output_details[0]['quantization']
                output_data = (output_data.astype(np.float32) - output_zero_point) * output_scale
            
            predicted_class = np.argmax(output_data)
            predictions.append(predicted_class)
            actual.append(i % len(np.unique(y_test)))  # Simplified - should map actual labels
        
        # Calculate accuracy
        accuracy = np.mean(np.array(predictions) == np.array(actual))
        
        return {
            'accuracy': float(accuracy),
            'total_samples': len(X_test),
            'predictions': predictions,
            'actual': actual
        }
    
    def measure_memory_usage(self, interpreter) -> Dict:
        """Measure memory usage of the model"""
        
        model_size = Path(interpreter._model_path).stat().st_size if hasattr(interpreter, '_model_path') else 0
        
        return {
            'model_size_kb': model_size / 1024,
            'peak_memory_mb': self.memory_tracker.peak_memory_usage(),
            'current_memory_mb': psutil.Process().memory_info().rss / (1024 * 1024)
        }
    
    def comprehensive_evaluation(self, model_path: Path, test_data_dir: Path) -> Dict:
        """Run comprehensive evaluation on a model"""
        
        logger.info(f"Evaluating model: {model_path}")
        
        # Load test data
        X_test, y_test = self.load_test_data(test_data_dir)
        
        # Setup interpreter
        interpreter = self.setup_interpreter(model_path)
        if interpreter is None:
            return {}
        
        results = {
            'model_path': str(model_path),
            'model_size_mb': Path(model_path).stat().st_size / (1024 * 1024),
            'evaluation_timestamp': time.time()
        }
        
        # Run benchmarks
        sample_input = np.expand_dims(X_test[0], axis=0).astype(np.float32)
        
        # Inference benchmark
        inference_results = self.run_inference_benchmark(interpreter, sample_input)
        results.update(inference_results)
        
        # Accuracy evaluation
        accuracy_results = self.evaluate_accuracy(interpreter, X_test, y_test)
        results.update(accuracy_results)
        
        # Memory usage
        memory_results = self.measure_memory_usage(interpreter)
        results.update(memory_results)
        
        logger.info(f"Evaluation complete for {model_path.name}")
        logger.info(f"  Accuracy: {accuracy_results['accuracy']:.4f}")
        logger.info(f"  Mean Latency: {inference_results['mean_latency_ms']:.2f} ms")
        logger.info(f"  Throughput: {inference_results['throughput_fps']:.2f} FPS")
        
        return results

class MemoryTracker:
    """Track memory usage during evaluation"""
    
    def __init__(self):
        self.peak_memory = 0
        self.start_memory = psutil.Process().memory_info().rss
    
    def peak_memory_usage(self) -> float:
        """Get peak memory usage in MB"""
        current = psutil.Process().memory_info().rss
        self.peak_memory = max(self.peak_memory, current)
        return self.peak_memory / (1024 * 1024)

def main():
    parser = argparse.ArgumentParser(description="Advanced Model Evaluation and Benchmarking")
    parser.add_argument("--model", type=str, required=True,
                       help="TFLite model path to evaluate")
    parser.add_argument("--test_data", type=str, required=True,
                       help="Directory with test data (.npy files)")
    parser.add_argument("--output_report", type=str,
                       help="Output report path")
    
    args = parser.parse_args()
    
    evaluator = AdvancedModelEvaluator()
    results = evaluator.comprehensive_evaluation(Path(args.model), Path(args.test_data))
    
    # Save results
    if args.output_report:
        report_path = Path(args.output_report)
    else:
        report_path = CONFIG.paths.artifacts_dir / f"benchmark_{Path(args.model).stem}.json"
    
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nBenchmark Results for {Path(args.model).name}:")
    print(f"  Accuracy: {results.get('accuracy', 0):.4f}")
    print(f"  Mean Latency: {results.get('mean_latency_ms', 0):.2f} ms")
    print(f"  Throughput: {results.get('throughput_fps', 0):.2f} FPS")
    print(f"  Model Size: {results.get('model_size_mb', 0):.2f} MB")
    print(f"  Report saved to: {report_path}")

if __name__ == "__main__":
    main()