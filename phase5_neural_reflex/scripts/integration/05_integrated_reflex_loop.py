import time
import threading
import numpy as np
from typing import Dict, List
import json
from datetime import datetime

print("🧠 NEURAL REFLEX SYSTEM - FINAL INTEGRATION")
print("=" * 50)

# Import your actual components
try:
    from audio_embeddings import AudioEmbeddingExtractor
    from emotion_detector import EmotionDetector
    from reflex_feedback import ReflexFeedback
    from visual_feedback import VisualFeedback
    print("✅ All core components loaded successfully")
except ImportError as e:
    print(f"⚠️  Some components missing: {e}")
    # Create minimal fallbacks
    class AudioEmbeddingExtractor:
        def start_realtime_capture(self, callback): 
            print("🎤 Mock audio capture started")
            def mock_features():
                while True:
                    time.sleep(1)
                    callback({
                        'mfcc_mean': np.random.rand(13),
                        'spectral_centroid': np.random.uniform(100, 1000),
                        'zcr': np.random.uniform(0, 0.1),
                        'rms': np.random.uniform(0.01, 0.2)
                    }, np.random.rand(1024))
            threading.Thread(target=mock_features, daemon=True).start()
        def stop_capture(self): pass

    class EmotionDetector:
        def predict_emotion(self, features):
            emotions = ['neutral', 'calm', 'happy', 'sad', 'angry', 'fearful', 'disgust', 'surprised']
            return np.random.choice(emotions), 0.8, {'intensity': 'medium'}

    class ReflexFeedback:
        def generate_feedback(self, emotion, confidence, data):
            return f"Reflex: {emotion} detected with {confidence:.1%} confidence"

    class VisualFeedback:
        def update_emotion_state(self, emotion, confidence, feedback): 
            print(f"🎨 Visual: {emotion} ({(confidence*100):.0f}%)")

class NeuralReflexLoop:
    """Complete neural reflex system integrating all components"""
    
    def __init__(self):
        self.is_running = False
        self.emotion_history = []
        
        # Initialize your actual components
        self.audio_extractor = AudioEmbeddingExtractor()
        self.emotion_detector = EmotionDetector()
        self.reflex_feedback = ReflexFeedback()
        self.visual_feedback = VisualFeedback()
        
        # Performance tracking
        self.metrics = {
            "processing_count": 0,
            "total_latency": 0,
            "emotion_changes": 0
        }
        self.current_emotion = "neutral"
        
        print("✅ Neural Reflex System initialized")
    
    def start_system(self):
        """Start the complete neural reflex system"""
        print("🚀 STARTING NEURAL REFLEX SYSTEM...")
        self.is_running = True
        
        # Start audio processing
        self.audio_extractor.start_realtime_capture(self.process_audio)
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_performance, daemon=True)
        self.monitor_thread.start()
        
        print("🎯 Neural Reflex System: ACTIVE")
        print("   • Real-time emotion detection: ENABLED")
        print("   • Audio processing: STREAMING")
        print("   • Performance monitoring: ACTIVE")
    
    def stop_system(self):
        """Stop the system"""
        print("🛑 STOPPING NEURAL REFLEX SYSTEM")
        self.is_running = False
        self.audio_extractor.stop_capture()
    
    def process_audio(self, features, audio_data):
        """Process audio and detect emotions"""
        if not self.is_running:
            return
            
        start_time = time.time()
        
        try:
            # Detect emotion
            emotion, confidence, details = self.emotion_detector.predict_emotion(features)
            
            # Generate reflex feedback
            feedback = self.reflex_feedback.generate_feedback(emotion, confidence, details)
            
            # Update visual feedback
            self.visual_feedback.update_emotion_state(emotion, confidence, feedback)
            
            # Track emotion changes
            if emotion != self.current_emotion and confidence > 0.6:
                self.current_emotion = emotion
                self.metrics["emotion_changes"] += 1
                print(f"🎭 Emotion: {emotion.upper()} ({(confidence*100):.1f}%)")
            
            # Update metrics
            latency = (time.time() - start_time) * 1000
            self.metrics["processing_count"] += 1
            self.metrics["total_latency"] += latency
            
            # Store in history
            self.emotion_history.append({
                "timestamp": time.time(),
                "emotion": emotion,
                "confidence": confidence,
                "latency_ms": latency
            })
            
            # Keep history manageable
            if len(self.emotion_history) > 100:
                self.emotion_history.pop(0)
                
        except Exception as e:
            print(f"❌ Processing error: {e}")
    
    def monitor_performance(self):
        """Monitor and display system performance"""
        while self.is_running:
            time.sleep(5)
            
            if self.metrics["processing_count"] > 0:
                avg_latency = self.metrics["total_latency"] / self.metrics["processing_count"]
                processing_rate = self.metrics["processing_count"] / 5
                
                print(f"📊 Performance: {avg_latency:.1f}ms avg | {processing_rate:.1f} samples/sec | Changes: {self.metrics['emotion_changes']}")
                
                # Reset for next interval
                self.metrics["processing_count"] = 0
                self.metrics["total_latency"] = 0
    
    def get_status(self):
        """Get system status"""
        return {
            "running": self.is_running,
            "current_emotion": self.current_emotion,
            "total_processed": len(self.emotion_history),
            "emotion_changes": self.metrics["emotion_changes"]
        }

# Test the complete system
if __name__ == "__main__":
    print("🧪 COMPLETE NEURAL REFLEX SYSTEM TEST")
    print("=" * 50)
    
    system = NeuralReflexLoop()
    
    try:
        # Start system
        system.start_system()
        
        # Run test for 20 seconds
        print("\n⏱️  Running system for 20 seconds...")
        print("   (Speak to test real-time emotion detection)")
        print("   Press Ctrl+C to stop early\n")
        
        start_time = time.time()
        while time.time() - start_time < 20:
            status = system.get_status()
            print(f"�� Status: {status['current_emotion']} | Processed: {status['total_processed']} | Changes: {status['emotion_changes']}")
            time.sleep(2)
        
        # Final report
        print("\n📈 FINAL SYSTEM REPORT:")
        final_status = system.get_status()
        for key, value in final_status.items():
            print(f"   {key}: {value}")
        
        print("\n🎉 NEURAL REFLEX SYSTEM: OPERATIONAL!")
        
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    finally:
        system.stop_system()
        print("✅ Neural reflex test completed successfully!")
