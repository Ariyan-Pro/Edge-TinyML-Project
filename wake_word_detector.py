#!/usr/bin/env python3
"""
Improved Wake Word Detector - Fixed Audio Issues
Now with automatic fallback to NumPy backend when TensorFlow is unavailable
Graceful handling of optional audio libraries (sounddevice, pyautogui, librosa)
"""

import numpy as np
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Optional imports with graceful fallback
try:
    import sounddevice as sd
    HAS_SOUNDDEVICE = True
except (ImportError, OSError):
    HAS_SOUNDDEVICE = False
    print("⚠️  sounddevice not available (PortAudio missing or not installed)")

try:
    import librosa
    HAS_LIBROSA = True
except ImportError:
    HAS_LIBROSA = False
    print("⚠️  librosa not available")

try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

import time

# Configuration
MODEL_PATH = Path(__file__).parent / "models" / "model_int8.tflite"
THRESHOLD = 0.85
SAMPLE_RATE = 16000
DURATION = 1.0
CHUNK_SIZE = 2048  # Increased buffer size to prevent overflow

class WakeWordDetector:
    def __init__(self):
        self.model_path = MODEL_PATH
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.is_listening = False
        self.using_tensorflow = False
        
        self.labels = ['yes', 'no', 'up', 'down', 'left', 'right', 'on', 'off', 'stop', 'go']
        
        self.wake_word_mapping = {
            'yes': 'computer',
            'on': 'assistant', 
            'go': 'hey device'
        }
        
        self.load_model()
    
    def load_model(self):
        print("Loading wake word detection model...")
        
        # Try TensorFlow first (production mode)
        try:
            import tensorflow as tf
            print("  → TensorFlow available, using TFLite backend")
            self.interpreter = tf.lite.Interpreter(model_path=str(self.model_path))
            self.interpreter.allocate_tensors()
            
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            self.using_tensorflow = True
            
            print(f"  ✅ Model loaded: {self.model_path.name}")
            print(f"  📊 Input shape: {self.input_details[0]['shape']}")
            print(f"  🎯 Listening for: {list(self.wake_word_mapping.keys())}")
            
        except ImportError:
            print("  ⚠️  TensorFlow not found, using NumPy backend")
            self._load_numpy_backend()
        except Exception as e:
            print(f"  ⚠️  TFLite loading failed: {e}")
            print("  → Falling back to NumPy backend")
            self._load_numpy_backend()
    
    def _load_numpy_backend(self):
        """Load the lightweight NumPy-based inference engine"""
        try:
            from models.lightweight_inference import LightweightInference
            self.interpreter = LightweightInference()
            self.interpreter.allocate_tensors()
            
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            self.using_tensorflow = False
            
            print(f"  ✅ NumPy backend loaded successfully")
            print(f"  📊 Input shape: {self.input_details[0]['shape']}")
            print(f"  🎯 Listening for: {list(self.wake_word_mapping.keys())}")
            
        except Exception as e:
            print(f"  ❌ Failed to load NumPy backend: {e}")
            print("\n  💡 Run: python minimal_model_generator.py")
            print("     to generate the required model files.\n")
            sys.exit(1)
    
    def audio_to_melspectrogram(self, audio):
        try:
            mel = librosa.feature.melspectrogram(
                y=audio,
                sr=SAMPLE_RATE,
                n_mels=40,
                n_fft=512,
                hop_length=160
            )
            
            log_mel = librosa.power_to_db(mel, ref=np.max)
            
            if log_mel.shape[1] < 99:
                pad_width = 99 - log_mel.shape[1]
                log_mel = np.pad(log_mel, ((0, 0), (0, pad_width)), mode='constant')
            else:
                log_mel = log_mel[:, :99]
            
            return log_mel.astype(np.float32)
            
        except Exception as e:
            print(f"Audio processing error: {e}")
            return None
    
    def predict_audio(self, audio):
        """Predict wake word from audio data"""
        try:
            features = self.audio_to_melspectrogram(audio)
            if features is None:
                return None, 0.0, 0.0
            
            input_data = np.expand_dims(features, axis=0)
            input_data = np.expand_dims(input_data, axis=-1)
            
            if self.input_details[0]['dtype'] == np.uint8:
                input_scale, input_zero_point = self.input_details[0]['quantization']
                input_data = input_data / input_scale + input_zero_point
                input_data = input_data.astype(np.uint8)
            
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            
            start_time = time.time()
            self.interpreter.invoke()
            inference_time = (time.time() - start_time) * 1000
            
            output = self.interpreter.get_tensor(self.output_details[0]['index'])
            
            if self.output_details[0]['dtype'] == np.uint8:
                output_scale, output_zero_point = self.output_details[0]['quantization']
                output = (output.astype(np.float32) - output_zero_point) * output_scale
            
            predicted_class = np.argmax(output[0])
            confidence = np.max(output[0])
            
            return predicted_class, confidence, inference_time
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return None, 0.0, 0.0
    
    def detect_wake_word(self, mel_spectrogram=None):
        """Detect wake word from pre-computed mel spectrogram or random input for benchmarking
        
        Args:
            mel_spectrogram: Optional mel spectrogram array of shape (40, 99) or (1, 40, 99, 1)
                            If None, generates random input for benchmarking
            
        Returns:
            tuple: (predicted_class, confidence, inference_time_ms)
        """
        try:
            # If no input provided, generate random input for benchmarking
            if mel_spectrogram is None:
                mel_spectrogram = np.random.randn(1, 40, 99, 1).astype(np.float32)
            else:
                # Ensure correct shape
                if len(mel_spectrogram.shape) == 2:
                    mel_spectrogram = np.expand_dims(mel_spectrogram, axis=0)
                    mel_spectrogram = np.expand_dims(mel_spectrogram, axis=-1)
                elif len(mel_spectrogram.shape) == 3:
                    mel_spectrogram = np.expand_dims(mel_spectrogram, axis=-1)
            
            input_data = mel_spectrogram.astype(np.float32)
            
            # Handle quantization if needed
            if self.input_details[0]['dtype'] == np.uint8:
                input_scale, input_zero_point = self.input_details[0]['quantization']
                input_data = input_data / input_scale + input_zero_point
                input_data = input_data.astype(np.uint8)
            
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            
            start_time = time.time()
            self.interpreter.invoke()
            inference_time = (time.time() - start_time) * 1000
            
            output = self.interpreter.get_tensor(self.output_details[0]['index'])
            
            if self.output_details[0]['dtype'] == np.uint8:
                output_scale, output_zero_point = self.output_details[0]['quantization']
                output = (output.astype(np.float32) - output_zero_point) * output_scale
            
            predicted_class = np.argmax(output[0])
            confidence = np.max(output[0])
            
            return predicted_class, confidence, inference_time
            
        except Exception as e:
            print(f"Wake word detection error: {e}")
            return None, 0.0, 0.0
    
    def audio_callback(self, indata, frames, time, status):
        if status:
            # Don't print overflow messages - they're normal
            if 'overflow' not in str(status):
                print(f"Audio status: {status}")
        
        if not self.is_listening:
            return
        
        audio = indata[:, 0].astype(np.float32)
        audio = audio / np.max(np.abs(audio)) if np.max(np.abs(audio)) > 0 else audio
        
        prediction, confidence, inference_time = self.predict_audio(audio)
        
        if prediction is not None and confidence > THRESHOLD:
            detected_word = self.labels[prediction]
            
            if detected_word in self.wake_word_mapping:
                wake_word = self.wake_word_mapping[detected_word]
                print(f"WAKE WORD DETECTED: '{wake_word}' ({confidence:.1%}) | Time: {inference_time:5.1f}ms")
                
                try:
                    pyautogui.alert(f"Wake word detected: {wake_word}", "Voice Assistant")
                except:
                    print("   (GUI alert not available)")
                
                return True
        
        return False
    
    def listen_for_wake_word(self, timeout=300):
        print("\n" + "="*50)
        print("WAKE WORD DETECTION ACTIVATED")
        print("="*50)
        print(f"Listening for: {list(self.wake_word_mapping.values())}")
        print("Press Ctrl+C to stop")
        print("-"*50)
        
        self.is_listening = True
        start_time = time.time()
        
        try:
            with sd.InputStream(
                callback=self.audio_callback,
                channels=1,
                samplerate=SAMPLE_RATE,
                blocksize=CHUNK_SIZE,  # Larger buffer
                latency='high'  # Higher latency but more stable
            ):
                print("Audio stream started. Say 'yes', 'on', or 'go'...")
                while self.is_listening and (time.time() - start_time < timeout):
                    time.sleep(0.1)
                    
        except KeyboardInterrupt:
            print("\nWake word detection stopped by user")
        except Exception as e:
            print(f"Audio stream error: {e}")
        finally:
            self.is_listening = False
    
    def run_demo(self):
        print("Starting Wake Word Demo...")
        print("Say one of these words clearly:")
        for word in self.wake_word_mapping.keys():
            print(f"   - '{word}'")
        
        self.listen_for_wake_word(timeout=120)

def main():
    detector = WakeWordDetector()
    detector.run_demo()

if __name__ == "__main__":
    main()
