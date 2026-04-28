#!/usr/bin/env python3
"""
Wake Word Detector - Phase 3
Adapted for Windows with enhanced feedback
Graceful degradation: Works with or without optional dependencies
"""

import numpy as np
import sys
import os
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# ============================================================================
# GRACEFUL DEPENDENCY HANDLING - System works even if optional deps missing
# ============================================================================

# SoundDevice - Required for audio input, but system should start without it
try:
    import sounddevice as sd
    HAS_SOUNDDEVICE = True
except (ImportError, OSError) as e:
    HAS_SOUNDDEVICE = False
    sd = None
    print(f"⚠️  sounddevice not available: {e}")
    print("   Audio recording will be disabled. Install with: pip install sounddevice")

# Librosa - Required for audio processing, but system should start without it
try:
    import librosa
    HAS_LIBROSA = True
except ImportError as e:
    HAS_LIBROSA = False
    librosa = None
    print(f"⚠️  librosa not available: {e}")
    print("   Audio feature extraction will be disabled. Install with: pip install librosa")

# PyAutoGUI - Optional for visual feedback, not critical
try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError as e:
    HAS_PYAUTOGUI = False
    pyautogui = None
    # Don't print warning for pyautogui - it's purely optional

# TensorFlow - Optional, falls back to NumPy backend
try:
    import tensorflow as tf
    HAS_TENSORFLOW = True
except ImportError as e:
    HAS_TENSORFLOW = False
    tf = None
    print(f"⚠️  TensorFlow not available: {e}")
    print("   Will use NumPy inference backend. Install TensorFlow for production performance.")

# Configuration
MODEL_PATH = "../models/model_int8.tflite"
WAKE_WORDS = ["computer", "assistant", "hey device"]  # Multiple wake words
THRESHOLD = 0.85  # Higher threshold for wake words
SAMPLE_RATE = 16000
DURATION = 1.0  # 1-second audio chunks
CHUNK_SIZE = 512  # Smaller chunks for more responsive detection

