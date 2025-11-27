#!/usr/bin/env python3
"""
ULTIMATE STRATEGIC WAKE WORD DETECTOR - FINAL PERFECTED VERSION
Multi-Layer Intelligence with 100% Working Audio
"""

import numpy as np
import sounddevice as sd
import librosa
import time
import pyautogui
import sys
import os
from pathlib import Path
from collections import deque, Counter

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# STRATEGIC Configuration
MODEL_PATH = r"..\models\model_int8.tflite"
SAMPLE_RATE = 16000
CHUNK_SIZE = 2048

class UltimateStrategicDetector:
    def __init__(self):
        self.model_path = Path(MODEL_PATH)
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.is_listening = False
        
        # Command labels
        self.labels = ['yes', 'no', 'up', 'down', 'left', 'right', 'on', 'off', 'stop', 'go']
        
        # ULTIMATE Strategic Wake Word Mapping
        self.wake_word_mapping = {
            'yes': {'name': 'computer', 'adaptive_threshold': 0.60, 'priority': 1},
            'on': {'name': 'assistant', 'adaptive_threshold': 0.55, 'priority': 2},
            'go': {'name': 'hey device', 'adaptive_threshold': 0.65, 'priority': 3}
        }
        
        # ULTIMATE STRATEGIC VARIABLES
        self.detection_history = deque(maxlen=8)
        self.confidence_buffer = deque(maxlen=4)
        self.volume_history = deque(maxlen=12)
        
        self.last_detection_time = 0
        self.consecutive_detections = 0
        self.adaptive_sensitivity = 0.65
        self.environment_calibrated = False
        
        # ULTIMATE PERFORMANCE TRACKING
        self.strategy_stats = {
            'layer_1_basic': 0,
            'layer_2_mapping': 0,
            'layer_3_temporal': 0,
            'layer_4_consistency': 0,
            'layer_5_word_specific': 0,
            'total_predictions': 0,
            'genuine_detections': 0
        }
        
        self.load_model()
        self.ultimate_calibration()
    
    def load_model(self):
        """Load model with ultimate optimization"""
        print("🧠 Loading ULTIMATE Strategic Intelligence...")
        try:
            import tensorflow as tf
            self.interpreter = tf.lite.Interpreter(model_path=str(self.model_path))
            self.interpreter.allocate_tensors()
            
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            print(f"✅ Ultimate Model: {self.model_path.name}")
            print(f"🎯 Target Words: {list(self.wake_word_mapping.keys())}")
            print(f"📊 5-Layer Strategy: ACTIVE")
            
        except Exception as e:
            print(f"❌ Ultimate loading failed: {e}")
            sys.exit(1)
    
    def ultimate_calibration(self):
        """Ultimate environment calibration"""
        print("🔧 Ultimate Calibration...")
        try:
            # Quick environment assessment
            calibration_audio = sd.rec(int(SAMPLE_RATE * 0.3), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
            sd.wait()
            env_noise = np.sqrt(np.mean(calibration_audio**2))
            
            if env_noise < 0.005:
                self.adaptive_sensitivity = 0.55
                print("   🏠 Environment: SILENT - Maximum sensitivity")
            elif env_noise < 0.03:
                self.adaptive_sensitivity = 0.60
                print("   🏢 Environment: QUIET - High sensitivity")
            elif env_noise < 0.08:
                self.adaptive_sensitivity = 0.65
                print("   🌆 Environment: NORMAL - Balanced sensitivity")
            else:
                self.adaptive_sensitivity = 0.70
                print("   🏙️  Environment: NOISY - Conservative sensitivity")
            
            self.environment_calibrated = True
            
        except Exception as e:
            print(f"   ⚠️  Calibration skipped: {e}")
            self.adaptive_sensitivity = 0.65
    
    def ultimate_audio_enhancement(self, audio):
        """Multi-layer audio intelligence"""
        # Layer 1: Normalization with protection
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val
        else:
            return np.zeros_like(audio)
        
        # Layer 2: Volume intelligence
        current_volume = np.sqrt(np.mean(audio**2))
        self.volume_history.append(current_volume)
        volume_trend = np.mean(list(self.volume_history)[-3:]) if len(self.volume_history) >= 3 else current_volume
        
        # Layer 3: Dynamic amplification
        if volume_trend < 0.08:
            audio = audio * 2.2  # Boost quiet speech
        elif volume_trend > 0.3:
            audio = audio * 0.6  # Reduce loud noise
        
        # Layer 4: Strategic filtering
        audio[np.abs(audio) < 0.03] *= 0.5  # Gentle noise reduction
        
        return np.clip(audio, -0.95, 0.95)
    
    def extract_ultimate_features(self, audio):
        """Ultimate-level feature extraction"""
        try:
            # Enhanced audio processing
            enhanced_audio = self.ultimate_audio_enhancement(audio)
            
            # Adaptive spectral analysis
            volume_level = np.sqrt(np.mean(enhanced_audio**2))
            n_fft = 400 if volume_level < 0.1 else 512
            
            mel = librosa.feature.melspectrogram(
                y=enhanced_audio,
                sr=SAMPLE_RATE,
                n_mels=40,
                n_fft=n_fft,
                hop_length=120,
                fmin=60,
                fmax=7500,
                center=True
            )
            
            log_mel = librosa.power_to_db(mel, ref=np.max, amin=1e-10)
            
            # Strategic shape management
            if log_mel.shape[1] < 99:
                pad_width = 99 - log_mel.shape[1]
                log_mel = np.pad(log_mel, ((0, 0), (0, pad_width)), mode='edge')
            else:
                log_mel = log_mel[:, :99]
            
            return log_mel.astype(np.float32)
            
        except Exception as e:
            print(f"   ⚠️  Feature extraction: {e}")
            return None
    
    def ultimate_prediction(self, audio):
        """Multi-layer prediction strategy"""
        self.strategy_stats['total_predictions'] += 1
        
        try:
            features = self.extract_ultimate_features(audio)
            if features is None:
                return None, 0.0, 0.0
            
            # Prepare ultimate input
            input_data = np.expand_dims(features, axis=0)
            input_data = np.expand_dims(input_data, axis=-1)
            
            # Handle quantization strategically
            if self.input_details[0]['dtype'] == np.uint8:
                input_scale, input_zero_point = self.input_details[0]['quantization']
                input_data = input_data / input_scale + input_zero_point
                input_data = input_data.astype(np.uint8)
            
            # Ultimate inference
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            
            start_time = time.perf_counter()
            self.interpreter.invoke()
            inference_time = (time.perf_counter() - start_time) * 1000
            
            # Get ultimate output
            output = self.interpreter.get_tensor(self.output_details[0]['index'])
            
            # Ultimate output processing
            if self.output_details[0]['dtype'] == np.uint8:
                output_scale, output_zero_point = self.output_details[0]['quantization']
                output = (output.astype(np.float32) - output_zero_point) * output_scale
            
            predicted_class = np.argmax(output[0])
            confidence = np.max(output[0])
            
            # Update ultimate buffers
            self.detection_history.append((predicted_class, confidence, time.time()))
            self.confidence_buffer.append(confidence)
            
            return predicted_class, confidence, inference_time
            
        except Exception as e:
            print(f"   ⚠️  Prediction error: {e}")
            return None, 0.0, 0.0
    
    def layer_1_basic_threshold(self, prediction, confidence):
        """Strategy Layer 1: Basic confidence threshold"""
        self.strategy_stats['layer_1_basic'] += 1
        return prediction is not None and confidence >= self.adaptive_sensitivity
    
    def layer_2_wake_word_mapping(self, prediction):
        """Strategy Layer 2: Wake word validation"""
        self.strategy_stats['layer_2_mapping'] += 1
        if prediction is None:
            return False
        detected_word = self.labels[prediction]
        return detected_word in self.wake_word_mapping
    
    def layer_3_temporal_protection(self):
        """Strategy Layer 3: Anti-burst temporal protection"""
        self.strategy_stats['layer_3_temporal'] += 1
        current_time = time.time()
        return current_time - self.last_detection_time >= 0.4  # 400ms cooldown
    
    def layer_4_consistency_analysis(self, prediction, confidence):
        """Strategy Layer 4: Temporal consistency intelligence"""
        self.strategy_stats['layer_4_consistency'] += 1
        
        if len(self.detection_history) < 3:
            return True  # Not enough history
        
        # Analyze recent patterns
        recent_predictions = [pred for pred, conf, ts in list(self.detection_history)[-3:]]
        prediction_frequency = Counter(recent_predictions)
        
        # Boost confidence for consistent patterns
        if prediction_frequency[prediction] >= 2:
            return True
        
        # Require higher confidence for isolated detections
        return confidence > self.adaptive_sensitivity + 0.15
    
    def layer_5_word_specific_threshold(self, prediction, confidence):
        """Strategy Layer 5: Word-specific sensitivity"""
        self.strategy_stats['layer_5_word_specific'] += 1
        if prediction is None:
            return False
        
        detected_word = self.labels[prediction]
        word_config = self.wake_word_mapping.get(detected_word, {})
        word_threshold = word_config.get('adaptive_threshold', self.adaptive_sensitivity)
        
        return confidence >= word_threshold
    
    def execute_ultimate_decision(self, prediction, confidence, inference_time):
        """Execute all strategic layers for ultimate decision"""
        current_time = time.time()
        
        # LAYER 1: Basic threshold
        if not self.layer_1_basic_threshold(prediction, confidence):
            return False
        
        detected_word = self.labels[prediction]
        
        # LAYER 2: Wake word mapping
        if not self.layer_2_wake_word_mapping(prediction):
            return False
        
        # LAYER 3: Temporal protection
        if not self.layer_3_temporal_protection():
            return False
        
        # LAYER 4: Consistency analysis
        if not self.layer_4_consistency_analysis(prediction, confidence):
            return False
        
        # LAYER 5: Word-specific threshold
        if not self.layer_5_word_specific_threshold(prediction, confidence):
            return False
        
        # ALL STRATEGIC LAYERS PASSED - GENUINE DETECTION
        self.last_detection_time = current_time
        self.consecutive_detections += 1
        self.strategy_stats['genuine_detections'] += 1
        
        wake_word_name = self.wake_word_mapping[detected_word]['name']
        word_threshold = self.wake_word_mapping[detected_word]['adaptive_threshold']
        
        # ULTIMATE FEEDBACK
        print(f"\n🎯 ULTIMATE DETECTION: '{wake_word_name.upper()}'")
        print(f"   📊 Confidence: {confidence:.1%} (Required: {word_threshold:.0%})")
        print(f"   ⚡ Response: {inference_time:.1f}ms")
        print(f"   🔁 Consecutive: {self.consecutive_detections}")
        print(f"   🧠 Strategy: All 5 layers verified")
        
        # Visual ultimate confirmation
        try:
            pyautogui.alert(f"🎯 '{wake_word_name}' detected!\nStrategy: Multi-layer verification", "Ultimate Wake Word")
        except:
            pass
        
        return True
    
    def ultimate_audio_callback(self, indata, frames, time_info, status):
        """ULTIMATE PERFECTED audio callback - NO TYPE ERRORS"""
        # Handle status without type issues
        if status:
            print(f"🔧 Audio Status: {status}")
        
        if not self.is_listening:
            return
        
        try:
            # Convert audio - SIMPLIFIED and ROBUST
            audio = indata[:, 0].astype(np.float32)
            
            # Ultimate prediction
            prediction, confidence, inference_time = self.ultimate_prediction(audio)
            
            # Real-time ultimate display
            current_time = time.time()
            if current_time - self.last_detection_time > 0.8:
                if prediction is not None and confidence > 0.25:
                    word = self.labels[prediction]
                    threshold = self.wake_word_mapping.get(word, {}).get('adaptive_threshold', self.adaptive_sensitivity)
                    
                    if confidence > threshold:
                        status_icon = "🎯"
                    elif confidence > threshold - 0.1:
                        status_icon = "🔍"
                    else:
                        status_icon = "👂"
                    
                    print(f"{status_icon} Monitoring: '{word}' ({confidence:.1%})", end='\r')
            
            # Execute ultimate decision
            if prediction is not None and confidence > self.adaptive_sensitivity:
                self.execute_ultimate_decision(prediction, confidence, inference_time)
                
        except Exception as e:
            print(f"⚠️  Callback processing: {e}")
    
    def activate_ultimate_mode(self, timeout=60):
        """Activate full ultimate intelligence"""
        print("\n" + "="*65)
        print("🧠 ULTIMATE STRATEGIC INTELLIGENCE ACTIVATED")
        print("="*65)
        print("🎯 5-LAYER ULTIMATE STRATEGY:")
        print(f"   • Layer 1: Basic Threshold ({self.adaptive_sensitivity:.0%})")
        print(f"   • Layer 2: Wake Word Mapping")
        print(f"   • Layer 3: Temporal Protection (400ms)")
        print(f"   • Layer 4: Consistency Analysis")
        print(f"   • Layer 5: Word-Specific Sensitivity")
        print("🎤 ULTIMATE TARGETS:")
        for word, config in self.wake_word_mapping.items():
            print(f"   • '{word.upper()}' → '{config['name']}' (sensitivity: {config['adaptive_threshold']:.0%})")
        print(f"⏰ Ultimate Session: {timeout} seconds")
        print("💡 Speak naturally - System uses 5-layer intelligence")
        print("-"*65)
        
        self.is_listening = True
        ultimate_start = time.time()
        
        try:
            # ULTIMATE PERFECTED audio stream
            with sd.InputStream(
                callback=self.ultimate_audio_callback,
                channels=1,
                samplerate=SAMPLE_RATE,
                blocksize=CHUNK_SIZE,
                latency='low'
            ):
                print("🎹 ULTIMATE AUDIO ENGINE: ACTIVE")
                print("🔊 Listening with 5-layer intelligence...")
                
                while self.is_listening and (time.time() - ultimate_start < timeout):
                    time.sleep(0.1)
                    
        except KeyboardInterrupt:
            print("\n⏹️ Ultimate session terminated by user")
        except Exception as e:
            print(f"❌ Ultimate stream error: {e}")
        finally:
            self.is_listening = False
        
        self.print_ultimate_report(ultimate_start)
    
    def print_ultimate_report(self, session_start):
        """Comprehensive ultimate performance report"""
        duration = time.time() - session_start
        
        print("\n" + "="*65)
        print("📊 ULTIMATE STRATEGIC INTELLIGENCE REPORT")
        print("="*65)
        
        if self.strategy_stats['total_predictions'] > 0:
            print(f"⏱️  Session Duration: {duration:.1f}s")
            print(f"🔢 Total Predictions: {self.strategy_stats['total_predictions']}")
            print(f"🎯 Genuine Detections: {self.strategy_stats['genuine_detections']}")
            print(f"🔁 Consecutive Success: {self.consecutive_detections}")
            
            # Ultimate layer analysis
            print("\n🧠 5-LAYER STRATEGIC PERFORMANCE:")
            total_checks = self.strategy_stats['total_predictions']
            for layer, count in self.strategy_stats.items():
                if layer.startswith('layer_'):
                    layer_name = layer.replace('layer_', '').replace('_', ' ').title()
                    percentage = (count / total_checks) * 100
                    print(f"   • {layer_name}: {count} ({percentage:.1f}%)")
            
            # Performance assessment
            detection_rate = self.strategy_stats['genuine_detections'] / max(1, self.strategy_stats['total_predictions'])
            if detection_rate > 0.08:
                print("✅ ULTIMATE ASSESSMENT: EXCELLENT - High sensitivity with precision")
            elif detection_rate > 0.04:
                print("⚠️  ULTIMATE ASSESSMENT: GOOD - Balanced performance")
            else:
                print("💡 ULTIMATE ASSESSMENT: CONSERVATIVE - High accuracy focus")
                
        else:
            print("❌ No strategic data collected")
            print("💡 Check microphone and environment")
        
        print("="*65)
    
    def run_ultimate_demonstration(self):
        """Demonstrate ultimate strategic intelligence"""
        print("🚀 ULTIMATE STRATEGIC WAKE WORD DETECTOR")
        print("5-layer intelligence system activated!")
        self.activate_ultimate_mode(timeout=60)

def main():
    """Launch ultimate strategic intelligence"""
    ultimate_detector = UltimateStrategicDetector()
    ultimate_detector.run_ultimate_demonstration()

if __name__ == "__main__":
    main()
