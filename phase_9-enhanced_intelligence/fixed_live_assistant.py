# fixed_live_assistant.py
import tensorflow as tf
import numpy as np
import time
import threading
from typing import Dict, Any
import pyaudio
import queue
import wave
import os

# Import your Phase 9.0 components
from hybrid_model_router_optimized import Phase9EnhancedIntelligence
from phase9_working import Phase9ShadowNet

class FixedLiveVoiceAssistant:
    """
    FIXED LIVE VOICE ASSISTANT: Proper microphone integration + real-time processing
    """
    
    def __init__(self):
        print("🚀 INITIALIZING FIXED LIVE VOICE ASSISTANT...")
        
        # Phase 9.0 Components
        self.hybrid_intelligence = Phase9EnhancedIntelligence()
        self.shadow_net = Phase9ShadowNet()
        
        # FIXED: Proper audio configuration for real microphones
        self.sample_rate = 16000
        self.chunk_size = 1024  # Smaller chunks for real-time
        self.channels = 1
        self.audio_format = pyaudio.paInt16  # Most microphones use Int16
        self.audio_queue = queue.Queue()
        
        # Audio buffer configuration
        self.audio_buffer = np.array([], dtype=np.float32)
        self.buffer_duration = 2.0  # 2-second buffer for better processing
        self.buffer_size = int(self.sample_rate * self.buffer_duration)
        
        # Assistant state
        self.is_listening = False
        self.current_emotion = 'neutral'
        self.command_history = []
        self.audio_interface = None
        self.audio_stream = None
        
        # Debug and recording
        self.debug_mode = True
        self.recording_counter = 0
        
        # Start Phase 9.0 systems
        self._start_phase9_systems()
        
        print("🎯 FIXED LIVE VOICE ASSISTANT READY!")
        print("   🧠 Hybrid Intelligence: ACTIVE")
        print("   🎤 Real Microphone: CONFIGURED")
        print("   🔊 Audio Format: 16-bit PCM")
        print("   📏 Sample Rate: 16kHz")
    
    def _start_phase9_systems(self):
        """Start all Phase 9.0 systems"""
        print("   🔗 Starting Phase 9.0 integration...")
        
        # Start Shadow-Net Event Bus
        self.shadow_net.start_shadow_net()
        print("   ✅ Phase 9.0 systems: OPERATIONAL")
    
    def _setup_audio_stream(self):
        """FIXED: Proper microphone setup with error handling"""
        try:
            self.audio_interface = pyaudio.PyAudio()
            
            # Test available devices
            print("   🔍 Checking audio devices...")
            for i in range(self.audio_interface.get_device_count()):
                device_info = self.audio_interface.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    print(f"     🎤 Device {i}: {device_info['name']}")
            
            # FIXED: Proper stream configuration for real microphones
            self.audio_stream = self.audio_interface.open(
                format=self.audio_format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self._audio_callback,
                input_device_index=None  # Use default device
            )
            
            print("   ✅ Microphone stream: CONFIGURED")
            return True
            
        except Exception as e:
            print(f"   ❌ Microphone setup failed: {e}")
            print("   💡 Try: pip install pyaudio")
            print("   💡 On Windows, you might need: pip install pipwin && pipwin install pyaudio")
            return False
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """FIXED: Proper audio callback with conversion to float32"""
        try:
            # Convert Int16 to Float32 (-1.0 to 1.0 range)
            audio_chunk = np.frombuffer(in_data, dtype=np.int16).astype(np.float32) / 32768.0
            self.audio_queue.put(audio_chunk)
        except Exception as e:
            print(f"   ❌ Audio callback error: {e}")
        
        return (in_data, pyaudio.paContinue)
    
    def _save_debug_audio(self, audio_data: np.ndarray, prefix: str = "debug"):
        """Save audio for debugging"""
        if not self.debug_mode:
            return
            
        filename = f"{prefix}_{self.recording_counter:04d}.wav"
        self.recording_counter += 1
        
        # Convert back to int16 for WAV file
        audio_int16 = (audio_data * 32768.0).astype(np.int16)
        
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_int16.tobytes())
        
        print(f"   💾 Debug audio saved: {filename}")

    def _audio_processing_loop(self):
        """FIXED: Robust audio processing loop"""
        print("   🔄 Starting audio processing loop...")
        
        if not self._setup_audio_stream():
            print("   ❌ Cannot start without microphone")
            return
        
        self.audio_stream.start_stream()
        print("   🎤 Microphone stream: ACTIVE")
        
        consecutive_failures = 0
        max_failures = 5
        
        try:
            while self.is_listening and consecutive_failures < max_failures:
                try:
                    # Get audio chunk with timeout
                    audio_chunk = self.audio_queue.get(timeout=1.0)
                    
                    # Reset failure counter on success
                    consecutive_failures = 0
                    
                    # Add to buffer
                    self.audio_buffer = np.concatenate([self.audio_buffer, audio_chunk])
                    
                    # Keep buffer at desired size
                    if len(self.audio_buffer) > self.buffer_size:
                        self.audio_buffer = self.audio_buffer[-self.buffer_size:]
                    
                    # Process when we have enough audio
                    if len(self.audio_buffer) >= int(self.sample_rate * 1.0):  # At least 1 second
                        self._process_audio_buffer(self.audio_buffer.copy())
                        
                except queue.Empty:
                    # No audio data, just continue
                    continue
                except Exception as e:
                    print(f"   ❌ Audio processing error: {e}")
                    consecutive_failures += 1
                    time.sleep(0.1)
                    
        except Exception as e:
            print(f"   ❌ Audio loop crashed: {e}")
        finally:
            self._cleanup_audio()
    
    def _process_audio_buffer(self, audio_buffer: np.ndarray):
        """FIXED: Process audio with proper error handling"""
        try:
            # Save debug audio occasionally
            if self.debug_mode and np.random.random() < 0.01:  # 1% chance
                self._save_debug_audio(audio_buffer, "live_input")
            
            # Use hybrid intelligence
            result = self.hybrid_intelligence.process_audio_intelligently(audio_buffer)
            
            # Update current emotion
            self.current_emotion = result['emotion']['emotion']
            
            # Check if wakeword detected
            if result['hybrid_prediction']['wakeword_detected']:
                self._handle_wakeword_detection(result)
            else:
                # Just update emotion context
                self._update_emotion_context(result)
                
        except Exception as e:
            print(f"   ❌ Audio processing failed: {e}")
    
    def _handle_wakeword_detection(self, result: Dict):
        """Handle wakeword detection with emotional context"""
        emotion = result['emotion']['emotion']
        confidence = result['hybrid_prediction']['final_confidence']
        
        print(f"🎯 WAKE-WORD DETECTED!")
        print(f"   🎭 Emotion: {emotion} ({confidence:.1%} confidence)")
        print(f"   ⚡ Performance: {result['performance']['total_time_ms']:.1f}ms")
        
        # Route through Shadow-Net Event Bus
        try:
            event_result = self.hybrid_intelligence._route_to_event_bus(result)
            print(f"   🌐 Event Bus: {event_result}")
        except Exception as e:
            print(f"   ⚠️ Event Bus failed: {e}")
        
        # Emotional response routing
        self._emotional_response_routing(emotion, result)
        
        # Add to command history
        self.command_history.append({
            'timestamp': time.time(),
            'emotion': emotion,
            'confidence': confidence,
            'routing': result['routing_decision']
        })
    
    def _emotional_response_routing(self, emotion: str, result: Dict):
        """Route responses based on emotional context"""
        emotional_routing = result['routing_decision']['emotional_routing']
        
        print(f"   🧠 Emotional Routing: {emotional_routing}")
        
        # Different responses based on emotion
        emotion_responses = {
            'happy': "I detect you're happy! How can I help? 😊",
            'sad': "I sense you might be feeling down. I'm here to help. 💙",
            'angry': "I notice some frustration. Let me help calmly. 🧘",
            'excited': "You sound excited! What's the plan? 🚀",
            'neutral': "How can I assist you today?",
            'tired': "You sound tired. Let me help efficiently. 😴",
            'surprised': "Wow! You sound surprised! What happened? 😲",
            'fear': "I sense some concern. I'm here to help safely. 🛡️"
        }
        
        response = emotion_responses.get(emotion, "How can I help you?")
        print(f"   💬 Response: {response}")
        
        # Cross-device emotional sync
        self._sync_emotional_state(emotion, result)
    
    def _sync_emotional_state(self, emotion: str, result: Dict):
        """Sync emotional state across devices via Event Bus"""
        try:
            # Send emotional state to other devices
            sync_result = self.shadow_net.event_bus.send_to_device('phone', 'state_sync', {
                'emotional_state': emotion,
                'confidence': result['emotion']['confidence'],
                'context': result['routing_decision']['context_awareness'],
                'timestamp': time.time()
            })
            print(f"   🔄 Emotional Sync: {sync_result}")
        except Exception as e:
            print(f"   ⚠️ Emotional sync failed: {e}")
    
    def _update_emotion_context(self, result: Dict):
        """Update emotion context without wakeword"""
        emotion = result['emotion']['emotion']
        confidence = result['emotion']['confidence']
        
        # Only log significant emotion changes
        if confidence > 0.7 and emotion != self.current_emotion:
            print(f"   🎭 Emotion Context: {emotion} ({confidence:.1%})")
    
    def _cleanup_audio(self):
        """Properly cleanup audio resources"""
        try:
            if self.audio_stream:
                self.audio_stream.stop_stream()
                self.audio_stream.close()
            if self.audio_interface:
                self.audio_interface.terminate()
            print("   🔇 Audio resources cleaned up")
        except Exception as e:
            print(f"   ⚠️ Audio cleanup warning: {e}")
    
    def start_listening(self):
        """Start the fixed live voice assistant"""
        print("\n🎧 STARTING FIXED LIVE VOICE ASSISTANT...")
        print("   🔊 Listening for voice commands...")
        print("   🧠 Emotional intelligence: ACTIVE")
        print("   🎤 Real microphone: ENABLED")
        print("   💡 Say your wakeword to begin!")
        print("   🛑 Press Ctrl+C to stop")
        
        self.is_listening = True
        
        # Start audio processing in separate thread
        self.audio_thread = threading.Thread(target=self._audio_processing_loop, daemon=True)
        self.audio_thread.start()
        
        try:
            # Keep the assistant running
            while self.is_listening:
                time.sleep(0.1)
                
                # Display status every 30 seconds
                if int(time.time()) % 30 == 0:
                    print(f"   📊 Status: Listening | Emotion: {self.current_emotion} | Commands: {len(self.command_history)}")
                    
        except KeyboardInterrupt:
            self.stop_listening()
    
    def stop_listening(self):
        """Stop the voice assistant"""
        print("\n🛑 STOPPING FIXED LIVE VOICE ASSISTANT...")
        self.is_listening = False
        
        # Wait for audio thread to finish
        if hasattr(self, 'audio_thread'):
            self.audio_thread.join(timeout=2.0)
        
        # Cleanup audio resources
        self._cleanup_audio()
        
        # Print summary
        print(f"📈 SESSION SUMMARY:")
        print(f"   Total Commands: {len(self.command_history)}")
        if self.command_history:
            emotions = [cmd['emotion'] for cmd in self.command_history]
            from collections import Counter
            emotion_counts = Counter(emotions)
            print(f"   Emotion Distribution: {dict(emotion_counts)}")
        
        print("✅ Fixed Live Voice Assistant: SHUTDOWN COMPLETE")

