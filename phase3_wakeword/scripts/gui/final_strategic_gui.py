#!/usr/bin/env python3
"""
PHASE 3.5: FINAL WORKING STRATEGIC GUI
Compatible with NumPy 1.26.4 and TensorFlow 2.13.0
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

class FinalStrategicGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 STRATEGIC VOICE ASSISTANT - PHASE 3.5")
        self.root.geometry("1100x750")
        
        # Initialize components
        self.wake_detector = None
        self.command_listener = None
        self.components_loaded = False
        
        # Load components safely
        self.load_components()
        
        # Data buffers for visualization
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
        
    def load_components(self):
        """Load strategic components with error handling"""
        try:
            from ultimate_strategic_wake_word import UltimateStrategicDetector
            from command_listener import VoiceCommandListener
            
            self.wake_detector = UltimateStrategicDetector()
            self.command_listener = VoiceCommandListener()
            self.components_loaded = True
            print("✅ All strategic components loaded successfully!")
            
        except ImportError as e:
            print(f"⚠️ Import error: {e}")
            self.setup_fallback_components()
        except Exception as e:
            print(f"⚠️ Component loading error: {e}")
            self.setup_fallback_components()
    
    def setup_fallback_components(self):
        """Setup fallback components for demonstration"""
        print("🔄 Setting up fallback demonstration mode...")
        
        class FallbackDetector:
            def __init__(self):
                self.wake_word_mapping = {
                    'yes': {'name': 'computer', 'adaptive_threshold': 0.60},
                    'on': {'name': 'assistant', 'adaptive_threshold': 0.55},
                    'go': {'name': 'hey device', 'adaptive_threshold': 0.65}
                }
                self.adaptive_sensitivity = 0.65
                self.labels = ['yes', 'no', 'up', 'down', 'left', 'right', 'on', 'off', 'stop', 'go']
                self.strategy_stats = {
                    'total_predictions': 0,
                    'genuine_detections': 0
                }
            
            def ultimate_prediction(self, audio):
                """Simulated prediction"""
                audio_level = np.sqrt(np.mean(audio**2))
                base_confidence = min(audio_level * 3, 0.95)
                noise = np.random.normal(0, 0.1)
                confidence = max(0.1, min(0.95, base_confidence + noise))
                
                # Occasionally return a high confidence to simulate detection
                if confidence > 0.7 and np.random.random() > 0.85:
                    predicted_class = 0  # 'yes'
                else:
                    predicted_class = np.random.randint(0, len(self.labels))
                
                inference_time = np.random.uniform(2.0, 5.0)
                return predicted_class, confidence, inference_time
            
            def execute_ultimate_decision(self, prediction, confidence, inference_time):
                """Simulated strategic decision"""
                if confidence > self.adaptive_sensitivity:
                    detected_word = self.labels[prediction]
                    if detected_word in self.wake_word_mapping:
                        self.strategy_stats['genuine_detections'] += 1
                        return True
                return False
        
        class FallbackListener:
            def activate_command_mode(self, timeout=30):
                print(f"🎤 Command mode activated for {timeout} seconds")
                time.sleep(2)  # Simulate command listening
                print("🔁 Returning to wake word detection")
        
        self.wake_detector = FallbackDetector()
        self.command_listener = FallbackListener()
        self.components_loaded = True
        print("✅ Fallback demonstration mode activated")
    
    def setup_gui(self):
        """Create the professional GUI layout"""
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header section
        self.setup_header(main_frame)
        
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
        
    def setup_header(self, parent):
        """Setup the header with status information"""
        header_frame = ctk.CTkFrame(parent)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # Title
        ctk.CTkLabel(
            header_frame, 
            text="🎯 STRATEGIC VOICE ASSISTANT", 
            font=("Arial", 24, "bold")
        ).pack(pady=5)
        
        ctk.CTkLabel(
            header_frame,
            text="Phase 3.5 - Multi-Layer Intelligence System",
            font=("Arial", 14),
            text_color="lightblue"
        ).pack(pady=2)
        
        # System status
        mode_status = "FULL STRATEGIC MODE" if hasattr(self.wake_detector, 'load_model') else "DEMONSTRATION MODE"
        self.status_label = ctk.CTkLabel(
            header_frame,
            text=f"🔴 SYSTEM OFFLINE - {mode_status}",
            font=("Arial", 16, "bold"),
            text_color="red"
        )
        self.status_label.pack(pady=10)
        
    def setup_visualization(self, parent):
        """Setup the visualization area"""
        # Real-time monitoring
        monitor_frame = ctk.CTkFrame(parent)
        monitor_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            monitor_frame,
            text="📊 REAL-TIME STRATEGIC MONITORING",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Audio and confidence monitoring
        self.setup_realtime_monitors(monitor_frame)
        
        # Strategic layers
        layers_frame = ctk.CTkFrame(parent)
        layers_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            layers_frame,
            text="🧠 5-LAYER STRATEGIC INTELLIGENCE",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        self.setup_strategic_layers(layers_frame)
        
    def setup_realtime_monitors(self, parent):
        """Setup real-time monitoring widgets"""
        # Two-column layout
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        # Audio monitoring
        audio_frame = ctk.CTkFrame(parent)
        audio_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        ctk.CTkLabel(audio_frame, text="🎵 AUDIO INPUT", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Audio level
        level_frame = ctk.CTkFrame(audio_frame)
        level_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(level_frame, text="Level:").pack(side="left")
        self.audio_level = ctk.CTkProgressBar(level_frame, width=150)
        self.audio_level.pack(side="left", padx=10)
        self.audio_level_label = ctk.CTkLabel(level_frame, text="0.000")
        self.audio_level_label.pack(side="left")
        
        # Activity indicator
        activity_frame = ctk.CTkFrame(audio_frame)
        activity_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(activity_frame, text="Status:").pack(side="left")
        self.activity_indicator = ctk.CTkLabel(
            activity_frame, 
            text="●", 
            font=("Arial", 20),
            text_color="gray"
        )
        self.activity_indicator.pack(side="left", padx=10)
        
        # Confidence monitoring
        confidence_frame = ctk.CTkFrame(parent)
        confidence_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        ctk.CTkLabel(confidence_frame, text="📈 DETECTION CONFIDENCE", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Confidence bar
        self.confidence_bar = ctk.CTkProgressBar(confidence_frame, height=25)
        self.confidence_bar.pack(fill="x", padx=10, pady=5)
        self.confidence_bar.set(0)
        
        self.confidence_value = ctk.CTkLabel(
            confidence_frame,
            text="0.0%",
            font=("Arial", 16, "bold")
        )
        self.confidence_value.pack(pady=5)
        
        # Threshold indicator
        threshold_frame = ctk.CTkFrame(confidence_frame)
        threshold_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(threshold_frame, text="Activation:").pack(side="left")
        self.threshold_label = ctk.CTkLabel(
            threshold_frame, 
            text="65%", 
            font=("Arial", 11, "bold"),
            text_color="yellow"
        )
        self.threshold_label.pack(side="left", padx=10)
        
    def setup_strategic_layers(self, parent):
        """Setup the 5 strategic layers visualization"""
        layers_container = ctk.CTkFrame(parent)
        layers_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid for 5 layers
        for i in range(5):
            layers_container.grid_columnconfigure(i, weight=1)
        
        layer_configs = [
            ("Layer 1", "Basic Threshold", "#FF6B6B"),
            ("Layer 2", "Wake Word Mapping", "#4ECDC4"),
            ("Layer 3", "Temporal Protection", "#45B7D1"),
            ("Layer 4", "Consistency Analysis", "#96CEB4"),
            ("Layer 5", "Word-Specific", "#FFEAA7")
        ]
        
        self.layer_indicators = {}
        
        for i, (name, description, color) in enumerate(layer_configs):
            layer_frame = ctk.CTkFrame(layers_container)
            layer_frame.grid(row=0, column=i, sticky="nsew", padx=3, pady=3)
            
            # Layer indicator
            indicator = ctk.CTkLabel(
                layer_frame,
                text="●",
                font=("Arial", 24),
                text_color="gray"
            )
            indicator.pack(pady=5)
            
            # Layer name
            ctk.CTkLabel(
                layer_frame,
                text=name,
                font=("Arial", 11, "bold")
            ).pack()
            
            # Description
            ctk.CTkLabel(
                layer_frame,
                text=description,
                font=("Arial", 9),
                text_color="lightgray"
            ).pack()
            
            self.layer_indicators[name] = {
                'indicator': indicator,
                'color': color,
                'active': False
            }
    
    def setup_controls(self, parent):
        """Setup the control panel"""
        # System controls
        controls_frame = ctk.CTkFrame(parent)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            controls_frame,
            text="⚙️ SYSTEM CONTROLS",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        self.start_button = ctk.CTkButton(
            controls_frame,
            text="🚀 ACTIVATE STRATEGIC SYSTEM",
            command=self.start_system,
            fg_color="#2E8B57",
            hover_color="#3CB371",
            font=("Arial", 14, "bold"),
            height=45
        )
        self.start_button.pack(fill="x", pady=5)
        
        self.stop_button = ctk.CTkButton(
            controls_frame,
            text="⏹️ DEACTIVATE SYSTEM",
            command=self.stop_system,
            fg_color="#DC143C",
            hover_color="#FF4500",
            font=("Arial", 14, "bold"),
            height=45,
            state="disabled"
        )
        self.stop_button.pack(fill="x", pady=5)
        
        # Wake word targets
        targets_frame = ctk.CTkFrame(parent)
        targets_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            targets_frame,
            text="🎯 ACTIVE WAKE WORDS",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        for word, config in self.wake_detector.wake_word_mapping.items():
            target_text = f"• '{word}' → '{config['name']}'"
            ctk.CTkLabel(targets_frame, text=target_text).pack(anchor="w", pady=2)
        
        # Performance statistics
        stats_frame = ctk.CTkFrame(parent)
        stats_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            stats_frame,
            text="📊 PERFORMANCE STATISTICS",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        self.setup_statistics(stats_frame)
        
        # Detection log
        log_frame = ctk.CTkFrame(parent)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            log_frame,
            text="📝 DETECTION HISTORY",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        self.log_text = ctk.CTkTextbox(log_frame, font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True)
        self.log_text.configure(state="disabled")
    
    def setup_statistics(self, parent):
        """Setup performance statistics"""
        self.stats_labels = {}
        
        stats_config = [
            ("Session Duration:", "0s"),
            ("Total Predictions:", "0"),
            ("Wake Words Detected:", "0"),
            ("Success Rate:", "0%"),
            ("Current Mode:", "OFFLINE"),
            ("Sensitivity:", "65%")
        ]
        
        for label, default in stats_config:
            stat_frame = ctk.CTkFrame(parent)
            stat_frame.pack(fill="x", padx=5, pady=2)
            
            ctk.CTkLabel(stat_frame, text=label, font=("Arial", 11)).pack(side="left")
            value_label = ctk.CTkLabel(stat_frame, text=default, font=("Arial", 11, "bold"))
            value_label.pack(side="right")
            
            self.stats_labels[label] = value_label
    
    def setup_audio_stream(self):
        """Setup audio stream for processing"""
        def audio_callback(indata, frames, time, status):
            if self.is_listening:
                audio_level = float(np.sqrt(np.mean(indata**2)))
                self.audio_data.append(audio_level)
                self.audio_queue.put(indata[:, 0].astype(np.float32))
        
        self.stream = sd.InputStream(
            callback=audio_callback,
            channels=1,
            samplerate=16000,
            blocksize=1024,
            latency='low'
        )
    
    def start_system(self):
        """Start the strategic system"""
        self.is_listening = True
        self.stream.start()
        
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        
        mode_status = "STRATEGIC MODE" if hasattr(self.wake_detector, 'load_model') else "DEMO MODE"
        self.status_label.configure(
            text=f"🟢 SYSTEM ACTIVE - {mode_status}", 
            text_color="green"
        )
        
        self.session_start_time = time.time()
        self.log_message("🚀 STRATEGIC SYSTEM ACTIVATED")
        self.log_message("🎯 5-layer intelligence engaged")
        self.log_message("🔊 Real-time audio processing: ONLINE")
        
        # Start processing thread
        self.processing_thread = threading.Thread(target=self.process_audio, daemon=True)
        self.processing_thread.start()
        
        # Start GUI update thread
        self.gui_thread = threading.Thread(target=self.update_gui, daemon=True)
        self.gui_thread.start()
    
    def stop_system(self):
        """Stop the system"""
        self.is_listening = False
        self.stream.stop()
        
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_label.configure(text="🔴 SYSTEM OFFLINE", text_color="red")
        
        self.log_message("⏹️ Strategic system deactivated")
    
    def process_audio(self):
        """Process audio for wake word detection"""
        while self.is_listening:
            try:
                audio_chunk = self.audio_queue.get(timeout=1.0)
                self.total_predictions += 1
                
                # Get prediction from detector
                prediction, confidence, inference_time = self.wake_detector.ultimate_prediction(audio_chunk)
                self.current_confidence = confidence if prediction is not None else 0.0
                
                if prediction is not None and confidence > 0.3:
                    detected_word = self.wake_detector.labels[prediction]
                    
                    # Check for wake word with strategic decision
                    if hasattr(self.wake_detector, 'execute_ultimate_decision'):
                        # Real strategic decision
                        if (confidence > self.wake_detector.adaptive_sensitivity and 
                            self.wake_detector.execute_ultimate_decision(prediction, confidence, inference_time)):
                            self.handle_detection(detected_word, confidence, inference_time)
                    else:
                        # Fallback decision
                        if confidence > self.wake_detector.adaptive_sensitivity:
                            if detected_word in self.wake_detector.wake_word_mapping:
                                self.handle_detection(detected_word, confidence, inference_time)
                
            except queue.Empty:
                continue
            except Exception as e:
                self.log_message(f"❌ Processing error: {e}")
    
    def handle_detection(self, wake_word, confidence, inference_time):
        """Handle wake word detection"""
        self.genuine_detections += 1
        wake_word_name = self.wake_detector.wake_word_mapping[wake_word]['name']
        timestamp = time.strftime("%H:%M:%S")
        
        log_entry = f"[{timestamp}] 🎯 '{wake_word_name.upper()}' detected ({confidence:.1%}) in {inference_time:.1f}ms"
        self.log_message(log_entry)
        
        # Visual feedback
        self.trigger_detection_animation()
        self.update_statistics()
        
        # Activate command mode
        self.root.after(100, self.activate_command_mode)
    
    def activate_command_mode(self):
        """Activate command listening mode"""
        self.current_mode = "COMMAND"
        self.status_label.configure(
            text="🎤 COMMAND MODE - Listening for voice commands", 
            text_color="yellow"
        )
        
        self.log_message("🎤 Switching to command mode...")
        
        # Activate command listener
        self.command_listener.activate_command_mode(timeout=10)
        
        # Return to wake word mode after command session
        self.root.after(3000, self.return_to_wake_word_mode)
    
    def return_to_wake_word_mode(self):
        """Return to wake word detection mode"""
        self.current_mode = "WAKE_WORD"
        self.status_label.configure(
            text="🟢 SYSTEM ACTIVE - Strategic Listening Engaged", 
            text_color="green"
        )
        
        self.log_message("🔁 Returning to wake word detection")
    
    def trigger_detection_animation(self):
        """Trigger visual detection animation"""
        # Flash all layers gold
        for name, indicator in self.layer_indicators.items():
            indicator['indicator'].configure(text_color="#FFD700")
            indicator['active'] = True
        
        # Reset after delay
        self.root.after(800, self.reset_layer_indicators)
    
    def reset_layer_indicators(self):
        """Reset layer indicators to normal state"""
        for name, indicator in self.layer_indicators.items():
            if indicator['active']:
                indicator['indicator'].configure(text_color=indicator['color'])
            else:
                indicator['indicator'].configure(text_color="gray")
    
    def update_statistics(self):
        """Update performance statistics"""
        session_time = time.time() - self.session_start_time
        self.stats_labels["Session Duration:"].configure(text=f"{session_time:.1f}s")
        self.stats_labels["Total Predictions:"].configure(text=str(self.total_predictions))
        self.stats_labels["Wake Words Detected:"].configure(text=str(self.genuine_detections))
        
        if self.total_predictions > 0:
            success_rate = self.genuine_detections / self.total_predictions
            self.stats_labels["Success Rate:"].configure(text=f"{success_rate:.1%}")
        
        self.stats_labels["Current Mode:"].configure(text=self.current_mode.replace("_", " ").title())
        
        sensitivity = self.wake_detector.adaptive_sensitivity
        self.stats_labels["Sensitivity:"].configure(text=f"{int(sensitivity*100)}%")
        self.threshold_label.configure(text=f"{int(sensitivity*100)}%")
    
    def update_gui(self):
        """Continuous GUI updates"""
        while self.is_listening:
            try:
                # Update audio level
                if self.audio_data:
                    current_level = self.audio_data[-1]
                    display_level = min(current_level * 8, 1.0)
                    self.audio_level.set(display_level)
                    self.audio_level_label.configure(text=f"{current_level:.3f}")
                    
                    # Update activity indicator
                    if current_level > 0.01:
                        self.activity_indicator.configure(text_color="#00FF00")
                    else:
                        self.activity_indicator.configure(text_color="gray")
                
                # Update confidence display
                self.confidence_bar.set(self.current_confidence)
                self.confidence_value.configure(text=f"{self.current_confidence:.1%}")
                
                # Update confidence bar color
                threshold = self.wake_detector.adaptive_sensitivity
                if self.current_confidence > threshold:
                    self.confidence_bar.configure(progress_color="#00FF00")
                elif self.current_confidence > threshold - 0.2:
                    self.confidence_bar.configure(progress_color="#FFFF00")
                else:
                    self.confidence_bar.configure(progress_color="#FF0000")
                
                time.sleep(0.1)
                
            except Exception as e:
                print(f"GUI update error: {e}")
                break
    
    def log_message(self, message):
        """Add message to log"""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
    
    def on_closing(self):
        """Cleanup on window close"""
        self.is_listening = False
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()
        self.root.destroy()

def main():
    """Launch the final strategic GUI"""
    root = ctk.CTk()
    app = FinalStrategicGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
