# phase5_neural_reflex/scripts/03_reflex_feedback.py
import time
import threading
from collections import deque

class ReflexFeedbackSystem:
    def __init__(self):
        self.emotion_history = deque(maxlen=10)  # Last 10 emotions
        self.current_state = 'calm'
        self.state_callbacks = []
        
    def update_emotion(self, emotion_data):
        """Update system with new emotion data"""
        self.emotion_history.append(emotion_data)
        new_state = self.calculate_reflex_state()
        
        if new_state != self.current_state:
            self.current_state = new_state
            self.notify_state_change(new_state)
            
        return new_state
    
    def calculate_reflex_state(self):
        """Calculate current reflex state from emotion history"""
        if not self.emotion_history:
            return 'calm'
            
        recent_emotions = [e['emotion'] for e in list(self.emotion_history)[-5:]]
        
        # Count alert emotions
        alert_count = sum(1 for e in recent_emotions if e in ['angry', 'fearful', 'surprised'])
        
        if alert_count >= 3:
            return 'alert'
        elif any(e in ['happy', 'focused'] for e in recent_emotions):
            return 'focused'
        else:
            return 'calm'
    
    def add_state_callback(self, callback):
        """Register callback for state changes"""
        self.state_callbacks.append(callback)
        
    def notify_state_change(self, new_state):
        """Notify all callbacks of state change"""
        for callback in self.state_callbacks:
            try:
                callback(new_state)
            except Exception as e:
                print(f"Callback error: {e}")
    
    def get_reflex_parameters(self):
        """Get parameters based on current reflex state"""
        params = {
            'calm': {
                'response_speed': 1.0,
                'voice_tone': 'gentle',
                'processing_depth': 'normal',
                'ui_color': '#2E8B57'  # Sea Green
            },
            'focused': {
                'response_speed': 0.7, 
                'voice_tone': 'clear',
                'processing_depth': 'enhanced',
                'ui_color': '#1E90FF'  # Dodger Blue
            },
            'alert': {
                'response_speed': 0.3,
                'voice_tone': 'crisp',
                'processing_depth': 'minimal', 
                'ui_color': '#FF4500'  # Orange Red
            }
        }
        return params.get(self.current_state, params['calm'])
