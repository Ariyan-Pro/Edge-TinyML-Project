# wake_word_diagnostic.py
import tensorflow as tf
import numpy as np
import time
import pyaudio
import wave
from hybrid_model_router_optimized import Phase9EnhancedIntelligence

class WakeWordDiagnostic:
    """Diagnose what's actually happening with wake word detection"""
    
    def __init__(self):
        print("🔍 WAKE WORD DIAGNOSTIC TOOL")
        self.hybrid_intelligence = Phase9EnhancedIntelligence()
        self.setup_audio()
        
    def setup_audio(self):
        """Setup audio for recording"""
        self.audio_interface = pyaudio.PyAudio()
        self.sample_rate = 16000
        self.chunk_size = 1024
        
    def record_and_test(self, duration=3, filename="test_recording.wav"):
        """Record audio and test wake word detection"""
        print(f"\n🎤 Recording {duration} seconds of audio...")
        print("💡 Speak your wake word clearly!")
        
        # Record audio
        stream = self.audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        frames = []
        for i in range(0, int(self.sample_rate / self.chunk_size * duration)):
            data = stream.read(self.chunk_size, exception_on_overflow=False)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        
        # Convert to numpy array
        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16).astype(np.float32) / 32768.0
        
        # Save recording
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes((audio_data * 32768.0).astype(np.int16).tobytes())
        
        print(f"💾 Saved recording: {filename}")
        
        return audio_data
    
    def analyze_audio(self, audio_data):
        """Comprehensive audio analysis"""
        print("\n📊 ANALYZING AUDIO...")
        
        # Basic audio stats
        energy = np.mean(audio_data ** 2)
        max_amplitude = np.max(np.abs(audio_data))
        print(f"   🔊 Audio Energy: {energy:.6f}")
        print(f"   📈 Max Amplitude: {max_amplitude:.6f}")
        
        # Test with hybrid intelligence
        print("   🧠 Testing with AI models...")
        result = self.hybrid_intelligence.process_audio_intelligently(audio_data)
        
        # Detailed analysis
        print(f"\n🎯 WAKE WORD ANALYSIS:")
        print(f"   🔔 Wake Word Detected: {result['hybrid_prediction']['wakeword_detected']}")
        print(f"   📊 Confidence: {result['hybrid_prediction']['final_confidence']:.1%}")
        print(f"   🎭 Emotion: {result['emotion']['emotion']} ({result['emotion']['confidence']:.1%})")
        print(f"   ⚡ Processing Time: {result['performance']['total_time_ms']:.1f}ms")
        
        # Model-specific details
        print(f"\n🔍 MODEL DETAILS:")
        print(f"   Emotion Model Confidence: {result['emotion']['confidence']:.1%}")
        print(f"   WakeWord Model Confidence: {result['wakeword']['confidence']:.1%}")
        
        return result
    
    def test_common_wake_words(self):
        """Test what wake words the model actually recognizes"""
        print("\n🧪 TESTING COMMON WAKE WORDS:")
        common_words = ["yes", "no", "stop", "go", "up", "down", "left", "right", "on", "off"]
        
        for word in common_words:
            print(f"\n🎯 Testing: '{word}'")
            audio = self.record_and_test(2, f"test_{word}.wav")
            result = self.analyze_audio(audio)
            
            if result['hybrid_prediction']['wakeword_detected']:
                print(f"   ✅ '{word}' - DETECTED! ({result['hybrid_prediction']['final_confidence']:.1%})")
            else:
                print(f"   ❌ '{word}' - Not detected")
            
            time.sleep(1)  # Brief pause between tests
    
    def continuous_listening_test(self, duration=30):
        """Test continuous listening to see what triggers detection"""
        print(f"\n🔄 CONTINUOUS LISTENING TEST ({duration} seconds)")
        print("💡 Speak different words and see what gets detected...")
        
        stream = self.audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.sample_rate  # 1-second chunks
        )
        
        start_time = time.time()
        detection_count = 0
        
        while time.time() - start_time < duration:
            try:
                # Record 1 second of audio
                data = stream.read(self.sample_rate, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
                
                # Test for wake word
                result = self.hybrid_intelligence.process_audio_intelligently(audio_data)
                
                if result['hybrid_prediction']['wakeword_detected']:
                    detection_count += 1
                    print(f"🎯 DETECTION #{detection_count}:")
                    print(f"   Confidence: {result['hybrid_prediction']['final_confidence']:.1%}")
                    print(f"   Emotion: {result['emotion']['emotion']}")
                    print(f"   Time: {time.time() - start_time:.1f}s")
                
                # Progress indicator
                elapsed = time.time() - start_time
                print(f"⏱️  {elapsed:.1f}s | Detections: {detection_count} | Listening...", end='\r')
                
            except Exception as e:
                print(f"❌ Error: {e}")
                break
        
        stream.stop_stream()
        stream.close()
        
        print(f"\n📊 TEST COMPLETE:")
        print(f"   Total Detections: {detection_count}")
        print(f"   Detections per minute: {detection_count / (duration/60):.1f}")
    
    def cleanup(self):
        """Cleanup resources"""
        self.audio_interface.terminate()

def main():
    diagnostic = WakeWordDiagnostic()
    
    print("Choose diagnostic mode:")
    print("1. Single recording test")
    print("2. Test common wake words") 
    print("3. Continuous listening test")
    print("4. Full diagnostic suite")
    
    try:
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "1":
            audio = diagnostic.record_and_test()
            diagnostic.analyze_audio(audio)
            
        elif choice == "2":
            diagnostic.test_common_wake_words()
            
        elif choice == "3":
            diagnostic.continuous_listening_test()
            
        elif choice == "4":
            print("🚀 RUNNING FULL DIAGNOSTIC SUITE...")
            audio = diagnostic.record_and_test()
            diagnostic.analyze_audio(audio)
            diagnostic.test_common_wake_words()
            diagnostic.continuous_listening_test(20)
            
        else:
            print("❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n👋 Diagnostic interrupted")
    except Exception as e:
        print(f"❌ Diagnostic failed: {e}")
    finally:
        diagnostic.cleanup()

if __name__ == "__main__":
    main()