# final_optimized_assistant.py
import tensorflow as tf
import numpy as np
import time
import threading
import pyaudio
import queue
from collections import deque
from hybrid_model_router_optimized import Phase9EnhancedIntelligence

class FinalOptimizedAssistant:
    """
    FINAL OPTIMIZED ASSISTANT: Better noise filtering + adaptive thresholds
    """
    
    def __init__(self):
        print("🚀 INITIALIZING FINAL OPTIMIZED ASSISTANT...")
        
        # Core components
        self.hybrid_intelligence = Phase9EnhancedIntelligence()
        
        # Audio configuration
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.audio_format = pyaudio.paInt16
        self.audio_queue = queue.Queue()
        
        # ✅ OPTIMIZED: Higher confidence threshold + noise filtering
        self.wake_word_mappings = {
            'on': 'assistant',      # Primary wake word
            'yes': 'computer',      # Alternative wake word  
            'go': 'hey device'      # Secondary wake word
        }
        
        # ✅ OPTIMIZED: Higher thresholds to reduce false positives
        self.word_specific_thresholds = {
            'on': 0.75,    # 75% confidence for 'on' → 'assistant'
            'yes': 0.80,   # 80% confidence for 'yes' → 'computer'  
            'go': 0.85     # 85% confidence for 'go' → 'hey device'
        }
        
        # Strategic parameters
        self.detection_cooldown = 3.0  # Increased cooldown
        self.last_detection_time = 0
        self.command_count = 0
        
        # ✅ OPTIMIZED: Noise filtering
        self.energy_threshold = 0.005  # Minimum audio energy
        self.background_energy = 0.0
        self.background_samples = 0
        
        # Audio setup
        self.audio_interface = pyaudio.PyAudio()
        self.audio_stream = self.audio_interface.open(
            format=self.audio_format,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self._audio_callback
        )
        
        print("🎯 FINAL OPTIMIZED ASSISTANT READY!")
        print("   🔊 Enhanced Noise Filtering: ACTIVE")
        print("   📊 Higher Confidence Thresholds: 75-85%")
        print("   🔔 Primary: Say 'ON' clearly for 'assistant'")
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Audio callback"""
        audio_chunk = np.frombuffer(in_data, dtype=np.int16).astype(np.float32) / 32768.0
        self.audio_queue.put(audio_chunk)
        return (in_data, pyaudio.paContinue)
    
    def _calculate_audio_energy(self, audio_data):
        """Calculate audio energy for voice activity detection"""
        return np.mean(audio_data ** 2)
    
    def _update_background_noise(self, energy):
        """Update background noise estimate"""
        if self.background_samples < 100:  # First 100 samples for calibration
            self.background_energy = (self.background_energy * self.background_samples + energy) / (self.background_samples + 1)
            self.background_samples += 1
    
    def _is_likely_voice(self, audio_data, energy):
        """Check if audio is likely to be voice vs background noise"""
        # Skip if too quiet
        if energy < self.energy_threshold:
            return False
        
        # Skip if close to background noise level
        if self.background_samples >= 50 and energy < self.background_energy * 3:
            return False
        
        # Check for voice-like characteristics
        zero_crossings = np.sum(np.diff(np.signbit(audio_data)))
        zero_crossing_rate = zero_crossings / len(audio_data)
        
        # Voice typically has moderate zero-crossing rate
        return 0.05 < zero_crossing_rate < 0.5
    
    def _process_audio_optimized(self):
        """Process audio with enhanced noise filtering"""
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_detection_time < self.detection_cooldown:
            return None
        
        # Need at least 1 second of audio
        if len(self.audio_buffer) < self.sample_rate:
            return None
        
        # Use most recent 1 second
        processing_audio = self.audio_buffer[-self.sample_rate:]
        
        # Calculate audio energy
        energy = self._calculate_audio_energy(processing_audio)
        self._update_background_noise(energy)
        
        # Enhanced voice activity detection
        if not self._is_likely_voice(processing_audio, energy):
            return None
        
        try:
            # Get hybrid intelligence result
            result = self.hybrid_intelligence.process_audio_intelligently(processing_audio)
            
            # Extract KWS prediction
            wakeword_result = result.get('wakeword', {})
            predicted_class = wakeword_result.get('predicted_class', '')
            confidence = wakeword_result.get('confidence', 0.0)
            
            print(f"🔍 DETECTED: '{predicted_class}' with {confidence:.1%} confidence (Energy: {energy:.6f})")
            
            # Apply word-specific threshold
            if predicted_class in self.wake_word_mappings:
                required_threshold = self.word_specific_thresholds.get(predicted_class, 0.75)
                
                if confidence >= required_threshold:
                    # ✅ Valid detection!
                    self.last_detection_time = current_time
                    return {
                        'kws_keyword': predicted_class,
                        'mapped_wake_word': self.wake_word_mappings[predicted_class],
                        'confidence': confidence,
                        'emotion': result.get('emotion', {}).get('emotion', 'neutral'),
                        'audio_energy': energy,
                        'background_energy': self.background_energy
                    }
                else:
                    print(f"   📊 Below threshold: {confidence:.1%} < {required_threshold:.0%}")
            elif predicted_class:
                print(f"   🔍 Detected '{predicted_class}' but not in wake word mappings")
            
        except Exception as e:
            print(f"❌ Processing error: {e}")
        
        return None
    
    def _handle_detection(self, detection_result):
        """Handle successful detection"""
        self.command_count += 1
        
        print(f"\n🎯 COMMAND #{self.command_count} - GENUINE WAKE WORD!")
        print(f"   🔍 KWS Keyword: '{detection_result['kws_keyword']}'")
        print(f"   🔔 Mapped to: '{detection_result['mapped_wake_word']}'")
        print(f"   📊 Confidence: {detection_result['confidence']:.1%}")
        print(f"   🎭 Emotion: {detection_result['emotion']}")
        print(f"   🔊 Audio Energy: {detection_result['audio_energy']:.6f}")
        
        # Response based on mapped wake word
        responses = {
            'assistant': "Hello! I'm your assistant. How can I help you?",
            'computer': "Computer activated. Ready for your command.",
            'hey device': "Device listening. What would you like to do?"
        }
        
        response = responses.get(detection_result['mapped_wake_word'], "Hello!")
        print(f"   💬 Response: {response}")
        print(f"   ⏱️  Next detection in {self.detection_cooldown}s")
    
    def start_final(self):
        """Start the final optimized assistant"""
        print("\n" + "="*60)
        print("🎧 FINAL OPTIMIZED ASSISTANT - ENHANCED NOISE FILTERING")
        print("="*60)
        print("   🔊 Listening for CLEAR 'ON', 'YES', or 'GO'...")
        print("   🔔 Primary: Say 'ON' clearly for 'assistant'")
        print("   📊 Confidence Threshold: 75-85% (reduces false positives)")
        print("   🎯 Background Noise Filtering: ACTIVE")
        print("   🛑 Press Ctrl+C to exit")
        print("="*60)
        
        self.audio_stream.start_stream()
        
        # Audio buffer (2 seconds)
        self.audio_buffer = np.array([], dtype=np.float32)
        buffer_size = self.sample_rate * 2
        
        try:
            while True:
                try:
                    # Get audio data
                    audio_chunk = self.audio_queue.get(timeout=0.1)
                    self.audio_buffer = np.concatenate([self.audio_buffer, audio_chunk])
                    
                    # Maintain buffer size
                    if len(self.audio_buffer) > buffer_size:
                        self.audio_buffer = self.audio_buffer[-buffer_size:]
                    
                    # Process audio with enhanced filtering
                    detection_result = self._process_audio_optimized()
                    
                    if detection_result:
                        self._handle_detection(detection_result)
                    
                    # Status display
                    cooldown_left = max(0, self.detection_cooldown - (time.time() - self.last_detection_time))
                    bg_info = f"BG: {self.background_energy:.6f}" if self.background_samples >= 50 else "Calibrating..."
                    
                    if cooldown_left > 0:
                        print(f"   ⏳ Cooldown: {cooldown_left:.1f}s | {bg_info} | Commands: {self.command_count}", end='\r')
                    else:
                        print(f"   ✅ Ready | {bg_info} | Commands: {self.command_count} | Say 'ON' clearly...", end='\r')
                        
                except queue.Empty:
                    # Update status
                    cooldown_left = max(0, self.detection_cooldown - (time.time() - self.last_detection_time))
                    bg_info = f"BG: {self.background_energy:.6f}" if self.background_samples >= 50 else "Calibrating..."
                    
                    if cooldown_left > 0:
                        print(f"   ⏳ Cooldown: {cooldown_left:.1f}s | {bg_info} | Commands: {self.command_count}", end='\r')
                    else:
                        print(f"   ✅ Ready | {bg_info} | Commands: {self.command_count} | Say 'ON' clearly...", end='\r')
                    continue
                    
        except KeyboardInterrupt:
            self.stop_final()
    
    def stop_final(self):
        """Stop the assistant"""
        print("\n\n🛑 SHUTTING DOWN FINAL OPTIMIZED ASSISTANT...")
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.audio_interface.terminate()
        
        print(f"📊 SESSION SUMMARY:")
        print(f"   Total Valid Commands: {self.command_count}")
        print(f"   Background Energy: {self.background_energy:.6f}")
        print(f"   Calibration Samples: {self.background_samples}")
        print("✅ Final Optimized Assistant: SHUTDOWN COMPLETE")

if __name__ == "__main__":
    assistant = FinalOptimizedAssistant()
    assistant.start_final()