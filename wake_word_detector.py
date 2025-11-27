#!/usr/bin/env python3
"""
Improved Wake Word Detector - Fixed Audio Issues
"""

import numpy as np
import sounddevice as sd
import librosa
import time
import pyautogui
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Configuration
MODEL_PATH = r"..\models\model_int8.tflite"
THRESHOLD = 0.85
SAMPLE_RATE = 16000
DURATION = 1.0
CHUNK_SIZE = 2048  # Increased buffer size to prevent overflow

class WakeWordDetector:
    def __init__(self):
        self.model_path = Path(MODEL_PATH)
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.is_listening = False
        
        self.labels = ['yes', 'no', 'up', 'down', 'left', 'right', 'on', 'off', 'stop', 'go']
        
        self.wake_word_mapping = {
            'yes': 'computer',
            'on': 'assistant', 
            'go': 'hey device'
        }
        
        self.load_model()
    
    def load_model(self):
        print("Loading wake word detection model...")
        try:
            import tensorflow as tf
            self.interpreter = tf.lite.Interpreter(model_path=str(self.model_path))
            self.interpreter.allocate_tensors()
            
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            print(f"Model loaded: {self.model_path.name}")
            print(f"Listening for: {list(self.wake_word_mapping.keys())}")
            
        except Exception as e:
            print(f"Failed to load model: {e}")
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
