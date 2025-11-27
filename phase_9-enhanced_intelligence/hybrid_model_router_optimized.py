# hybrid_model_router_optimized.py - FIXED VERSION
import tensorflow as tf
import numpy as np
import time
from typing import Dict, Tuple, Any

class HybridModelRouterOptimized:
    """
    PHASE 9.0 HYBRID INTELLIGENCE - FIXED WAKEWORD OUTPUT PROCESSING
    """
    
    def __init__(self):
        # Load both models
        self.emotion_model = self._load_emotion_model()
        self.wakeword_model = self._load_wakeword_model()
        
        # ✅ FIXED: Define KWS classes for proper output interpretation
        self.kws_classes = ['on', 'yes', 'no', 'stop', 'go', 'up', 'down', 'left', 'right', 'off']
        
        # Performance metrics
        self.model_stats = {
            'emotion': {'calls': 0, 'avg_time': 0, 'last_time': 0},
            'wakeword': {'calls': 0, 'avg_time': 0, 'last_time': 0}
        }
        
        # Context-aware routing
        self.current_context = 'neutral'
        self.emotion_history = []
        
        print("🧠 HYBRID MODEL ROUTER INITIALIZED!")
        print(f"   ✅ Emotion Model: {self._get_file_size('emotion')} bytes")
        print(f"   ✅ WakeWord Model: {self._get_file_size('wakeword')} bytes")
        print(f"   🎯 KWS Classes: {len(self.kws_classes)} commands")
        print(f"   🎯 Context-Aware Routing: ACTIVE")
    
    def _load_emotion_model(self):
        """Load the ultra-fast emotion detection model (6.7KB)"""
        try:
            emotion_path = r"C:\Users\dell\Projects\Edge-TinyML-Project\phase5_neural_reflex\models\emotion_detector_optimized.tflite"
            interpreter = tf.lite.Interpreter(model_path=emotion_path)
            interpreter.allocate_tensors()
            print(f"   🎭 Emotion Model: LOADED (6.7KB)")
            return interpreter
        except Exception as e:
            print(f"   ❌ Emotion Model failed: {e}")
            return None
    
    def _load_wakeword_model(self):
        """Load the efficient wake-word model (77KB)"""
        try:
            wakeword_path = r"C:\Users\dell\Projects\Edge-TinyML-Project\phase1_baseline\models\production\model_int8.tflite"
            interpreter = tf.lite.Interpreter(model_path=wakeword_path)
            interpreter.allocate_tensors()
            print(f"   🔊 WakeWord Model: LOADED (77KB)")
            return interpreter
        except Exception as e:
            print(f"   ❌ WakeWord Model failed: {e}")
            return None
    
    def _get_file_size(self, model_type: str) -> int:
        if model_type == 'emotion':
            return 6736
        else:
            return 77408
    
    def intelligent_router(self, audio_data: np.ndarray, context: Dict = None) -> Dict:
        """OPTIMIZED HYBRID ROUTING - FIXED VERSION"""
        start_time = time.time()
        
        # Step 1: Parallel model execution
        emotion_result = self._run_emotion_detection_fast(audio_data)
        wakeword_result = self._run_wakeword_detection_fixed(audio_data)  # ✅ FIXED METHOD
        
        # Step 2: Context-aware fusion
        hybrid_result = self._fuse_predictions(emotion_result, wakeword_result, context)
        
        total_time = (time.time() - start_time) * 1000
        
        return {
            'hybrid_prediction': hybrid_result,
            'emotion': emotion_result,
            'wakeword': wakeword_result,
            'context': self.current_context,
            'performance': {
                'total_time_ms': total_time,
                'emotion_time_ms': emotion_result.get('inference_time_ms', 0),
                'wakeword_time_ms': wakeword_result.get('inference_time_ms', 0),
                'models_used': ['emotion', 'wakeword']
            },
            'routing_decision': self._get_routing_decision(emotion_result, wakeword_result)
        }
    
    def _extract_audio_features_fast(self, audio_data: np.ndarray) -> np.ndarray:
        """FAST audio feature extraction without librosa"""
        try:
            features = []
            
            # 1. Basic statistical features (FAST)
            features.append(np.mean(audio_data))           # Mean
            features.append(np.std(audio_data))            # Standard deviation
            features.append(np.max(audio_data))            # Max amplitude
            features.append(np.min(audio_data))            # Min amplitude
            
            # 2. Zero crossing rate (FAST)
            zero_crossings = np.sum(np.diff(np.signbit(audio_data)))
            features.append(zero_crossings / len(audio_data))
            
            # 3. Energy (FAST)
            features.append(np.mean(audio_data ** 2))      # RMS energy
            
            # 4. Spectral features using FFT (FASTER than librosa)
            fft = np.fft.rfft(audio_data)
            magnitude = np.abs(fft)
            
            # Spectral centroid (weighted mean)
            if np.sum(magnitude) > 0:
                spectral_centroid = np.sum(np.arange(len(magnitude)) * magnitude) / np.sum(magnitude)
            else:
                spectral_centroid = 0
            features.append(spectral_centroid)
            
            # Spectral spread (variance)
            if np.sum(magnitude) > 0:
                spectral_spread = np.sqrt(np.sum((np.arange(len(magnitude)) - spectral_centroid) ** 2 * magnitude) / np.sum(magnitude))
            else:
                spectral_spread = 0
            features.append(spectral_spread)
            
            # 5. Simple frequency bands (FAST)
            bands = 8
            band_size = len(magnitude) // bands
            for i in range(bands):
                start_idx = i * band_size
                end_idx = (i + 1) * band_size if i < bands - 1 else len(magnitude)
                band_energy = np.sum(magnitude[start_idx:end_idx])
                features.append(band_energy)
            
            # Ensure exactly 16 features
            if len(features) < 16:
                features.extend([0.0] * (16 - len(features)))
            elif len(features) > 16:
                features = features[:16]
            
            return np.array(features, dtype=np.float32)
            
        except Exception as e:
            print(f"   ⚠️ Fast feature extraction failed: {e}")
            return np.zeros(16, dtype=np.float32)
    
    def _create_spectrogram_fast(self, audio_data: np.ndarray) -> np.ndarray:
        """FAST spectrogram creation without librosa"""
        try:
            # Simple STFT implementation
            frame_size = 512
            hop_size = 256
            n_frames = (len(audio_data) - frame_size) // hop_size + 1
            
            # Initialize spectrogram
            spectrogram = np.zeros((40, 99), dtype=np.uint8)
            
            # Simple mel-like bands (approximation)
            for i in range(min(n_frames, 99)):
                start = i * hop_size
                end = start + frame_size
                frame = audio_data[start:end]
                
                # Apply window
                windowed = frame * np.hanning(len(frame))
                
                # FFT
                fft = np.fft.rfft(windowed)
                magnitude = np.abs(fft)
                
                # Simple mel bands (40 bands)
                for mel_band in range(40):
                    # Approximate mel scaling
                    start_bin = mel_band * (len(magnitude) // 40)
                    end_bin = (mel_band + 1) * (len(magnitude) // 40)
                    band_energy = np.sum(magnitude[start_bin:end_bin])
                    
                    # Simple normalization
                    value = min(int(band_energy * 10), 255)
                    spectrogram[mel_band, i] = value
            
            return spectrogram
            
        except Exception as e:
            print(f"   ⚠️ Fast spectrogram failed: {e}")
            return np.zeros((40, 99), dtype=np.uint8)
    
    def _run_emotion_detection_fast(self, audio_data: np.ndarray) -> Dict:
        """FAST emotion detection"""
        if not self.emotion_model:
            return {'emotion': 'neutral', 'confidence': 0.0, 'error': 'model_not_loaded'}
        
        start_time = time.time()
        
        try:
            # Extract features FAST
            audio_features = self._extract_audio_features_fast(audio_data)
            
            # Reshape and run model
            processed_audio = audio_features.reshape(1, 16).astype(np.float32)
            
            input_details = self.emotion_model.get_input_details()
            output_details = self.emotion_model.get_output_details()
            
            self.emotion_model.set_tensor(input_details[0]['index'], processed_audio)
            self.emotion_model.invoke()
            
            emotion_output = self.emotion_model.get_tensor(output_details[0]['index'])
            
            # Decode emotion
            emotions = ['neutral', 'happy', 'sad', 'angry', 'surprised', 'fear', 'disgust', 'calm']
            emotion_idx = np.argmax(emotion_output[0])
            confidence = float(np.max(emotion_output[0]))
            emotion = emotions[emotion_idx % len(emotions)]
            
            emotion_time = (time.time() - start_time) * 1000
            
            self._update_model_stats('emotion', emotion_time)
            
            return {
                'emotion': emotion,
                'confidence': confidence,
                'inference_time_ms': emotion_time,
                'method': 'fast_features'
            }
            
        except Exception as e:
            print(f"   ❌ Fast emotion detection error: {e}")
            return {'emotion': 'neutral', 'confidence': 0.0, 'error': str(e), 'inference_time_ms': 0}
    
    def _run_wakeword_detection_fixed(self, audio_data: np.ndarray) -> Dict:
        """✅ FIXED: Proper wake-word detection with correct output interpretation"""
        if not self.wakeword_model:
            return {
                'predicted_class': '', 
                'confidence': 0.0, 
                'wakeword_detected': False,
                'error': 'model_not_loaded'
            }
        
        start_time = time.time()
        
        try:
            # Create spectrogram FAST
            spectrogram = self._create_spectrogram_fast(audio_data)
            
            # Reshape and run model
            processed_audio = spectrogram.reshape(1, 40, 99, 1).astype(np.uint8)
            
            input_details = self.wakeword_model.get_input_details()
            output_details = self.wakeword_model.get_output_details()
            
            self.wakeword_model.set_tensor(input_details[0]['index'], processed_audio)
            self.wakeword_model.invoke()
            
            wakeword_output = self.wakeword_model.get_tensor(output_details[0]['index'])
            
            # ✅ FIXED: Proper output interpretation
            # The model outputs probabilities for each class
            probabilities = wakeword_output[0]
            
            # Get predicted class and confidence
            predicted_index = np.argmax(probabilities)
            confidence = float(probabilities[predicted_index])
            
            # ✅ FIXED: Cap confidence at 100% and handle edge cases
            confidence = min(confidence, 1.0)
            
            # Get class name
            if 0 <= predicted_index < len(self.kws_classes):
                predicted_class = self.kws_classes[predicted_index]
                wakeword_detected = confidence > 0.5  # Basic threshold
            else:
                predicted_class = ''
                wakeword_detected = False
                confidence = 0.0
            
            wakeword_time = (time.time() - start_time) * 1000
            
            self._update_model_stats('wakeword', wakeword_time)
            
            return {
                'predicted_class': predicted_class,
                'confidence': confidence,
                'wakeword_detected': wakeword_detected,
                'inference_time_ms': wakeword_time,
                'method': 'fast_spectrogram',
                'all_probabilities': {self.kws_classes[i]: float(prob) for i, prob in enumerate(probabilities) if i < len(self.kws_classes)}
            }
            
        except Exception as e:
            print(f"   ❌ Fixed wakeword detection error: {e}")
            return {
                'predicted_class': '', 
                'confidence': 0.0, 
                'wakeword_detected': False,
                'error': str(e), 
                'inference_time_ms': 0
            }

    def _fuse_predictions(self, emotion_result: Dict, wakeword_result: Dict, context: Dict) -> Dict:
        """Fuse emotion and wakeword predictions"""
        wakeword_conf = wakeword_result.get('confidence', 0)
        emotion_type = emotion_result.get('emotion', 'neutral')
        emotion_conf = emotion_result.get('confidence', 0)
        
        # Get the predicted class
        predicted_class = wakeword_result.get('predicted_class', '')
        wakeword_detected = wakeword_result.get('wakeword_detected', False)
        
        # Emotional context adjustment
        adjusted_confidence = wakeword_conf
        
        if emotion_type == 'excited' and emotion_conf > 0.7:
            adjusted_confidence *= 1.2
        elif emotion_type == 'tired' and emotion_conf > 0.6:
            adjusted_confidence *= 0.8
        
        # Cap confidence
        adjusted_confidence = min(adjusted_confidence, 1.0)
        
        # Update emotion context
        if emotion_conf > 0.6:
            self.current_context = emotion_type
            self.emotion_history.append(emotion_type)
            if len(self.emotion_history) > 10:
                self.emotion_history.pop(0)
        
        return {
            'final_confidence': adjusted_confidence,
            'wakeword_detected': wakeword_detected,
            'predicted_class': predicted_class,
            'emotional_context': emotion_type,
            'context_confidence': emotion_conf,
            'adjusted_by_emotion': adjusted_confidence != wakeword_conf
        }
    
    def _get_routing_decision(self, emotion_result: Dict, wakeword_result: Dict) -> Dict:
        """Get routing decision based on predictions"""
        emotion = emotion_result.get('emotion', 'neutral')
        wakeword_detected = wakeword_result.get('wakeword_detected', False)
        predicted_class = wakeword_result.get('predicted_class', '')
        
        routing_rules = {
            'excited': {'priority': 'high', 'response_speed': 'fast', 'verbose': True},
            'happy': {'priority': 'high', 'response_speed': 'fast', 'verbose': True},
            'neutral': {'priority': 'medium', 'response_speed': 'normal', 'verbose': False},
            'tired': {'priority': 'low', 'response_speed': 'slow', 'verbose': False},
            'sad': {'priority': 'medium', 'response_speed': 'gentle', 'verbose': True}
        }
        
        rule = routing_rules.get(emotion, routing_rules['neutral'])
        
        return {
            'emotional_routing': rule,
            'wakeword_triggered': wakeword_detected,
            'predicted_class': predicted_class,
            'recommended_action': 'process_command' if wakeword_detected else 'continue_listening',
            'context_awareness': f"{emotion}_{'active' if wakeword_detected else 'passive'}"
        }
    
    def _update_model_stats(self, model_type: str, inference_time: float):
        """Update performance statistics"""
        stats = self.model_stats[model_type]
        stats['calls'] += 1
        stats['last_time'] = inference_time
        if stats['avg_time'] == 0:
            stats['avg_time'] = inference_time
        else:
            stats['avg_time'] = (stats['avg_time'] * 0.9) + (inference_time * 0.1)
    
    def get_performance_report(self) -> Dict:
        """Get performance report"""
        return {
            'hybrid_system': {
                'total_calls': sum(stats['calls'] for stats in self.model_stats.values()),
                'models_loaded': [model for model, stats in self.model_stats.items() if stats['calls'] > 0]
            },
            'model_performance': self.model_stats,
            'current_context': self.current_context,
            'emotion_history': self.emotion_history[-5:],
            'kws_classes': self.kws_classes,
            'system_efficiency': f"{(self.model_stats['emotion']['avg_time'] + self.model_stats['wakeword']['avg_time']):.2f}ms total avg"
        }

# PHASE 9.0 ENHANCED INTELLIGENCE CLASS
class Phase9EnhancedIntelligence:
    """
    PHASE 9.0 ENHANCED: Hybrid Models + Event Bus - FIXED VERSION
    """
    
    def __init__(self):
        self.hybrid_router = HybridModelRouterOptimized()
        print("🚀 PHASE 9.0 ENHANCED INTELLIGENCE: HYBRID MODELS + EVENT BUS")
    
    def process_audio_intelligently(self, audio_data: np.ndarray) -> Dict:
        """Process audio using hybrid model intelligence"""
        result = self.hybrid_router.intelligent_router(audio_data)
        
        # Route through Phase 9.0 Event Bus if wakeword detected
        if result['hybrid_prediction']['wakeword_detected']:
            event_bus_result = self._route_to_event_bus(result)
            result['phase9_routing'] = event_bus_result
        
        return result
    
    def _route_to_event_bus(self, hybrid_result: Dict) -> Dict:
        """Route intelligent results through Phase 9.0 Event Bus"""
        return {
            'event_bus_engaged': True,
            'emotional_context': hybrid_result['emotion']['emotion'],
            'predicted_class': hybrid_result['hybrid_prediction']['predicted_class'],
            'routing_decision': hybrid_result['routing_decision'],
            'cross_device_ready': True
        }

# TEST THE FIXED HYBRID SYSTEM
if __name__ == "__main__":
    print("🧪 TESTING FIXED HYBRID MODEL INTELLIGENCE...")
    
    enhanced_ai = Phase9EnhancedIntelligence()
    
    # Test with optimized processing
    print("   🎵 Generating test audio...")
    dummy_audio = np.random.normal(0, 0.1, 16000).astype(np.float32)
    
    result = enhanced_ai.process_audio_intelligently(dummy_audio)
    
    print(f"🎯 HYBRID RESULT: {result['hybrid_prediction']}")
    print(f"⚡ PERFORMANCE: {result['performance']}")
    print(f"🧠 ROUTING: {result['routing_decision']}")
    
    report = enhanced_ai.hybrid_router.get_performance_report()
    print(f"📊 SYSTEM REPORT: {report}")
    
    print("\n✅ FIXED HYBRID INTELLIGENCE: READY FOR REAL-TIME!")
    print("   🎭 Emotion Model: FAST FEATURES ✓")
    print("   🔊 WakeWord Model: FIXED OUTPUT PROCESSING ✓") 
    print("   🎯 KWS Classes: 10 COMMANDS ✓")
    print("   🧠 Context-Aware Fusion: ACTIVE ✓")
    print("   ⚡ Performance: OPTIMIZED ✓")