# TEST FUNCTION FOR MICROPHONE
def test_microphone_only():
    """Test just the microphone without AI processing"""
    print("🎤 TESTING MICROPHONE ONLY...")
    
    try:
        p = pyaudio.PyAudio()
        
        # List audio devices
        print("Available audio devices:")
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                print(f"  {i}: {info['name']}")
        
        # Test recording
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )
        
        print("Recording 3 seconds of audio...")
        frames = []
        for i in range(0, int(16000 / 1024 * 3)):
            data = stream.read(1024)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Save test recording
        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
        with wave.open("microphone_test.wav", 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(audio_data.tobytes())
        
        print("✅ Microphone test successful! Saved as 'microphone_test.wav'")
        print("💡 Play the file to verify your microphone is working")
        
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")
        print("💡 Try installing pyaudio properly:")
        print("   pip install pyaudio")
        print("   On Windows: pip install pipwin && pipwin install pyaudio")

# MAIN EXECUTION
if __name__ == "__main__":
    print("=" * 60)
    print("🎯 FIXED LIVE VOICE ASSISTANT - MICROPHONE EDITION")
    print("=" * 60)
    
    # Choose mode
    print("\nSelect mode:")
    print("1. Test Microphone Only")
    print("2. Fixed Live Assistant")
    print("3. Simulated Demo")
    
    try:
        choice = input("Enter choice (1, 2, or 3): ").strip()
        
        if choice == "1":
            test_microphone_only()
        elif choice == "2":
            assistant = FixedLiveVoiceAssistant()
            assistant.start_listening()
        elif choice == "3":
            # Run the simulated version that worked
            from ultimate_assistant_integration import demonstrate_ultimate_assistant
            demonstrate_ultimate_assistant()
        else:
            print("❌ Invalid choice. Running microphone test...")
            test_microphone_only()
            
    except KeyboardInterrupt:
        print("\n🛑 User interrupted. Shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Troubleshooting tips:")
        print("   1. Run 'pip install pyaudio'")
        print("   2. On Windows, try: 'pip install pipwin && pipwin install pyaudio'")
        print("   3. Check your microphone permissions")
        print("   4. Test with option 1 first")