# production_voice_assistant.py
import tensorflow as tf
import numpy as np
import time
import threading
import pyaudio
import queue
import wave
from hybrid_model_router_optimized import Phase9EnhancedIntelligence
from phase9_working import Phase9ShadowNet

class ProductionVoiceAssistant:
    """
    PRODUCTION-READY VOICE ASSISTANT: Optimized for daily use
    """
    
    def __init__(self, wake_word="assistant"):
        print("🚀 INITIALIZING PRODUCTION VOICE ASSISTANT...")
        
        # Core components
        self.hybrid_intelligence = Phase9EnhancedIntelligence()
        self.shadow_net = Phase9ShadowNet()
        self.wake_word = wake_word
        
        # Audio configuration (optimized for production)
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.audio_format = pyaudio.paInt16
        self.audio_queue = queue.Queue()
        
        # Production settings
        self.is_listening = False
        self.current_emotion = 'neutral'
        self.command_count = 0
        self.session_start = time.time()
        
        # Start systems
        self._initialize_systems()
        
        print("🎯 PRODUCTION VOICE ASSISTANT READY!")
        print(f"   🔔 Wake Word: '{self.wake_word}'")
        print("   🎤 Microphone: OPTIMIZED")
        print("   🧠 Emotional AI: ACTIVE")
        print("   🌐 Multi-Device: READY")
    
    def _initialize_systems(self):
        """Initialize all production systems"""
        # Start Shadow-Net Event Bus
        self.shadow_net.start_shadow_net()
        
        # Setup audio
        self.audio_interface = pyaudio.PyAudio()
        self.audio_stream = self.audio_interface.open(
            format=self.audio_format,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self._audio_callback
        )
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Production audio callback"""
        audio_chunk = np.frombuffer(in_data, dtype=np.int16).astype(np.float32) / 32768.0
        self.audio_queue.put(audio_chunk)
        return (in_data, pyaudio.paContinue)
    
    def _process_voice_command(self, emotion: str, confidence: float):
        """Process voice commands with emotional intelligence"""
        self.command_count += 1
        
        # Emotional responses
        responses = {
            'happy': "I detect happiness! How can I assist? 😊",
            'sad': "I sense you might need support. I'm here for you. 💙", 
            'angry': "I notice some intensity. Let me help calmly. 🧘",
            'excited': "You sound excited! What's the plan? 🚀",
            'neutral': "How can I help you today?",
            'tired': "You sound tired. Let me assist efficiently. 😴",
            'surprised': "Wow! You sound surprised! What happened? 😲",
            'fear': "I sense concern. I'm here to help safely. 🛡️"
        }
        
        response = responses.get(emotion, "How can I assist you?")
        
        # Display command info
        print(f"\n🎯 COMMAND #{self.command_count}")
        print(f"   🎭 Emotion: {emotion} ({confidence:.1%})")
        print(f"   💬 Response: {response}")
        
        # Cross-device sync
        self._sync_with_devices(emotion, confidence)
        
        return response
    
    def _sync_with_devices(self, emotion: str, confidence: float):
        """Sync emotional state across devices"""
        try:
            sync_data = {
                'emotional_state': emotion,
                'confidence': confidence,
                'command_count': self.command_count,
                'timestamp': time.time()
            }
            
            # Sync with phone
            phone_result = self.shadow_net.event_bus.send_to_device('phone', 'emotional_sync', sync_data)
            
            # Sync with other devices
            other_result = self.shadow_net.event_bus.send_to_device('tablet', 'emotional_sync', sync_data)
            
            print(f"   🔄 Multi-Device Sync: ✅ Phone: {phone_result}, Tablet: {other_result}")
            
        except Exception as e:
            print(f"   ⚠️ Device sync: {e}")
    
    def start_production_mode(self):
        """Start the production voice assistant"""
        print("\n" + "="*50)
        print("🎧 PRODUCTION VOICE ASSISTANT - LIVE")
        print("="*50)
        print("   🔊 Listening for voice commands...")
        print(f"   🔔 Say '{self.wake_word}' to activate")
        print("   🧠 Emotional intelligence: ACTIVE")
        print("   🌐 Multi-device sync: ENABLED")
        print("   🛑 Press Ctrl+C to exit")
        print("="*50)
        
        self.is_listening = True
        self.audio_stream.start_stream()
        
        # Audio buffer
        audio_buffer = np.array([], dtype=np.float32)
        buffer_size = self.sample_rate * 2  # 2-second buffer
        
        try:
            while self.is_listening:
                try:
                    # Get audio data
                    audio_chunk = self.audio_queue.get(timeout=1.0)
                    audio_buffer = np.concatenate([audio_buffer, audio_chunk])
                    
                    # Maintain buffer size
                    if len(audio_buffer) > buffer_size:
                        audio_buffer = audio_buffer[-buffer_size:]
                    
                    # Process when we have enough audio
                    if len(audio_buffer) >= self.sample_rate:  # At least 1 second
                        result = self.hybrid_intelligence.process_audio_intelligently(audio_buffer)
                        
                        # Update emotion context
                        self.current_emotion = result['emotion']['emotion']
                        
                        # Handle wake word detection
                        if result['hybrid_prediction']['wakeword_detected']:
                            self._process_voice_command(
                                result['emotion']['emotion'],
                                result['hybrid_prediction']['final_confidence']
                            )
                    
                    # Status update every 30 seconds
                    if int(time.time()) % 30 == 0:
                        uptime = time.time() - self.session_start
                        print(f"   📊 Status: {int(uptime)}s | Commands: {self.command_count} | Emotion: {self.current_emotion}")
                        
                except queue.Empty:
                    continue
                    
        except KeyboardInterrupt:
            self.stop_production_mode()
    
    def stop_production_mode(self):
        """Stop the production assistant"""
        print("\n🛑 SHUTTING DOWN PRODUCTION ASSISTANT...")
        self.is_listening = False
        
        # Cleanup
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.audio_interface.terminate()
        
        # Session summary
        session_duration = time.time() - self.session_start
        print(f"\n📈 PRODUCTION SESSION SUMMARY:")
        print(f"   ⏱️  Duration: {session_duration:.1f} seconds")
        print(f"   🎯 Commands Processed: {self.command_count}")
        print(f"   📊 Commands/Minute: {self.command_count/(session_duration/60):.1f}")
        print(f"   🎭 Final Emotion: {self.current_emotion}")
        print("✅ Production Voice Assistant: SHUTDOWN COMPLETE")

# QUICK START FUNCTION
def quick_start():
    """Quick start the production assistant"""
    assistant = ProductionVoiceAssistant(wake_word="assistant")
    assistant.start_production_mode()

if __name__ == "__main__":
    quick_start()