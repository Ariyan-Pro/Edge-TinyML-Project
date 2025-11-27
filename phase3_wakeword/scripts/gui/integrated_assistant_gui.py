#!/usr/bin/env python3
"""
PHASE 3.5: INTEGRATED STRATEGIC ASSISTANT WITH GUI
Complete voice assistant with visual interface
"""

import customtkinter as ctk
import threading
import time
import queue
import numpy as np
import sounddevice as sd
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from ultimate_strategic_wake_word import UltimateStrategicDetector
from command_listener import VoiceCommandListener

class IntegratedStrategicAssistant:
    def __init__(self):
        # Initialize components
        self.wake_detector = UltimateStrategicDetector()
        self.command_listener = VoiceCommandListener()
        
        # System state
        self.current_mode = "WAKE_WORD"  # WAKE_WORD or COMMAND
        self.is_running = False
        self.audio_queue = queue.Queue()
        
        # Statistics
        self.detection_count = 0
        self.session_start_time = time.time()
        
    def start_system(self):
        """Start the complete integrated system"""
        self.is_running = True
        self.session_start_time = time.time()
        
        # Start audio processing thread
        self.processing_thread = threading.Thread(target=self._audio_processing_loop, daemon=True)
        self.processing_thread.start()
        
        print("🚀 INTEGRATED STRATEGIC ASSISTANT ACTIVATED")
        print("🎯 Mode: Wake Word Detection")
        
    def stop_system(self):
        """Stop the integrated system"""
        self.is_running = False
        print("⏹️ Integrated system stopped")
        
    def _audio_processing_loop(self):
        """Main audio processing loop"""
        def audio_callback(indata, frames, time, status):
            if self.is_running:
                audio_chunk = indata[:, 0].astype(np.float32)
                self.audio_queue.put(audio_chunk)
        
        # Start audio stream
        with sd.InputStream(
            callback=audio_callback,
            channels=1,
            samplerate=16000,
            blocksize=2048,
            latency='low'
        ):
            print("🎹 Audio engine: ACTIVE")
            
            while self.is_running:
                try:
                    audio_chunk = self.audio_queue.get(timeout=1.0)
                    
                    if self.current_mode == "WAKE_WORD":
                        self._process_wake_word_mode(audio_chunk)
                    elif self.current_mode == "COMMAND":
                        # Command mode handled by command_listener
                        pass
                        
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"❌ Processing error: {e}")
                    
    def _process_wake_word_mode(self, audio_chunk):
        """Process audio in wake word detection mode"""
        prediction, confidence, inference_time = self.wake_detector.ultimate_prediction(audio_chunk)
        
        if prediction is not None and confidence > 0.25:
            detected_word = self.wake_detector.labels[prediction]
            
            # Check if it's a wake word with strategic layers
            if (confidence > self.wake_detector.adaptive_sensitivity and 
                detected_word in self.wake_detector.wake_word_mapping):
                
                # Execute strategic decision with all layers
                if self.wake_detector.execute_ultimate_decision(prediction, confidence, inference_time):
                    self._activate_command_mode(detected_word)
    
    def _activate_command_mode(self, wake_word):
        """Switch to command listening mode"""
        self.current_mode = "COMMAND"
        self.detection_count += 1
        
        wake_word_name = self.wake_detector.wake_word_mapping[wake_word]['name']
        print(f"🎯 COMMAND MODE ACTIVATED by '{wake_word_name}'")
        
        # Activate command listener
        self.command_listener.activate_command_mode()
        
        # Return to wake word detection after command session
        self.current_mode = "WAKE_WORD"
        print("🔁 Returned to Wake Word Detection mode")
        
    def get_system_stats(self):
        """Get current system statistics"""
        session_duration = time.time() - self.session_start_time
        stats = self.wake_detector.strategy_stats.copy()
        stats.update({
            'session_duration': session_duration,
            'detection_count': self.detection_count,
            'current_mode': self.current_mode,
            'sensitivity': self.wake_detector.adaptive_sensitivity
        })
        return stats

class IntegratedAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Integrated Strategic Assistant - Phase 3.5")
        self.root.geometry("1000x700")
        
        self.assistant = IntegratedStrategicAssistant()
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the integrated assistant GUI"""
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text="🎯 INTEGRATED STRATEGIC ASSISTANT",
            font=("Arial", 24, "bold")
        ).pack(pady=5)
        
        ctk.CTkLabel(
            header_frame,
            text="Phase 3.5 - Complete Voice Control System",
            font=("Arial", 14)
        ).pack(pady=5)
        
        # Status display
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="x", padx=10, pady=10)
        
        self.mode_label = ctk.CTkLabel(
            status_frame,
            text="Current Mode: WAKE WORD DETECTION",
            font=("Arial", 16, "bold"),
            text_color="#4ECDC4"
        )
        self.mode_label.pack(pady=10)
        
        # Controls
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        self.start_button = ctk.CTkButton(
            controls_frame,
            text="🚀 START INTEGRATED SYSTEM",
            command=self.start_system,
            fg_color="#2E8B57",
            hover_color="#3CB371",
            font=("Arial", 16, "bold"),
            height=50
        )
        self.start_button.pack(fill="x", padx=20, pady=10)
        
        self.stop_button = ctk.CTkButton(
            controls_frame,
            text="⏹️ STOP SYSTEM",
            command=self.stop_system,
            fg_color="#DC143C", 
            hover_color="#FF4500",
            font=("Arial", 16, "bold"),
            height=50,
            state="disabled"
        )
        self.stop_button.pack(fill="x", padx=20, pady=10)
        
        # Statistics
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            stats_frame,
            text="📊 SYSTEM STATISTICS",
            font=("Arial", 18, "bold")
        ).pack(pady=10)
        
        # Stats grid
        self.stats_labels = {}
        stats_grid = ctk.CTkFrame(stats_frame)
        stats_grid.pack(fill="both", expand=True, padx=20, pady=20)
        
        stats_config = [
            ("Session Duration:", "0s"),
            ("Wake Word Detections:", "0"),
            ("Total Predictions:", "0"), 
            ("Genuine Detections:", "0"),
            ("Success Rate:", "0%"),
            ("Current Sensitivity:", "65%")
        ]
        
        for i, (label, value) in enumerate(stats_config):
            row = i % 3
            col = i // 3
            
            stat_frame = ctk.CTkFrame(stats_grid)
            stat_frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            
            ctk.CTkLabel(
                stat_frame,
                text=label,
                font=("Arial", 12)
            ).pack(side="left", padx=5)
            
            value_label = ctk.CTkLabel(
                stat_frame,
                text=value,
                font=("Arial", 12, "bold")
            )
            value_label.pack(side="right", padx=5)
            
            self.stats_labels[label] = value_label
        
        # Start GUI updates
        self.update_gui()
        
    def start_system(self):
        """Start the integrated system"""
        self.assistant.start_system()
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.mode_label.configure(text="Current Mode: WAKE WORD DETECTION", text_color="#4ECDC4")
        
    def stop_system(self):
        """Stop the integrated system"""
        self.assistant.stop_system()
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.mode_label.configure(text="Current Mode: SYSTEM OFFLINE", text_color="#DC143C")
        
    def update_gui(self):
        """Update GUI with current statistics"""
        if self.assistant.is_running:
            stats = self.assistant.get_system_stats()
            
            # Update mode display
            mode_text = f"Current Mode: {stats['current_mode'].replace('_', ' ').title()}"
            mode_color = "#4ECDC4" if stats['current_mode'] == "WAKE_WORD" else "#FFD700"
            self.mode_label.configure(text=mode_text, text_color=mode_color)
            
            # Update statistics
            self.stats_labels["Session Duration:"].configure(
                text=f"{stats['session_duration']:.1f}s"
            )
            self.stats_labels["Wake Word Detections:"].configure(
                text=str(stats['detection_count'])
            )
            self.stats_labels["Total Predictions:"].configure(
                text=str(stats['total_predictions'])
            )
            self.stats_labels["Genuine Detections:"].configure(
                text=str(stats['genuine_detections'])
            )
            
            if stats['total_predictions'] > 0:
                success_rate = stats['genuine_detections'] / stats['total_predictions']
                self.stats_labels["Success Rate:"].configure(
                    text=f"{success_rate:.1%}"
                )
            
            self.stats_labels["Current Sensitivity:"].configure(
                text=f"{int(stats['sensitivity']*100)}%"
            )
        
        # Schedule next update
        self.root.after(1000, self.update_gui)

def main():
    """Launch the integrated assistant GUI"""
    root = ctk.CTk()
    app = IntegratedAssistantGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
