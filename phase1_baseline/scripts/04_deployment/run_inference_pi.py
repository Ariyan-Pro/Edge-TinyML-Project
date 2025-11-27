# phase1_baseline/scripts/run_inference_pi.py
import numpy as np
import time
import logging
from pathlib import Path
import argparse
import threading
from collections import deque
import sys
import json
from datetime import datetime

# Import configuration
sys.path.append(str(Path(__file__).parent.parent))
from config import CONFIG

# Try to import audio dependencies
try:
    import sounddevice as sd
    import soundfile as sf
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("Warning: sounddevice or soundfile not available")

# Try to import TFLite runtime
try:
    import tflite_runtime.interpreter as tflite
    TFLITE_RUNTIME = True
except ImportError:
    try:
        import tensorflow as tf
        tflite = tf.lite
        TFLITE_RUNTIME = False
    except ImportError:
        print("Error: No TFLite runtime available")
        sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealTimeKWSInference:
    """Real-time keyword spotting inference engine"""
    
    def __init__(self, model_path: Path, config=CONFIG.audio):
        self.config = config
        self.model_path = model_path
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.audio_buffer = deque(maxlen=int(config.sample_rate * 2))  # 2-second buffer
        self.is_running = False
        self.inference_stats = {
            'total_inferences': 0,
            'average_latency': 0,
            'last_prediction': None,
            'start_time': time.time()
        }
        self.class_names = ['yes', 'no', 'up', 'down', 'left', 'right', 'on', 'off', 'stop', 'go']
        
        self.setup_model()
    
    def setup_model(self):
        """Initialize TFLite model"""
        try:
            self.interpreter = tflite.Interpreter(model_path=str(self.model_path))
            self.interpreter.allocate_tensors()
            
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            logger.info(f"Model loaded successfully: {self.model_path.name}")
            logger.info(f"Input details: {self.input_details[0]}")
            logger.info(f"Output details: {self.output_details[0]}")
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
    
    def audio_callback(self, indata, frames, time_info, status):
        """Audio stream callback - stores audio data in buffer"""
        if status:
            logger.warning(f"Audio callback status: {status}")
        
        # Convert to mono and store
        audio_mono = indata[:, 0] if indata.ndim > 1 else indata
        self.audio_buffer.extend(audio_mono)
    
    def extract_audio_chunk(self) -> np.ndarray:
        """Extract 1-second audio chunk from buffer"""
        required_samples = int(self.config.sample_rate * self.config.duration)
        
        if len(self.audio_buffer) < required_samples:
            return None
        
        # Get the most recent 1-second chunk
        audio_chunk = np.array(list(self.audio_buffer))[-required_samples:]
        return audio_chunk
    
    def preprocess_audio(self, audio_chunk: np.ndarray) -> np.ndarray:
        """Preprocess audio chunk for model inference"""
        try:
            # Compute mel spectrogram
            mel_spec = self.compute_mel_spectrogram(audio_chunk)
            
            # Normalize shape
            mel_spec = self.normalize_spectrogram_shape(mel_spec)
            
            # Add batch and channel dimensions
            mel_spec = np.expand_dims(mel_spec, axis=0)  # Batch
            mel_spec = np.expand_dims(mel_spec, axis=-1)  # Channel
            
            return mel_spec
            
        except Exception as e:
            logger.error(f"Audio preprocessing failed: {str(e)}")
            return None
    
    def compute_mel_spectrogram(self, audio: np.ndarray) -> np.ndarray:
        """Compute mel spectrogram from audio"""
        import librosa
        
        mel_spec = librosa.feature.melspectrogram(
            y=audio,
            sr=self.config.sample_rate,
            n_mels=self.config.n_mels,
            n_fft=self.config.n_fft,
            hop_length=self.config.hop_length
        )
        
        log_mel = librosa.power_to_db(mel_spec, ref=np.max)
        return log_mel.astype(np.float32)
    
    def normalize_spectrogram_shape(self, spectrogram: np.ndarray) -> np.ndarray:
        """Normalize spectrogram to expected shape"""
        n_mels, n_frames = spectrogram.shape
        
        if n_frames < self.config.max_frames:
            pad_width = self.config.max_frames - n_frames
            spectrogram = np.pad(spectrogram, ((0, 0), (0, pad_width)), mode='constant')
        elif n_frames > self.config.max_frames:
            spectrogram = spectrogram[:, :self.config.max_frames]
        
        return spectrogram
    
    def run_inference(self, input_data: np.ndarray) -> Tuple[int, float]:
        """Run single inference and return prediction + latency"""
        start_time = time.time()
        
        try:
            # Handle quantization if needed
            if self.input_details[0]['dtype'] == np.uint8:
                input_scale, input_zero_point = self.input_details[0]['quantization']
                input_data = input_data / input_scale + input_zero_point
                input_data = input_data.astype(np.uint8)
            
            # Set input tensor
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            
            # Run inference
            self.interpreter.invoke()
            
            # Get output
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
            
            # Handle output quantization if needed
            if self.output_details[0]['dtype'] == np.uint8:
                output_scale, output_zero_point = self.output_details[0]['quantization']
                output_data = (output_data.astype(np.float32) - output_zero_point) * output_scale
            
            inference_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Get prediction
            prediction = np.argmax(output_data, axis=1)[0]
            confidence = np.max(output_data)
            
            return prediction, confidence, inference_time
            
        except Exception as e:
            logger.error(f"Inference failed: {str(e)}")
            return -1, 0.0, 0.0
    
    def inference_loop(self):
        """Main inference loop"""
        logger.info("Starting inference loop...")
        
        while self.is_running:
            try:
                # Extract audio chunk
                audio_chunk = self.extract_audio_chunk()
                if audio_chunk is None:
                    time.sleep(0.01)  # Wait for more audio data
                    continue
                
                # Preprocess
                input_data = self.preprocess_audio(audio_chunk)
                if input_data is None:
                    continue
                
                # Run inference
                prediction, confidence, latency = self.run_inference(input_data)
                
                # Update statistics
                self.inference_stats['total_inferences'] += 1
                self.inference_stats['average_latency'] = (
                    self.inference_stats['average_latency'] * (self.inference_stats['total_inferences'] - 1) + latency
                ) / self.inference_stats['total_inferences']
                
                # Only report high-confidence predictions
                if confidence > 0.7 and prediction < len(self.class_names):
                    predicted_class = self.class_names[prediction]
                    self.inference_stats['last_prediction'] = {
                        'class': predicted_class,
                        'confidence': float(confidence),
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    print(f"🎯 PREDICTION: {predicted_class} ({confidence:.2f}) | Latency: {latency:.1f}ms")
                
                # Small delay to prevent overwhelming CPU
                time.sleep(0.05)
                
            except Exception as e:
                logger.error(f"Inference loop error: {str(e)}")
                time.sleep(0.1)
    
    def start(self, audio_device=None):
        """Start real-time inference"""
        if not AUDIO_AVAILABLE:
            logger.error("Audio dependencies not available")
            return
        
        try:
            # Start audio stream
            self.audio_stream = sd.InputStream(
                samplerate=self.config.sample_rate,
                channels=1,
                blocksize=int(self.config.sample_rate * 0.1),  # 100ms blocks
                device=audio_device,
                callback=self.audio_callback
            )
            
            self.audio_stream.start()
            logger.info("Audio stream started")
            
            # Start inference loop
            self.is_running = True
            self.inference_loop()
            
        except Exception as e:
            logger.error(f"Failed to start inference: {str(e)}")
    
    def stop(self):
        """Stop real-time inference"""
        self.is_running = False
        
        if hasattr(self, 'audio_stream'):
            self.audio_stream.stop()
            self.audio_stream.close()
            logger.info("Audio stream stopped")
        
        # Save inference statistics
        self.save_statistics()
    
    def save_statistics(self):
        """Save inference statistics to file"""
        stats_path = CONFIG.paths.artifacts_dir / "inference_statistics.json"
        
        self.inference_stats['end_time'] = time.time()
        self.inference_stats['total_duration'] = self.inference_stats['end_time'] - self.inference_stats['start_time']
        
        with open(stats_path, 'w') as f:
            json.dump(self.inference_stats, f, indent=2)
        
        logger.info(f"Inference statistics saved to: {stats_path}")

def list_audio_devices():
    """List available audio devices"""
    if not AUDIO_AVAILABLE:
        print("Audio dependencies not available")
        return
    
    print("Available audio devices:")
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        print(f"  {i}: {device['name']} (in: {device['max_input_channels']}, out: {device['max_output_channels']})")

def main():
    parser = argparse.ArgumentParser(description="Real-time KWS Inference on Raspberry Pi")
    parser.add_argument("--model", type=str, required=True,
                       help="TFLite model path")
    parser.add_argument("--device", type=int, default=None,
                       help="Audio device ID")
    parser.add_argument("--list_devices", action="store_true",
                       help="List audio devices and exit")
    
    args = parser.parse_args()
    
    if args.list_devices:
        list_audio_devices()
        return
    
    if not Path(args.model).exists():
        print(f"Error: Model file not found: {args.model}")
        return
    
    # Create inference engine
    inference_engine = RealTimeKWSInference(Path(args.model))
    
    try:
        print("Starting real-time keyword spotting...")
        print("Press Ctrl+C to stop")
        print("-" * 50)
        
        inference_engine.start(audio_device=args.device)
        
    except KeyboardInterrupt:
        print("\nStopping inference...")
        inference_engine.stop()
        print("Inference stopped")

if __name__ == "__main__":
    main()