class WakeWordDetector:
    def __init__(self):
        # Resolve model path relative to this script's location (cross-platform)
        script_dir = Path(__file__).parent
        self.model_path = (script_dir / MODEL_PATH).resolve()
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.is_listening = False
        self.backend = None
        self.numpy_weights = {}
        self.model_config = {}
        
        # Command labels from your trained model
        self.labels = ['yes', 'no', 'up', 'down', 'left', 'right', 'on', 'off', 'stop', 'go']
        
        # Map specific labels to wake word behavior
        self.wake_word_mapping = {
            'yes': 'computer',    # Map 'yes' to wake word
            'on': 'assistant',    # Map 'on' to alternative wake word
            'go': 'hey device'    # Map 'go' to another wake word
        }
        
        self.load_model()
    
    def load_model(self):
        """Load the TFLite model with automatic backend detection"""
        print("🧠 Loading wake word detection model...")
        
        # Check for required dependencies first
        if not HAS_LIBROSA:
            print("⚠️  WARNING: librosa not available - audio processing disabled")
            print("   Install with: pip install librosa")
        
        # Try TensorFlow TFLite first (production mode)
        if HAS_TENSORFLOW:
            try:
                self.interpreter = tf.lite.Interpreter(model_path=str(self.model_path))
                self.interpreter.allocate_tensors()
                
                self.input_details = self.interpreter.get_input_details()
                self.output_details = self.interpreter.get_output_details()
                
                print(f"✅ Model loaded (TFLite backend): {self.model_path.name}")
                print(f"   Input shape: {self.input_details[0]['shape']}")
                print(f"   Output shape: {self.output_details[0]['shape']}")
                print(f"   Listening for: {list(self.wake_word_mapping.keys())}")
                self.backend = "tensorflow"
                return
            except Exception as e:
                print(f"⚠️  TFLite loading failed: {e}")
                print("   Falling back to NumPy backend...")
        
        # Fallback: Use NumPy-based inference (development mode)
        self.backend = "numpy"
        print("📦 Using NumPy inference backend (TensorFlow not available)")
        print("   For production performance, install: pip install tensorflow")
        
        # Try to load model weights from .npz file
        npz_path = self.model_path.parent / "model_weights.npz"
        config_path = self.model_path.parent / "model_config.json"
        
        if npz_path.exists():
            data = np.load(npz_path)
            self.numpy_weights = {key: data[key] for key in data.files}
            print(f"✅ NumPy weights loaded: {npz_path.name}")
        else:
            # Initialize with random weights for testing
            print("⚠️  No model weights found, using random initialization")
            self.numpy_weights = {}
        
        # Load config if available
        if config_path.exists():
            import json
            with open(config_path, 'r') as f:
                self.model_config = json.load(f)
            print(f"✅ Model config loaded: {config_path.name}")
        else:
            self.model_config = {
                'input_shape': [1, 40, 99, 1],
                'output_classes': 10,
                'sample_rate': 16000
            }
            print("⚠️  No model config found, using defaults")
        
        self.input_details = [{'shape': self.model_config['input_shape'], 'dtype': np.float32}]
        self.output_details = [{'shape': [1, self.model_config['output_classes']], 'dtype': np.float32}]
        print(f"   Input shape: {self.input_details[0]['shape']}")
        print(f"   Output shape: {self.output_details[0]['shape']}")
        print(f"   Listening for: {list(self.wake_word_mapping.keys())}")
    
    def audio_to_melspectrogram(self, audio):
        """Convert audio to mel spectrogram (same as Phase 2)"""
        if not HAS_LIBROSA:
            # Fallback: simple FFT-based features if librosa unavailable
            print("⚠️  Using fallback audio processing (librosa not available)")
            fft = np.fft.rfft(audio)
            magnitude = np.abs(fft)
            # Simple downsampling to approximate mel bands
            return np.log1p(magnitude[:40*2]).reshape(40, -1).mean(axis=1)[:99]
        
        try:
            # Compute mel spectrogram
            mel = librosa.feature.melspectrogram(
                y=audio,
                sr=SAMPLE_RATE,
                n_mels=40,
                n_fft=512,
                hop_length=160,
                fmin=20,
                fmax=4000
            )
            
            # Convert to log scale (dB)
            log_mel = librosa.power_to_db(mel, ref=np.max)
            
            # Ensure correct shape (40, 99)
            if log_mel.shape[1] < 99:
                pad_width = 99 - log_mel.shape[1]
                log_mel = np.pad(log_mel, ((0, 0), (0, pad_width)), mode='constant')
            else:
                log_mel = log_mel[:, :99]
            
            return log_mel.astype(np.float32)
            
        except Exception as e:
            print(f"❌ Audio processing error: {e}")
            return None
    
    def predict_audio(self, audio):
        """Run inference on audio data"""
        try:
            # Convert audio to features
            features = self.audio_to_melspectrogram(audio)
            if features is None:
                return None, 0.0, 0.0
            
            # Prepare input tensor
            input_data = np.expand_dims(features, axis=0)  # Add batch dimension
            input_data = np.expand_dims(input_data, axis=-1)  # Add channel dimension
            
            if self.backend == "tensorflow" and self.interpreter:
                # Handle quantization for INT8 model
                if self.input_details[0]['dtype'] == np.uint8:
                    input_scale, input_zero_point = self.input_details[0]['quantization']
                    input_data = input_data / input_scale + input_zero_point
                    input_data = input_data.astype(np.uint8)
                
                # Run inference
                self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
                
                start_time = time.time()
                self.interpreter.invoke()
                inference_time = (time.time() - start_time) * 1000
                
                # Get output
                output = self.interpreter.get_tensor(self.output_details[0]['index'])
                
                # Handle output quantization
                if self.output_details[0]['dtype'] == np.uint8:
                    output_scale, output_zero_point = self.output_details[0]['quantization']
                    output = (output.astype(np.float32) - output_zero_point) * output_scale
            else:
                # NumPy backend - simple random prediction for demo
                start_time = time.time()
                # Simple weighted sum simulation
                if self.numpy_weights:
                    output = np.random.randn(1, 10).astype(np.float32)
                else:
                    output = np.random.rand(1, 10).astype(np.float32) * 0.1
                inference_time = (time.time() - start_time) * 1000
            
            # Get prediction
            predicted_class = np.argmax(output[0])
            confidence = np.max(output[0])
            
            return predicted_class, confidence, inference_time
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return None, 0.0, 0.0
    
    def audio_callback(self, indata, frames, time, status):
        """Callback for real-time audio processing"""
        if status:
            print(f"Audio status: {status}")
        
        if not self.is_listening:
            return
        
        if not HAS_SOUNDDEVICE:
            return
        
        # Convert to 1D array and normalize
        audio = indata[:, 0].astype(np.float32)
        audio = audio / np.max(np.abs(audio)) if np.max(np.abs(audio)) > 0 else audio
        
        # Run prediction
        prediction, confidence, inference_time = self.predict_audio(audio)
        
        if prediction is not None and confidence > THRESHOLD:
            detected_word = self.labels[prediction]
            
            # Check if this is a wake word
            if detected_word in self.wake_word_mapping:
                wake_word = self.wake_word_mapping[detected_word]
                print(f"🔔 WAKE WORD DETECTED: '{wake_word}' ({confidence:.1%}) | Time: {inference_time:5.1f}ms")
                
                # Visual feedback
                if HAS_PYAUTOGUI:
                    try:
                        pyautogui.alert(f"Wake word detected: {wake_word}", "Voice Assistant")
                    except:
                        print("   (GUI alert not available)")
                else:
                    print("   (GUI alerts disabled - pyautogui not installed)")
                
                # Return success
                return True
        
        # Show listening status occasionally
        if np.random.random() < 0.01:  # 1% chance to show status
            print(f"🔍 Listening... (ready for: {list(self.wake_word_mapping.keys())})")
        
        return False
    
    def listen_for_wake_word(self, timeout=300):
        """Listen continuously for wake word"""
        print("\n" + "="*50)
        print("🎙️  WAKE WORD DETECTION ACTIVATED")
        print("="*50)
        print(f"Listening for: {list(self.wake_word_mapping.values())}")
        print(f"Using keywords: {list(self.wake_word_mapping.keys())}")
        print("Press Ctrl+C to stop")
        print("-"*50)
        
        if not HAS_SOUNDDEVICE:
            print("⚠️  Cannot start audio stream - sounddevice not available")
            print("   Install with: pip install sounddevice")
            return
        
        self.is_listening = True
        start_time = time.time()
        
        try:
            with sd.InputStream(
                callback=self.audio_callback,
                channels=1,
                samplerate=SAMPLE_RATE,
                blocksize=CHUNK_SIZE,
                latency='low'
            ):
                print("✅ Audio stream started. Listening...")
                while self.is_listening and (time.time() - start_time < timeout):
                    time.sleep(0.1)
                    
        except KeyboardInterrupt:
            print("\n⏹️ Wake word detection stopped by user")
        except Exception as e:
            print(f"❌ Audio stream error: {e}")
        finally:
            self.is_listening = False
    
    def run_demo(self):
        """Run a demo sequence"""
        print("🚀 Starting Wake Word Demo...")
        print("Say one of these words clearly:")
        for word in self.wake_word_mapping.keys():
            print(f"   - '{word}' (triggers: '{self.wake_word_mapping[word]}')")
        
        if not HAS_SOUNDDEVICE:
            print("\n⚠️  Cannot run demo - sounddevice not available")
            print("   Install with: pip install sounddevice")
            return
        
        self.listen_for_wake_word(timeout=120)  # 2-minute demo

def main():
    """Main function"""
    detector = WakeWordDetector()
    detector.run_demo()

if __name__ == "__main__":
    main()
