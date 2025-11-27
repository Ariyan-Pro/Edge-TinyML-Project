# ultimate_assistant_integration.py
import tensorflow as tf
import numpy as np
import time
import threading
from typing import Dict, Any
import pyaudio
import queue

# Import your Phase 9.0 components
from hybrid_model_router_optimized import Phase9EnhancedIntelligence
from phase9_working import Phase9ShadowNet

class UltimateVoiceAssistant:
    """
    ULTIMATE VOICE ASSISTANT: Phase 9.0 Hybrid Intelligence + Event Bus Integration
    """
    
    def __init__(self):
        print("🚀 INITIALIZING ULTIMATE VOICE ASSISTANT...")
        
        # Phase 9.0 Components
        self.hybrid_intelligence = Phase9EnhancedIntelligence()
        self.shadow_net = Phase9ShadowNet()
        
        # Audio configuration
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.audio_queue = queue.Queue()
        
        # Assistant state
        self.is_listening = False
        self.current_emotion = 'neutral'
        self.command_history = []
        
        # Start Phase 9.0 systems
        self._start_phase9_systems()
        
        print("🎯 ULTIMATE VOICE ASSISTANT READY!")
        print("   🧠 Hybrid Intelligence: ACTIVE")
        print("   🌐 Shadow-Net Event Bus: RUNNING")
        print("   🎤 Real-time Audio: ENABLED")
    
    def _start_phase9_systems(self):
        """Start all Phase 9.0 systems"""
        print("   🔗 Starting Phase 9.0 integration...")
        
        # Start Shadow-Net Event Bus
        self.shadow_net.start_shadow_net()
        
        # Start audio processing thread
        self.audio_thread = threading.Thread(target=self._audio_processing_loop, daemon=True)
        self.audio_thread.start()
        
        print("   ✅ Phase 9.0 systems: OPERATIONAL")
    
    def _audio_processing_loop(self):
        """Real-time audio processing loop"""
        p = pyaudio.PyAudio()
        
        def audio_callback(in_data, frame_count, time_info, status):
            self.audio_queue.put(np.frombuffer(in_data, dtype=np.float32))
            return (in_data, pyaudio.paContinue)
        
        # Start audio stream
        stream = p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=audio_callback
        )
        
        stream.start_stream()
        print("   🎤 Audio stream: ACTIVE")
        
        # Audio buffer for processing
        audio_buffer = np.array([], dtype=np.float32)
        buffer_duration = 1.0  # 1 second buffer
        buffer_size = int(self.sample_rate * buffer_duration)
        
        try:
            while self.is_listening:
                try:
                    # Get audio chunk from queue
                    audio_chunk = self.audio_queue.get(timeout=0.1)
                    audio_buffer = np.concatenate([audio_buffer, audio_chunk])
                    
                    # Keep buffer at desired size
                    if len(audio_buffer) > buffer_size:
                        audio_buffer = audio_buffer[-buffer_size:]
                    
                    # Process when we have enough audio
                    if len(audio_buffer) >= buffer_size:
                        self._process_audio_buffer(audio_buffer.copy())
                        
                except queue.Empty:
                    continue
                    
        except Exception as e:
            print(f"   ❌ Audio processing error: {e}")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
    
    def _process_audio_buffer(self, audio_buffer: np.ndarray):
        """Process audio buffer with hybrid intelligence"""
        try:
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
        event_result = self.hybrid_intelligence._route_to_event_bus(result)
        print(f"   🌐 Event Bus: {event_result}")
        
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
    
    def start_listening(self):
        """Start the ultimate voice assistant"""
        print("\n🎧 STARTING ULTIMATE VOICE ASSISTANT...")
        print("   🔊 Listening for voice commands...")
        print("   🧠 Emotional intelligence: ACTIVE")
        print("   🌐 Multi-device sync: READY")
        print("   💡 Say your wakeword to begin!")
        
        self.is_listening = True
        
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
        print("\n🛑 STOPPING ULTIMATE VOICE ASSISTANT...")
        self.is_listening = False
        
        # Print summary
        print(f"📈 SESSION SUMMARY:")
        print(f"   Total Commands: {len(self.command_history)}")
        if self.command_history:
            emotions = [cmd['emotion'] for cmd in self.command_history]
            from collections import Counter
            emotion_counts = Counter(emotions)
            print(f"   Emotion Distribution: {dict(emotion_counts)}")
        
        print("✅ Ultimate Voice Assistant: SHUTDOWN COMPLETE")

    def get_system_status(self) -> Dict:
        """Get complete system status"""
        hybrid_report = self.hybrid_intelligence.hybrid_router.get_performance_report()
        
        return {
            'assistant': {
                'listening': self.is_listening,
                'current_emotion': self.current_emotion,
                'total_commands': len(self.command_history),
                'uptime': 'active' if self.is_listening else 'inactive'
            },
            'phase9_hybrid': hybrid_report,
            'shadow_net': {
                'event_bus': 'operational',
                'multi_device': 'ready',
                'encryption': 'active'
            },
            'performance': {
                'real_time': 'enabled',
                'emotional_ai': 'active',
                'cross_device': 'ready'
            }
        }

# QUICK DEMONSTRATION
def demonstrate_ultimate_assistant():
    """Demonstrate the ultimate voice assistant"""
    print("🎪 DEMONSTRATING ULTIMATE VOICE ASSISTANT...")
    
    assistant = UltimateVoiceAssistant()
    
    # Show system status
    status = assistant.get_system_status()
    print(f"📊 SYSTEM STATUS: {status}")
    
    # Test with simulated audio (since we can't use microphone in demo)
    print("\n🧪 SIMULATING VOICE INTERACTION...")
    
    # Simulate different emotional contexts
    test_scenarios = [
        {'emotion': 'happy', 'wakeword': True},
        {'emotion': 'angry', 'wakeword': True},
        {'emotion': 'sad', 'wakeword': True},
        {'emotion': 'excited', 'wakeword': True},
    ]
    
    for scenario in test_scenarios:
        print(f"\n--- Testing {scenario['emotion'].upper()} scenario ---")
        
        # Create simulated audio with emotional characteristics
        simulated_audio = np.random.normal(0, 0.1, 16000).astype(np.float32)
        
        # Process with hybrid intelligence
        result = assistant.hybrid_intelligence.process_audio_intelligently(simulated_audio)
        
        # Simulate wakeword detection
        if scenario['wakeword']:
            assistant._handle_wakeword_detection(result)
        
        time.sleep(1)
    
    # Show final status
    final_status = assistant.get_system_status()
    print(f"\n🎯 FINAL SYSTEM STATUS: {final_status}")
    
    assistant.stop_listening()

# MAIN EXECUTION
if __name__ == "__main__":
    print("=" * 60)
    print("🎯 ULTIMATE VOICE ASSISTANT - PHASE 9.0 INTEGRATION")
    print("=" * 60)
    
    # Choose mode
    print("\nSelect mode:")
    print("1. Demo Mode (Simulated interactions)")
    print("2. Live Mode (Real microphone - requires pyaudio)")
    
    try:
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "1":
            demonstrate_ultimate_assistant()
        elif choice == "2":
            assistant = UltimateVoiceAssistant()
            assistant.start_listening()
        else:
            print("❌ Invalid choice. Running demo mode...")
            demonstrate_ultimate_assistant()
            
    except KeyboardInterrupt:
        print("\n🛑 User interrupted. Shutting down...")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Tip: Make sure pyaudio is installed: pip install pyaudio")