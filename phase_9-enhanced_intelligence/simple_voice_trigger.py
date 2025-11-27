# simple_voice_trigger.py
import numpy as np
import time
import pyaudio
from hybrid_model_router_optimized import Phase9EnhancedIntelligence

class SimpleVoiceTrigger:
    """Simple voice trigger that works with ANY loud sound"""
    
    def __init__(self, sensitivity=0.02):
        self.sensitivity = sensitivity  # Adjust this based on your mic
        self.hybrid_intelligence = Phase9EnhancedIntelligence()
        self.setup_audio()
        
    def setup_audio(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=16000,  # 1-second chunks
            stream_callback=self.audio_callback
        )
        self.detection_count = 0
        
    def audio_callback(self, in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.int16).astype(np.float32) / 32768.0
        
        # Simple energy-based detection
        energy = np.mean(audio_data ** 2)
        
        if energy > self.sensitivity:
            self.detection_count += 1
            print(f"\n🎯 VOICE DETECTED! (#{self.detection_count})")
            print(f"   🔊 Energy: {energy:.6f}")
            
            # Process with AI
            result = self.hybrid_intelligence.process_audio_intelligently(audio_data)
            
            print(f"   🎭 Emotion: {result['emotion']['emotion']} ({result['emotion']['confidence']:.1%})")
            print(f"   🔔 Wake Word: {result['hybrid_prediction']['wakeword_detected']}")
            print(f"   💬 'Hello! How can I help you?'")
            
        print(f"✅ Listening... | Sensitivity: {self.sensitivity} | Detections: {self.detection_count}", end='\r')
        return (in_data, pyaudio.paContinue)
    
    def start(self):
        print("🎧 SIMPLE VOICE TRIGGER - SPEAK LOUDLY!")
        print("💡 This will trigger on ANY loud sound")
        print("🛑 Press Ctrl+C to stop")
        
        self.stream.start_stream()
        
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        print(f"\n📊 Session summary: {self.detection_count} detections")

# Run the simple version
if __name__ == "__main__":
    trigger = SimpleVoiceTrigger(sensitivity=0.01)  # Adjust sensitivity as needed
    trigger.start()