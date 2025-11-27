#!/usr/bin/env python3
"""
PHASE 3.5: STRATEGIC GUI - FORCE FRONT LAUNCH
Ensures window appears in foreground
"""

import customtkinter as ctk
import numpy as np
import sounddevice as sd
import threading
import time
import queue
from collections import deque
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# GUI Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class StrategicGUI:
    def __init__(self):
        # Create root window first
        self.root = ctk.CTk()
        self.setup_window()
        
        # Initialize components
        self.wake_detector = None
        self.command_listener = None
        self.load_components()
        
        # Data buffers
        self.audio_data = deque(maxlen=100)
        self.confidence_history = deque(maxlen=30)
        self.detection_log = deque(maxlen=15)
        
        # Performance tracking
        self.session_start_time = time.time()
        self.total_predictions = 0
        self.genuine_detections = 0
        self.current_confidence = 0.0
        
        # GUI state
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.current_mode = "WAKE_WORD"
        
        self.setup_gui()
        self.setup_audio_stream()
        
        # Force window to front
        self.bring_to_front()
    
    def setup_window(self):
        """Setup the main window"""
        self.root.title("🎯 STRATEGIC VOICE ASSISTANT - PHASE 3.5")
        self.root.geometry("1000x700")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Force window to appear in foreground
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))
    
    def bring_to_front(self):
        """Force window to front"""
        self.root.lift()
        self.root.focus_force()
        self.root.after(100, self.root.lift)
        self.root.after(200, self.root.focus_force)
    
    def load_components(self):
        """Load strategic components"""
        try:
            from ultimate_strategic_wake_word import UltimateStrategicDetector
            from command_listener import VoiceCommandListener
            
            self.wake_detector = UltimateStrategicDetector()
            self.command_listener = VoiceCommandListener()
            print("✅ Strategic components loaded!")
            
        except Exception as e:
            print(f"⚠️ Using fallback mode: {e}")
            self.setup_fallback_components()
    
    def setup_fallback_components(self):
        """Setup fallback components"""
        class FallbackDetector:
            def __init__(self):
                self.wake_word_mapping = {
                    'yes': {'name': 'computer', 'adaptive_threshold': 0.60},
                    'on': {'name': 'assistant', 'adaptive_threshold': 0.55},
                    'go': {'name': 'hey device', 'adaptive_threshold': 0.65}
                }
                self.adaptive_sensitivity = 0.65
                self.labels = ['yes', 'no', 'up', 'down', 'left', 'right', 'on', 'off', 'stop', 'go']
            
            def ultimate_prediction(self, audio):
                audio_level = np.sqrt(np.mean(audio**2))
                base_confidence = min(audio_level * 3, 0.95)
                noise = np.random.normal(0, 0.1)
                confidence = max(0.1, min(0.95, base_confidence + noise))
                predicted_class = np.random.randint(0, len(self.labels))
                inference_time = np.random.uniform(2.0, 5.0)
                return predicted_class, confidence, inference_time
        
        class FallbackListener:
            def activate_command_mode(self, timeout=30):
                print(f"🎤 Command mode activated for {timeout}s")
                time.sleep(2)
                print("🔁 Returning to wake word detection")
        
        self.wake_detector = FallbackDetector()
        self.command_listener = FallbackListener()
    
    def setup_gui(self):
        """Create the GUI layout"""
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            header_frame, 
            text="🎯 STRATEGIC VOICE ASSISTANT - PHASE 3.5", 
            font=("Arial", 20, "bold")
        ).pack(pady=5)
        
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="🔴 SYSTEM OFFLINE - Ready for Activation",
            font=("Arial", 14, "bold"),
            text_color="red"
        )
        self.status_label.pack(pady=10)
        
        # Content area
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left - Visualization
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Right - Controls
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.pack(side="right", fill="both", expand=False, padx=5, pady=5)
        
        self.setup_visualization(left_frame)
        self.setup_controls(right_frame)
    
    def setup_visualization(self, parent):
        """Setup visualization area"""
        # Monitoring
        monitor_frame = ctk.CTkFrame(parent)
        monitor_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(monitor_frame, text="📊 REAL-TIME MONITORING", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Audio level
        audio_frame = ctk.CTkFrame(monitor_frame)
        audio_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(audio_frame, text="Audio Level:").pack(side="left")
        self.audio_level = ctk.CTkProgressBar(audio_frame, width=150)
        self.audio_level.pack(side="left", padx=10)
        self.audio_level_label = ctk.CTkLabel(audio_frame, text="0.000")
        self.audio_level_label.pack(side="left")
        
        # Confidence
        confidence_frame = ctk.CTkFrame(monitor_frame)
        confidence_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(confidence_frame, text="Confidence:").pack()
        self.confidence_bar = ctk.CTkProgressBar(confidence_frame, height=20)
        self.confidence_bar.pack(fill="x", pady=5)
        self.confidence_value = ctk.CTkLabel(confidence_frame, text="0.0%", font=("Arial", 14, "bold"))
        self.confidence_value.pack()
        
        # Strategic layers
        layers_frame = ctk.CTkFrame(parent)
        layers_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(layers_frame, text="🧠 STRATEGIC LAYERS", font=("Arial", 16, "bold")).pack(pady=10)
        
        layers = [
            ("Layer 1", "Basic Threshold"),
            ("Layer 2", "Wake Word Mapping"),
            ("Layer 3", "Temporal Protection"),
            ("Layer 4", "Consistency Analysis"),
            ("Layer 5", "Word-Specific")
        ]
        
        self.layer_indicators = {}
        
        for name, desc in layers:
            layer_frame = ctk.CTkFrame(layers_frame)
            layer_frame.pack(fill="x", padx=10, pady=3)
            
            ctk.CTkLabel(layer_frame, text=name, font=("Arial", 12, "bold"), width=120).pack(side="left")
            ctk.CTkLabel(layer_frame, text=desc, font=("Arial", 10)).pack(side="left")
            
            indicator = ctk.CTkLabel(layer_frame, text="●", font=("Arial", 20), text_color="gray", width=30)
            indicator.pack(side="right")
            
            self.layer_indicators[name] = indicator
    
    def setup_controls(self, parent):
        """Setup control panel"""
        controls_frame = ctk.CTkFrame(parent)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(controls_frame, text="⚙️ CONTROLS", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.start_btn = ctk.CTkButton(
            controls_frame,
            text="🚀 START SYSTEM",
            command=self.start_system,
            fg_color="#2E8B57",
            height=40,
            font=("Arial", 14, "bold")
        )
        self.start_btn.pack(fill="x", pady=5)
        
        self.stop_btn = ctk.CTkButton(
            controls_frame,
            text="⏹️ STOP SYSTEM",
            command=self.stop_system,
            fg_color="#DC143C",
            height=40,
            font=("Arial", 14, "bold"),
            state="disabled"
        )
        self.stop_btn.pack(fill="x", pady=5)
        
        # Stats
        stats_frame = ctk.CTkFrame(parent)
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(stats_frame, text="📈 STATISTICS", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.stats_labels = {}
        stats = [
            ("Session:", "0s"),
            ("Predictions:", "0"),
            ("Detections:", "0"),
            ("Mode:", "OFFLINE")
        ]
        
        for label, default in stats:
            stat_frame = ctk.CTkFrame(stats_frame)
            stat_frame.pack(fill="x", padx=5, pady=2)
            
            ctk.CTkLabel(stat_frame, text=label).pack(side="left")
            value_label = ctk.CTkLabel(stat_frame, text=default, font=("Arial", 11, "bold"))
            value_label.pack(side="right")
            
            self.stats_labels[label] = value_label
        
        # Log
        log_frame = ctk.CTkFrame(parent)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(log_frame, text="📝 DETECTION LOG", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.log_text = ctk.CTkTextbox(log_frame, font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True)
        self.log_text.configure(state="disabled")
    
    def setup_audio_stream(self):
        """Setup audio stream"""
        def audio_callback(indata, frames, time, status):
            if self.is_listening:
                audio_level = float(np.sqrt(np.mean(indata**2)))
                self.audio_data.append(audio_level)
                self.audio_queue.put(indata[:, 0].astype(np.float32))
        
        self.stream = sd.InputStream(
            callback=audio_callback,
            channels=1,
            samplerate=16000,
            blocksize=1024
        )
    
    def start_system(self):
        """Start the system"""
        self.is_listening = True
        self.stream.start()
        
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.status_label.configure(text="🟢 SYSTEM ACTIVE", text_color="green")
        
        self.session_start_time = time.time()
        self.log_message("🚀 System activated")
        
        # Start processing
        self.processing_thread = threading.Thread(target=self.process_audio, daemon=True)
        self.processing_thread.start()
        
        # Start GUI updates
        self.gui_thread = threading.Thread(target=self.update_gui, daemon=True)
        self.gui_thread.start()
    
    def stop_system(self):
        """Stop the system"""
        self.is_listening = False
        self.stream.stop()
        
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text="🔴 SYSTEM OFFLINE", text_color="red")
        
        self.log_message("⏹️ System deactivated")
    
    def process_audio(self):
        """Process audio data"""
        while self.is_listening:
            try:
                audio_chunk = self.audio_queue.get(timeout=1.0)
                self.total_predictions += 1
                
                prediction, confidence, inference_time = self.wake_detector.ultimate_prediction(audio_chunk)
                self.current_confidence = confidence if prediction is not None else 0.0
                
                if prediction is not None and confidence > 0.3:
                    detected_word = self.wake_detector.labels[prediction]
                    
                    if confidence > self.wake_detector.adaptive_sensitivity:
                        if detected_word in self.wake_detector.wake_word_mapping:
                            self.genuine_detections += 1
                            self.root.after(0, lambda: self.handle_detection(detected_word, confidence))
                
            except queue.Empty:
                continue
            except Exception as e:
                self.log_message(f"❌ Error: {e}")
    
    def handle_detection(self, wake_word, confidence):
        """Handle detection"""
        wake_word_name = self.wake_detector.wake_word_mapping[wake_word]['name']
        timestamp = time.strftime("%H:%M:%S")
        
        log_entry = f"[{timestamp}] 🎯 '{wake_word_name}' ({confidence:.1%})"
        self.log_message(log_entry)
        
        # Visual feedback
        for indicator in self.layer_indicators.values():
            indicator.configure(text_color="#FFD700")
        
        self.root.after(800, self.reset_indicators)
        self.update_stats()
        
        # Activate command mode
        self.root.after(100, self.activate_command_mode)
    
    def activate_command_mode(self):
        """Activate command mode"""
        self.current_mode = "COMMAND"
        self.status_label.configure(text="🎤 COMMAND MODE", text_color="yellow")
        self.log_message("🎤 Command mode activated")
        
        self.command_listener.activate_command_mode(timeout=10)
        
        self.root.after(3000, self.return_to_wake_word)
    
    def return_to_wake_word(self):
        """Return to wake word mode"""
        self.current_mode = "WAKE_WORD"
        self.status_label.configure(text="🟢 SYSTEM ACTIVE", text_color="green")
        self.log_message("🔁 Back to wake word detection")
    
    def reset_indicators(self):
        """Reset layer indicators"""
        for indicator in self.layer_indicators.values():
            indicator.configure(text_color="gray")
    
    def update_stats(self):
        """Update statistics"""
        session_time = time.time() - self.session_start_time
        self.stats_labels["Session:"].configure(text=f"{session_time:.1f}s")
        self.stats_labels["Predictions:"].configure(text=str(self.total_predictions))
        self.stats_labels["Detections:"].configure(text=str(self.genuine_detections))
        self.stats_labels["Mode:"].configure(text=self.current_mode)
    
    def update_gui(self):
        """Update GUI elements"""
        while self.is_listening:
            try:
                # Update audio level
                if self.audio_data:
                    current_level = self.audio_data[-1]
                    display_level = min(current_level * 8, 1.0)
                    self.audio_level.set(display_level)
                    self.audio_level_label.configure(text=f"{current_level:.3f}")
                
                # Update confidence
                self.confidence_bar.set(self.current_confidence)
                self.confidence_value.configure(text=f"{self.current_confidence:.1%}")
                
                # Update confidence color
                threshold = self.wake_detector.adaptive_sensitivity
                if self.current_confidence > threshold:
                    self.confidence_bar.configure(progress_color="#00FF00")
                elif self.current_confidence > threshold - 0.2:
                    self.confidence_bar.configure(progress_color="#FFFF00")
                else:
                    self.confidence_bar.configure(progress_color="#FF0000")
                
                time.sleep(0.1)
                
            except Exception as e:
                break
    
    def log_message(self, message):
        """Add message to log"""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
    
    def on_closing(self):
        """Cleanup on close"""
        self.is_listening = False
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()
        self.root.destroy()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Launch the strategic GUI"""
    app = StrategicGUI()
    app.run()

if __name__ == "__main__":
    main()
