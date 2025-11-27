#!/usr/bin/env python3
"""
REAL-TIME KEYWORD SPOTTING - WINDOWS FIXED VERSION
Uses TensorFlow's TFLite instead of tflite_runtime
"""

import numpy as np
import librosa
import time
import threading
from pathlib import Path
import sys

# Use TensorFlow's TFLite (you already have TensorFlow installed!)
try:
    import tensorflow as tf
    tflite = tf.lite
    print("✅ Using TensorFlow's TFLite interpreter")
except ImportError:
    print("❌ TensorFlow not available")
    sys.exit(1)

try:
    import sounddevice as sd
    AUDIO_AVAILABLE = True
    print("✅ Audio devices available")
except ImportError:
    print("❌ sounddevice not available")
    AUDIO_AVAILABLE = False

class WindowsKeywordSpotter:
    def __init__(self, model_path='../../models/production/model_int8.tflite'):
        self.model_path = Path(model_path)
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.labels = ['yes', 'no', 'up', 'down', 'left', 'right', 'on', 'off', 'stop', 'go']
        self.is_running = False
        
        self.load_model()
        self.setup_audio()
    
    def load_model(self):
        """Load the TFLite model and allocate tensors"""
        print("🧠 Loading TensorFlow Lite model...")
        try:
            self.interpreter = tflite.Interpreter(model_path=str(self.model_path))
            self.interpreter.allocate_tensors()
            
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            print(f"✅ Model loaded: {self.model_path.name}")
            print(f"   Input: {self.input_details[0]['shape']}")
            print(f"   Output: {self.output_details[0]['shape']}")
            print(f"   Labels: {self.labels}")
            
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            sys.exit(1)
    
    def setup_audio(self):
        """Setup audio devices"""
        if AUDIO_AVAILABLE:
            try:
                devices = sd.query_devices()
                print("🎙️ Available audio input devices:")
                for i, device in enumerate(devices):
                    if device['max_input_channels'] > 0:
                        print(f"   {i}: {device['name']}")
                
                self.sample_rate = 16000
                self.duration = 1.0  # 1-second audio chunks
                self.channels = 1
                
                print(f"✅ Audio setup: {self.sample_rate}Hz, {self.duration}s chunks")
                
            except Exception as e:
                print(f"⚠️ Audio setup warning: {e}")
        else:
            print("🎧 Audio not available - using simulation mode")
    
    def audio_to_melspectrogram(self, audio):
        """Convert audio to mel spectrogram"""
        try:
            # Compute mel spectrogram
            mel = librosa.feature.melspectrogram(
                y=audio,
                sr=16000,
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
        
        # Convert to 1D array and normalize
        audio = indata[:, 0].astype(np.float32)
        audio = audio / np.max(np.abs(audio)) if np.max(np.abs(audio)) > 0 else audio
        
        # Run prediction
        prediction, confidence, inference_time = self.predict_audio(audio)
        
        if prediction is not None and confidence > 0.5:  # Only show confident predictions
            label = self.labels[prediction]
            print(f"🎯 Heard: {label:6s} ({confidence:.1%}) | Time: {inference_time:5.1f}ms")
        else:
            print(f"🔇 Listening... (confidence: {confidence:.1%})")
    
    def generate_synthetic_audio(self):
        """Generate synthetic audio for testing without microphone"""
        print("🎧 Running in SIMULATION mode - generating synthetic detections")
        
        while self.is_running:
            # Simulate random keyword patterns
            time.sleep(2.0)  # Wait 2 seconds between "detections"
            
            # Random "detection"
            if np.random.random() > 0.3:  # 70% chance of detection
                keyword_idx = np.random.randint(0, len(self.labels))
                confidence = np.random.uniform(0.7, 0.95)
                inference_time = np.random.uniform(2.0, 5.0)
                
                label = self.labels[keyword_idx]
                print(f"🎯 Heard: {label:6s} ({confidence:.1%}) | Time: {inference_time:5.1f}ms")
            else:
                print("🔇 Listening... (silence)")
    
    def run_real_time(self):
        """Main real-time inference loop"""
        print("\n" + "="*50)
        print("🚀 REAL-TIME KEYWORD SPOTTING - WINDOWS")
        print("="*50)
        print("Speak one of these commands:")
        print("yes, no, up, down, left, right, on, off, stop, go")
        print("Press Ctrl+C to stop")
        print("-"*50)
        
        self.is_running = True
        
        try:
            if AUDIO_AVAILABLE:
                print("🎤 Using REAL microphone input")
                print("✅ Listening... Speak now!")
                
                # Start audio stream
                with sd.InputStream(
                    callback=self.audio_callback,
                    channels=1,
                    samplerate=16000,
                    blocksize=int(16000 * 1.0),  # 1-second chunks
                    latency='low'
                ):
                    while self.is_running:
                        time.sleep(0.1)
            else:
                self.generate_synthetic_audio()
                
        except KeyboardInterrupt:
            print("\n⏹️ Stopping real-time inference...")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            self.is_running = False

def main():
    """Main function"""
    # Use the smallest, fastest model
    model_path = '../../models/production/model_int8.tflite'
    
    if not Path(model_path).exists():
        print(f"❌ Model not found: {model_path}")
        print("Please check the model path and try again")
        return
    
    print("🔧 Initializing Real-time Keyword Spotting...")
    
    # Create and run keyword spotter
    spotter = WindowsKeywordSpotter(model_path)
    spotter.run_real_time()

if __name__ == "__main__":
    main()