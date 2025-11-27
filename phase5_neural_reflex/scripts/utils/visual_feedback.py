import matplotlib.pyplot as plt
import numpy as np

class VisualFeedback:
    def __init__(self):
        self.emotion_history = []
        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        
    def update_display(self, emotion_data, reflex_state):
        """Update visual display based on emotion and reflex state"""
        self.emotion_history.append(emotion_data['emotion'])
        
        # Color mapping based on reflex state
        colors = {
            'calm': 'green',
            'focused': 'blue', 
            'alert': 'red'
        }
        
        color = colors.get(reflex_state, 'gray')
        
        # Simple visualization
        emotion_counts = {}
        for emotion in set(self.emotion_history[-10:]):  # Last 10 emotions
            emotion_counts[emotion] = self.emotion_history[-10:].count(emotion)
            
        # Update plot
        self.ax.clear()
        emotions = list(emotion_counts.keys())
        counts = list(emotion_counts.values())
        
        bars = self.ax.bar(emotions, counts, color=color, alpha=0.7)
        self.ax.set_title(f'Emotion Analysis - Reflex State: {reflex_state.upper()}')
        self.ax.set_ylabel('Frequency')
        
        plt.pause(0.1)
        
    def show_final_report(self):
        """Show final emotion analysis"""
        print("📊 FINAL EMOTION ANALYSIS:")
        for emotion in set(self.emotion_history):
            count = self.emotion_history.count(emotion)
            percentage = (count / len(self.emotion_history)) * 100
            print(f"   {emotion}: {count} times ({percentage:.1f}%)")
