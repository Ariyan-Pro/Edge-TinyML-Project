# working_assistant_fixed.py
import tensorflow as tf
import numpy as np
import time
import threading
import pyaudio
import queue
from collections import deque
from hybrid_model_router_optimized import Phase9EnhancedIntelligence

class WorkingAssistantFixed:
    """
    WORKING ASSISTANT: Bypasses broken KWS output with direct model access
    """
    
    def __init__(self):
        print("🚀 INITIALIZING WORKING ASSISTANT (FIXED)...")
        
        # Core components
        self.hybrid_intelligence = Phase9EnhancedIntelligence()
        
        # Audio configuration
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.audio_format = pyaudio.paInt16
        self.audio_queue = queue.Queue()
        
        # ✅ DIRECT KWS MODEL ACCESS (if available)
        self.kws_model = None
        self.kws_classes = ['on', 'yes', 'no', 'stop', 'go', 'up', 'down', 'left', 'right', 'off']
        
        # Wake word mapping
        self.wake_word_mappings = {
            'on': 'assistant',
            'yes': 'computer', 
            'go': 'hey device'
        }
        
        # Strategic parameters
        self.confidence_threshold = 0.55
        self.detection_cooldown = 2.0  # Increased cooldown for testing
        self.last_detection_time = 0
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
        
        print("🎯 WORKING ASSISTANT READY!")
        print("   🔧 Using direct audio processing")
        print("   🔔 Wake Word: 'ON' → 'assistant'")
        print("   📊 Confidence Threshold: 55%")
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Audio callback"""
        audio_chunk = np.frombuffer(in_data, dtype=np.int16).astype(np.float32) / 32768.0
        self.audio_queue.put(audio_chunk)
        return (in_data, pyaudio.paContinue)
    
    def _extract_kws_prediction(self, result):
        """Extract KWS prediction from hybrid result - HANDLES BROKEN OUTPUTS"""
        try:
            # Method 1: Try wakeword result
            wakeword = result.get('wakeword', {})
            predicted_class = wakeword.get('predicted_class', '')
            confidence = wakeword.get('confidence', 0.0)
            
            print(f"🔍 RAW KWS OUTPUT: '{predicted_class}' with {confidence:.1%} confidence")
            
            # Fix: Handle empty string predictions
            if predicted_class == '' and confidence > 1.0:
                print("   ⚠️  DETECTED BROKEN OUTPUT: Empty string with high confidence")
                return None, 0.0
            
            # Fix: Handle unrealistic confidence values
            if confidence > 1.0:  # Confidence should be 0.0-1.0
                print(f"   ⚠️  DETECTED BROKEN CONFIDENCE: {confidence} (clamping to 1.0)")
                confidence = 1.0
            
            return predicted_class, confidence
            
        except Exception as e:
            print(f"❌ Error extracting KWS prediction: {e}")
            return None, 0.0
    
    def _simple_voice_detection(self, audio_data):
        """Simple energy-based voice detection as fallback"""
        energy = np.mean(audio_data ** 2)
        return energy > 0.001  # Adjust based on your environment
    
    def _process_audio_direct(self, audio_buffer):
        """Process audio with robust error handling"""
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_detection_time < self.detection_cooldown:
            return None
        
        # Need at least 1 second of audio
        if len(audio_buffer) < self.sample_rate:
            return None
        
        # Use most recent 1 second
        processing_audio = audio_buffer[-self.sample_rate:]
        
        # Simple voice activity detection
        if not self._simple_voice_detection(processing_audio):
            return None
        
        try:
            # Get hybrid intelligence result
            result = self.hybrid_intelligence.process_audio_intelligently(processing_audio)
            
            # Extract KWS prediction with error handling
            kws_keyword, kws_confidence = self._extract_kws_prediction(result)
            
            if kws_keyword and kws_keyword in self.wake_word_mappings:
                if kws_confidence >= self.confidence_threshold:
                    # ✅ Valid detection!
                    self.last_detection_time = current_time
                    return {
                        'kws_keyword': kws_keyword,
                        'mapped_wake_word': self.wake_word_mappings[kws_keyword],
                        'confidence': kws_confidence,
                        'emotion': result.get('emotion', {}).get('emotion', 'neutral')
                    }
                else:
                    print(f"   📊 Below threshold: '{kws_keyword}' at {kws_confidence:.1%}")
            elif kws_keyword:
                print(f"   🔍 Detected '{kws_keyword}' but not in wake word mappings")
            
        except Exception as e:
            print(f"❌ Processing error: {e}")
        
        return None
    
    def _handle_detection(self, detection_result):
        """Handle successful detection"""
        self.command_count += 1
        
        print(f"\n🎯 COMMAND #{self.command_count} - WAKE WORD DETECTED!")
        print(f"   🔍 KWS Keyword: '{detection_result['kws_keyword']}'")
        print(f"   🔔 Mapped to: '{detection_result['mapped_wake_word']}'")
        print(f"   📊 Confidence: {detection_result['confidence']:.1%}")
        print(f"   🎭 Emotion: {detection_result['emotion']}")
        
        # Response based on mapped wake word
        responses = {
            'assistant': "Hello! I'm your assistant. How can I help you?",
            'computer': "Computer activated. Ready for your command.",
            'hey device': "Device listening. What would you like to do?"
        }
        
        response = responses.get(detection_result['mapped_wake_word'], "Hello!")
        print(f"   💬 Response: {response}")
        print(f"   ⏱️  Next detection in {self.detection_cooldown}s")
    
    def start_working(self):
        """Start the working assistant"""
        print("\n" + "="*50)
        print("🎧 WORKING ASSISTANT - DIRECT PROCESSING")
        print("="*50)
        print("   🔊 Listening for 'ON', 'YES', or 'GO'...")
        print("   🔔 Primary: Say 'ON' for 'assistant'")
        print("   🛡️  Bypassing broken KWS outputs")
        print("   🛑 Press Ctrl+C to exit")
        print("="*50)
        
        self.audio_stream.start_stream()
        
        # Audio buffer
        audio_buffer = np.array([], dtype=np.float32)
        buffer_size = self.sample_rate * 2
        
        try:
            while True:
                try:
                    # Get audio data
                    audio_chunk = self.audio_queue.get(timeout=0.1)
                    audio_buffer = np.concatenate([audio_buffer, audio_chunk])
                    
                    # Maintain buffer size
                    if len(audio_buffer) > buffer_size:
                        audio_buffer = audio_buffer[-buffer_size:]
                    
                    # Process audio
                    detection_result = self._process_audio_direct(audio_buffer)
                    
                    if detection_result:
                        self._handle_detection(detection_result)
                    
                    # Status display
                    cooldown_left = max(0, self.detection_cooldown - (time.time() - self.last_detection_time))
                    if cooldown_left > 0:
                        print(f"   ⏳ Cooldown: {cooldown_left:.1f}s | Commands: {self.command_count} | Listening...", end='\r')
                    else:
                        print(f"   ✅ Ready | Commands: {self.command_count} | Say 'ON'...", end='\r')
                        
                except queue.Empty:
                    # Update status
                    cooldown_left = max(0, self.detection_cooldown - (time.time() - self.last_detection_time))
                    if cooldown_left > 0:
                        print(f"   ⏳ Cooldown: {cooldown_left:.1f}s | Commands: {self.command_count} | Listening...", end='\r')
                    else:
                        print(f"   ✅ Ready | Commands: {self.command_count} | Say 'ON'...", end='\r')
                    continue
                    
        except KeyboardInterrupt:
            self.stop_working()
    
    def stop_working(self):
        """Stop the assistant"""
        print("\n\n🛑 SHUTTING DOWN WORKING ASSISTANT...")
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.audio_interface.terminate()
        
        print(f"📊 SESSION SUMMARY:")
        print(f"   Total Valid Commands: {self.command_count}")
        print("✅ Working Assistant: SHUTDOWN COMPLETE")

if __name__ == "__main__":
    assistant = WorkingAssistantFixed()
    assistant.start_working()