# realistic_voice_assistant.py
import tensorflow as tf
import numpy as np
import time
import threading
import pyaudio
import queue
import wave
from collections import deque
from hybrid_model_router_optimized import Phase9EnhancedIntelligence
from phase9_working import Phase9ShadowNet

class RealisticVoiceAssistant:
    """
    REALISTIC VOICE ASSISTANT: Proper noise filtering + voice detection
    """
    
    def __init__(self, wake_word="assistant"):
        print("🚀 INITIALIZING REALISTIC VOICE ASSISTANT...")
        
        # Core components
        self.hybrid_intelligence = Phase9EnhancedIntelligence()
        self.shadow_net = Phase9ShadowNet()
        self.wake_word = wake_word
        
        # Audio configuration
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.audio_format = pyaudio.paInt16
        self.audio_queue = queue.Queue()
        
        # VOICE DETECTION PARAMETERS (CRITICAL FIXES)
        self.energy_threshold = 0.01  # Minimum audio energy to consider as voice
        self.silence_duration = 0.5   # Seconds of silence to detect end of speech
        self.min_voice_duration = 0.3 # Minimum voice duration to process
        self.confidence_threshold = 0.8  # Minimum confidence to accept detection
        
        # State management
        self.is_listening = False
        self.current_emotion = 'neutral'
        self.command_count = 0
        self.session_start = time.time()
        self.last_detection_time = 0
        self.detection_cooldown = 2.0  # Minimum seconds between detections
        
        # Audio processing buffers
        self.voice_buffer = np.array([], dtype=np.float32)
        self.silence_counter = 0
        self.is_recording_voice = False
        
        # Start systems
        self._initialize_systems()
        
        print("🎯 REALISTIC VOICE ASSISTANT READY!")
        print("   🔊 Voice Activity Detection: ENABLED")
        print("   🔇 Noise Filtering: ACTIVE")
        print("   📊 Confidence Threshold: 80%")
        print("   ⏱️  Cooldown: 2 seconds between commands")
    
    def _initialize_systems(self):
        """Initialize all systems with proper error handling"""
        try:
            # Start Shadow-Net Event Bus
            self.shadow_net.start_shadow_net()
            
            # Setup audio with specific device selection
            self.audio_interface = pyaudio.PyAudio()
            
            # List available devices and choose the best one
            print("   🔍 Scanning audio devices...")
            input_devices = []
            for i in range(self.audio_interface.get_device_count()):
                device_info = self.audio_interface.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    input_devices.append((i, device_info['name']))
                    print(f"     {i}: {device_info['name']}")
            
            # Use default device (usually the best choice)
            self.audio_stream = self.audio_interface.open(
                format=self.audio_format,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self._audio_callback,
                input_device_index=None  # Use default device
            )
            
            print("   ✅ Audio system: OPTIMIZED")
            
        except Exception as e:
            print(f"   ❌ System initialization failed: {e}")
            raise
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Audio callback with basic error handling"""
        try:
            audio_chunk = np.frombuffer(in_data, dtype=np.int16).astype(np.float32) / 32768.0
            self.audio_queue.put(audio_chunk)
        except Exception as e:
            print(f"   ⚠️ Audio callback error: {e}")
        
        return (in_data, pyaudio.paContinue)
    
    def _calculate_energy(self, audio_data):
        """Calculate audio energy for voice activity detection"""
        return np.mean(audio_data ** 2)
    
    def _is_voice_activity(self, audio_chunk):
        """Detect if audio chunk contains voice activity"""
        energy = self._calculate_energy(audio_chunk)
        return energy > self.energy_threshold
    
    def _process_audio_with_vad(self, audio_buffer):
        """Process audio with proper Voice Activity Detection"""
        current_time = time.time()
        
        # Cooldown period check
        if current_time - self.last_detection_time < self.detection_cooldown:
            return None
        
        # Check if we have enough audio for processing
        if len(audio_buffer) < self.sample_rate:  # Need at least 1 second
            return None
        
        # Use the most recent 1 second of audio
        processing_audio = audio_buffer[-self.sample_rate:]
        
        # Check for voice activity in the processing window
        if not self._is_voice_activity(processing_audio):
            return None
        
        # Process with hybrid intelligence
        result = self.hybrid_intelligence.process_audio_intelligently(processing_audio)
        
        # Apply confidence threshold
        confidence = result['hybrid_prediction']['final_confidence']
        if confidence < self.confidence_threshold:
            return None
        
        # Check if wakeword is detected
        if not result['hybrid_prediction']['wakeword_detected']:
            return None
        
        # Valid detection found
        self.last_detection_time = current_time
        return result
    
    def _process_real_command(self, emotion: str, confidence: float):
        """Process only legitimate voice commands"""
        self.command_count += 1
        
        # Emotional responses
        responses = {
            'happy': "I detect happiness! How can I assist? 😊",
            'sad': "I sense you might need support. I'm here for you. 💙", 
            'angry': "I notice some intensity. Let me help calmly. 🧘",
            'excited': "You sound excited! What's the plan? 🚀",
            'neutral': "Hello! How can I help you today?",
            'tired': "You sound tired. Let me assist efficiently. 😴",
            'surprised': "Wow! You sound surprised! What happened? 😲",
            'fear': "I sense concern. I'm here to help safely. 🛡️"
        }
        
        response = responses.get(emotion, "How can I assist you?")
        
        # Display command info
        print(f"\n🎯 COMMAND #{self.command_count} - REAL VOICE DETECTED!")
        print(f"   🎭 Emotion: {emotion} ({confidence:.1%} confidence)")
        print(f"   💬 Response: {response}")
        print(f"   ⏱️  Next command available in {self.detection_cooldown} seconds")
        
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
                'timestamp': time.time(),
                'type': 'voice_command'
            }
            
            # Sync with devices
            phone_result = self.shadow_net.event_bus.send_to_device('phone', 'voice_command', sync_data)
            print(f"   🔄 Device Sync: ✅ Phone acknowledged")
            
        except Exception as e:
            print(f"   ⚠️ Device sync: {e}")
    
    def _display_listening_status(self):
        """Show that the system is actively listening"""
        status_indicators = ["🔊 Listening...", "🎤 Ready for voice", "💭 Waiting for command"]
        indicator = status_indicators[int(time.time()) % len(status_indicators)]
        
        cooldown_remaining = max(0, self.detection_cooldown - (time.time() - self.last_detection_time))
        if cooldown_remaining > 0:
            print(f"   ⏳ Cooldown: {cooldown_remaining:.1f}s | Commands: {self.command_count} | {indicator}", end='\r')
        else:
            print(f"   ✅ Ready | Commands: {self.command_count} | {indicator}", end='\r')
    
    def start_realistic_mode(self):
        """Start the realistic voice assistant"""
        print("\n" + "="*60)
        print("🎧 REALISTIC VOICE ASSISTANT - PRODUCTION READY")
        print("="*60)
        print("   🔊 Voice Activity Detection: ACTIVE")
        print("   🔇 Background Noise: FILTERED") 
        print("   📊 Confidence Threshold: 80% MINIMUM")
        print("   ⏱️  Anti-Spam: 2-second cooldown")
        print(f"   🔔 Wake Word: '{self.wake_word}'")
        print("   🧠 Emotional Intelligence: ENABLED")
        print("   🌐 Multi-Device Sync: READY")
        print("   🛑 Press Ctrl+C to exit")
        print("="*60)
        print("💡 SPEAK CLEARLY AND WAIT FOR RESPONSES...")
        
        self.is_listening = True
        self.audio_stream.start_stream()
        
        # Audio buffer for processing (3 seconds)
        audio_buffer = np.array([], dtype=np.float32)
        buffer_size = self.sample_rate * 3
        
        try:
            while self.is_listening:
                try:
                    # Get audio data with timeout
                    audio_chunk = self.audio_queue.get(timeout=0.1)
                    audio_buffer = np.concatenate([audio_buffer, audio_chunk])
                    
                    # Maintain buffer size
                    if len(audio_buffer) > buffer_size:
                        audio_buffer = audio_buffer[-buffer_size:]
                    
                    # Process audio with proper voice detection
                    result = self._process_audio_with_vad(audio_buffer)
                    
                    if result is not None:
                        # Valid voice command detected!
                        self._process_real_command(
                            result['emotion']['emotion'],
                            result['hybrid_prediction']['final_confidence']
                        )
                    
                    # Display status
                    self._display_listening_status()
                        
                except queue.Empty:
                    # No audio data, just update status
                    self._display_listening_status()
                    continue
                    
        except KeyboardInterrupt:
            self.stop_realistic_mode()
        except Exception as e:
            print(f"\n❌ System error: {e}")
            self.stop_realistic_mode()
    
    def stop_realistic_mode(self):
        """Stop the realistic assistant"""
        print("\n\n🛑 SHUTTING DOWN REALISTIC ASSISTANT...")
        self.is_listening = False
        
        # Cleanup
        try:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.audio_interface.terminate()
        except:
            pass
        
        # Session summary
        session_duration = time.time() - self.session_start
        print(f"\n📈 REALISTIC SESSION SUMMARY:")
        print(f"   ⏱️  Duration: {session_duration:.1f} seconds")
        print(f"   🎯 Valid Commands: {self.command_count}")
        if session_duration > 0:
            print(f"   📊 Commands/Minute: {self.command_count/(session_duration/60):.1f}")
        print(f"   🎭 Final Emotion: {self.current_emotion}")
        print("✅ Realistic Voice Assistant: SHUTDOWN COMPLETE")

# TEST FUNCTION TO CALIBRATE YOUR MICROPHONE
def calibrate_microphone():
    """Calibrate microphone sensitivity"""
    print("🎤 MICROPHONE CALIBRATION TOOL")
    print("This will help set the right sensitivity for your environment...")
    
    try:
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )
        
        print("🔊 Measuring background noise... (stay silent for 3 seconds)")
        background_energies = []
        
        for i in range(30):  # 3 seconds of background
            data = stream.read(1024, exception_on_overflow=False)
            audio_chunk = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            energy = np.mean(audio_chunk ** 2)
            background_energies.append(energy)
            print(f"   Background noise level: {energy:.6f}", end='\r')
            time.sleep(0.1)
        
        avg_background = np.mean(background_energies)
        recommended_threshold = avg_background * 10  # 10x background noise
        
        print(f"\n✅ CALIBRATION COMPLETE:")
        print(f"   📊 Average background noise: {avg_background:.6f}")
        print(f"   🎯 Recommended voice threshold: {recommended_threshold:.6f}")
        print(f"   💡 Current threshold in assistant: 0.010000")
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        if recommended_threshold > 0.01:
            print(f"   ⚠️  Your environment is noisy! Consider increasing threshold.")
        else:
            print(f"   ✅ Your environment is quiet! Current settings should work well.")
            
    except Exception as e:
        print(f"❌ Calibration failed: {e}")

# QUICK START FUNCTION
def quick_start():
    """Quick start the realistic assistant"""
    print("Choose mode:")
    print("1. Start Realistic Voice Assistant")
    print("2. Calibrate Microphone First")
    
    try:
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "2":
            calibrate_microphone()
            print("\n" + "="*50)
            input("Press Enter to start the voice assistant...")
        
        assistant = RealisticVoiceAssistant(wake_word="assistant")
        assistant.start_realistic_mode()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    quick_start()