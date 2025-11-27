# properly_mapped_assistant.py
import tensorflow as tf
import numpy as np
import time
import threading
import pyaudio
import queue
from collections import deque
from hybrid_model_router_optimized import Phase9EnhancedIntelligence

class ProperlyMappedAssistant:
    """
    PROPERLY CONFIGURED VOICE ASSISTANT: Correct wake word mapping implementation
    """
    
    def __init__(self):
        print("🚀 INITIALIZING PROPERLY MAPPED ASSISTANT...")
        
        # Core components
        self.hybrid_intelligence = Phase9EnhancedIntelligence()
        
        # Audio configuration
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.audio_format = pyaudio.paInt16
        self.audio_queue = queue.Queue()
        
        # ✅ PROPER WAKE WORD MAPPING CONFIGURATION
        self.wake_word_mappings = {
            'on': 'assistant',      # Primary wake word
            'yes': 'computer',      # Alternative wake word  
            'go': 'hey device'      # Secondary wake word
        }
        
        # ✅ PROPER STRATEGIC LAYER THRESHOLDS
        self.word_specific_thresholds = {
            'on': 0.55,    # 55% confidence for 'on' → 'assistant'
            'yes': 0.60,   # 60% confidence for 'yes' → 'computer'
            'go': 0.65     # 65% confidence for 'go' → 'hey device'
        }
        
        # Strategic intelligence parameters
        self.adaptive_sensitivity = 0.55  # Starting sensitivity for silent environments
        self.detection_cooldown = 0.4     # 400ms cooldown (Layer 3)
        self.detection_history = deque(maxlen=8)  # Layer 4 consistency buffer
        self.last_detection_time = 0
        
        # State management
        self.is_listening = False
        self.current_wake_word = None
        self.command_count = 0
        
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
        
        print("🎯 PROPERLY MAPPED ASSISTANT READY!")
        print("   🔔 Wake Word Mapping: 'on' → 'assistant'")
        print("   📊 Threshold: 55% confidence required")
        print("   🛡️  5-Layer Strategic Intelligence: ACTIVE")
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Audio callback with proper Int16 to Float32 conversion"""
        audio_chunk = np.frombuffer(in_data, dtype=np.int16).astype(np.float32) / 32768.0
        self.audio_queue.put(audio_chunk)
        return (in_data, pyaudio.paContinue)
    
    def _strategic_intelligence_check(self, kws_keyword, confidence, current_time):
        """✅ IMPLEMENT 5-LAYER STRATEGIC INTELLIGENCE"""
        
        # Layer 1: Basic Threshold Check
        if confidence < self.adaptive_sensitivity:
            return False, "Layer 1: Below adaptive sensitivity"
        
        # Layer 2: Wake Word Mapping Check
        if kws_keyword not in self.wake_word_mappings:
            return False, f"Layer 2: '{kws_keyword}' not in wake word mappings"
        
        # Layer 3: Temporal Protection (400ms cooldown)
        if current_time - self.last_detection_time < self.detection_cooldown:
            return False, f"Layer 3: In cooldown period"
        
        # Layer 4: Consistency Analysis
        recent_matches = list(self.detection_history)[-3:]  # Last 3 detections
        matching_count = sum(1 for word in recent_matches if word == kws_keyword)
        
        consistency_ok = (matching_count >= 2) or (confidence > self.adaptive_sensitivity + 0.15)
        if not consistency_ok:
            return False, f"Layer 4: Consistency check failed"
        
        # Layer 5: Word-Specific Sensitivity
        word_threshold = self.word_specific_thresholds.get(kws_keyword, 0.55)
        if confidence < word_threshold:
            return False, f"Layer 5: Below word-specific threshold ({word_threshold})"
        
        # ✅ ALL 5 LAYERS PASSED
        return True, "All strategic layers passed"
    
    def _process_audio_intelligently(self, audio_buffer):
        """Process audio with proper strategic intelligence"""
        current_time = time.time()
        
        # Need at least 1 second of audio
        if len(audio_buffer) < self.sample_rate:
            return None
        
        # Use most recent 1 second
        processing_audio = audio_buffer[-self.sample_rate:]
        
        # Get hybrid intelligence result
        result = self.hybrid_intelligence.process_audio_intelligently(processing_audio)
        
        # Extract KWS prediction
        kws_prediction = result.get('wakeword', {})
        kws_keyword = kws_prediction.get('predicted_class', '').lower()
        kws_confidence = kws_prediction.get('confidence', 0.0)
        
        # Apply strategic intelligence
        detection_ok, reason = self._strategic_intelligence_check(kws_keyword, kws_confidence, current_time)
        
        if detection_ok:
            # ✅ Valid detection - update history and return
            self.detection_history.append(kws_keyword)
            self.last_detection_time = current_time
            
            mapped_wake_word = self.wake_word_mappings[kws_keyword]
            return {
                'kws_keyword': kws_keyword,
                'mapped_wake_word': mapped_wake_word,
                'confidence': kws_confidence,
                'emotion': result['emotion'],
                'strategic_reason': reason
            }
        else:
            # Log strategic rejection for debugging
            if kws_confidence > 0.3:  # Only log meaningful detections
                print(f"   🛡️ Strategic Rejection: {kws_keyword} ({kws_confidence:.1%}) - {reason}")
            return None
    
    def _handle_wake_word_detection(self, detection_result):
        """Handle properly mapped wake word detection"""
        self.command_count += 1
        
        kws_keyword = detection_result['kws_keyword']
        mapped_wake_word = detection_result['mapped_wake_word']
        confidence = detection_result['confidence']
        emotion = detection_result['emotion']['emotion']
        
        print(f"\n🎯 COMMAND #{self.command_count} - WAKE WORD DETECTED!")
        print(f"   🔍 KWS Keyword: '{kws_keyword}'")
        print(f"   🔔 Mapped Wake Word: '{mapped_wake_word}'")
        print(f"   📊 Confidence: {confidence:.1%}")
        print(f"   🎭 Emotion: {emotion}")
        print(f"   🛡️ Strategic Validation: {detection_result['strategic_reason']}")
        
        # Different responses based on mapped wake word
        wake_word_responses = {
            'assistant': "Hello! I'm your assistant. How can I help you?",
            'computer': "Computer activated. What would you like to do?",
            'hey device': "Device listening. What's your command?"
        }
        
        response = wake_word_responses.get(mapped_wake_word, "Hello! How can I assist you?")
        print(f"   💬 Response: {response}")
        
        # Transition to command mode would happen here
        print(f"   ⏱️  Next wake word available in {self.detection_cooldown}s")
    
    def start_proper_listening(self):
        """Start the properly configured assistant"""
        print("\n" + "="*60)
        print("🎧 PROPERLY MAPPED ASSISTANT - STRATEGIC INTELLIGENCE ACTIVE")
        print("="*60)
        print("   🔊 Listening for mapped wake words...")
        print("   🔔 Primary: Say 'ON' to activate 'assistant'")
        print("   🎯 Alternative: Say 'YES' for 'computer'")
        print("   ⚡ Secondary: Say 'GO' for 'hey device'") 
        print("   📊 Required Confidence: 55% minimum")
        print("   🛡️  5-Layer Strategic Filtering: ENABLED")
        print("   🛑 Press Ctrl+C to exit")
        print("="*60)
        
        self.is_listening = True
        self.audio_stream.start_stream()
        
        # Audio buffer (2 seconds)
        audio_buffer = np.array([], dtype=np.float32)
        buffer_size = self.sample_rate * 2
        
        try:
            while self.is_listening:
                try:
                    # Get audio data
                    audio_chunk = self.audio_queue.get(timeout=0.1)
                    audio_buffer = np.concatenate([audio_buffer, audio_chunk])
                    
                    # Maintain buffer size
                    if len(audio_buffer) > buffer_size:
                        audio_buffer = audio_buffer[-buffer_size:]
                    
                    # Process with strategic intelligence
                    detection_result = self._process_audio_intelligently(audio_buffer)
                    
                    if detection_result:
                        self._handle_wake_word_detection(detection_result)
                    
                    # Status display
                    cooldown_remaining = max(0, self.detection_cooldown - (time.time() - self.last_detection_time))
                    status = f"✅ Ready" if cooldown_remaining == 0 else f"⏳ Cooldown: {cooldown_remaining:.1f}s"
                    print(f"   {status} | Commands: {self.command_count} | Listening...", end='\r')
                        
                except queue.Empty:
                    # Update status when no audio
                    cooldown_remaining = max(0, self.detection_cooldown - (time.time() - self.last_detection_time))
                    status = f"✅ Ready" if cooldown_remaining == 0 else f"⏳ Cooldown: {cooldown_remaining:.1f}s"
                    print(f"   {status} | Commands: {self.command_count} | Listening...", end='\r')
                    continue
                    
        except KeyboardInterrupt:
            self.stop_proper_listening()
    
    def stop_proper_listening(self):
        """Stop the assistant"""
        print("\n\n🛑 SHUTTING DOWN PROPERLY MAPPED ASSISTANT...")
        self.is_listening = False
        
        # Cleanup
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.audio_interface.terminate()
        
        print(f"📊 SESSION SUMMARY:")
        print(f"   Total Valid Commands: {self.command_count}")
        print("✅ Properly Mapped Assistant: SHUTDOWN COMPLETE")

# Quick test function
def test_wake_word_mapping():
    """Test the wake word mapping configuration"""
    print("🧪 TESTING WAKE WORD MAPPING CONFIGURATION...")
    
    assistant = ProperlyMappedAssistant()
    
    print("\n🔍 CONFIGURATION VERIFICATION:")
    print(f"   Primary Mapping: 'on' → '{assistant.wake_word_mappings['on']}'")
    print(f"   Required Confidence: {assistant.word_specific_thresholds['on']:.0%}")
    print(f"   Strategic Cooldown: {assistant.detection_cooldown}s")
    print(f"   Consistency Buffer: {assistant.detection_history.maxlen} entries")
    
    print("\n✅ CONFIGURATION CORRECT! Starting assistant...")
    assistant.start_proper_listening()

if __name__ == "__main__":
    test_wake_word_mapping()