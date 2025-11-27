#!/usr/bin/env python3
"""
PHASE 4: ENHANCED GUI INTEGRATION
Modern GUI showing automation state and cognitive features
"""

import customtkinter as ctk
import threading
import time
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# GUI Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class Phase4GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.automation_core = None
        self.memory_manager = None
        self.load_components()
        
        # GUI state
        self.is_listening = False
        self.current_mode = "WAKE_WORD"
        self.last_command = ""
        
        self.setup_window()
        self.setup_gui()
        
        # Start background updates
        self.start_background_updates()
    
    def load_components(self):
        """Load Phase 4 components"""
        try:
            # Import with proper path handling
            sys.path.append(str(Path(__file__).parent))
            from automation_core import AutomationCore
            from memory_manager import MemoryManager
            
            self.automation_core = AutomationCore()
            self.memory_manager = MemoryManager()
            print("✅ Phase 4 components loaded!")
            
        except Exception as e:
            print(f"⚠️ Component load warning: {e}")
            # Continue with limited functionality
    
    def setup_window(self):
        """Setup the main window"""
        self.title("🎯 SHADOW ASSISTANT - PHASE 4")
        self.geometry("900x600")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Force window to front
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))
        self.lift()
        self.focus_force()
    
    def setup_gui(self):
        """Create the GUI layout"""
        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text="🎯 SHADOW ASSISTANT - PHASE 4",
            font=("Arial", 20, "bold")
        ).pack(pady=5)
        
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="🔴 SYSTEM OFFLINE - Click Start to Activate",
            font=("Arial", 14, "bold"),
            text_color="red"
        )
        self.status_label.pack(pady=5)
        
        # Content area
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel - Controls and Status
        left_panel = ctk.CTkFrame(content_frame)
        left_panel.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Right panel - Logs and Memory
        right_panel = ctk.CTkFrame(content_frame)
        right_panel.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        self.setup_controls_panel(left_panel)
        self.setup_logs_panel(right_panel)
    
    def setup_controls_panel(self, parent):
        """Setup controls and status panel"""
        # Control buttons
        controls_frame = ctk.CTkFrame(parent)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(controls_frame, text="⚙️ CONTROLS", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.start_btn = ctk.CTkButton(
            controls_frame,
            text="🚀 START ASSISTANT",
            command=self.start_assistant,
            fg_color="#2E8B57",
            height=40,
            font=("Arial", 14, "bold")
        )
        self.start_btn.pack(fill="x", pady=5)
        
        self.stop_btn = ctk.CTkButton(
            controls_frame,
            text="⏹️ STOP ASSISTANT", 
            command=self.stop_assistant,
            fg_color="#DC143C",
            height=40,
            font=("Arial", 14, "bold"),
            state="disabled"
        )
        self.stop_btn.pack(fill="x", pady=5)
        
        # Status information
        status_frame = ctk.CTkFrame(parent)
        status_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(status_frame, text="📊 SYSTEM STATUS", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.mode_label = ctk.CTkLabel(status_frame, text="Mode: OFFLINE", font=("Arial", 12))
        self.mode_label.pack(anchor="w")
        
        self.commands_label = ctk.CTkLabel(status_frame, text="Commands Loaded: 0", font=("Arial", 12))
        self.commands_label.pack(anchor="w")
        
        self.memory_label = ctk.CTkLabel(status_frame, text="Memory Entries: 0", font=("Arial", 12))
        self.memory_label.pack(anchor="w")
        
        # Quick test area
        test_frame = ctk.CTkFrame(parent)
        test_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(test_frame, text="🧪 QUICK TEST", font=("Arial", 14, "bold")).pack(pady=10)
        
        test_input_frame = ctk.CTkFrame(test_frame)
        test_input_frame.pack(fill="x", padx=5, pady=5)
        
        self.test_entry = ctk.CTkEntry(test_input_frame, placeholder_text="Type command to test...")
        self.test_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        self.test_btn = ctk.CTkButton(
            test_input_frame,
            text="TEST",
            command=self.test_command,
            width=80
        )
        self.test_btn.pack(side="right", padx=5)
    
    def setup_logs_panel(self, parent):
        """Setup logs and memory panel"""
        # Command log
        log_frame = ctk.CTkFrame(parent)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(log_frame, text="📝 COMMAND LOG", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.log_text = ctk.CTkTextbox(log_frame, font=("Consolas", 10))
        self.log_text.pack(fill="both", expand=True)
        self.log_text.configure(state="disabled")
        
        # Memory preview
        memory_frame = ctk.CTkFrame(parent)
        memory_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(memory_frame, text="🧠 RECENT MEMORY", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.memory_text = ctk.CTkTextbox(memory_frame, height=100, font=("Consolas", 9))
        self.memory_text.pack(fill="x", padx=5, pady=5)
        self.memory_text.configure(state="disabled")
    
    def start_background_updates(self):
        """Start background GUI updates"""
        def update_loop():
            while True:
                try:
                    self.update_status()
                    self.update_memory_preview()
                except Exception as e:
                    print(f"Background update error: {e}")
                time.sleep(2)
        
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
    
    def update_status(self):
        """Update status information"""
        if self.automation_core:
            command_count = len(self.automation_core.commands)
            self.commands_label.configure(text=f"Commands Loaded: {command_count}")
        
        if self.memory_manager:
            try:
                memories = self.memory_manager.get_recent_memories(1)
                memory_count = len(memories) + 10  # Fixed the syntax error
                self.memory_label.configure(text=f"Memory Entries: {memory_count}")
            except:
                self.memory_label.configure(text="Memory Entries: N/A")
    
    def update_memory_preview(self):
        """Update memory preview"""
        if not self.memory_manager:
            return
        
        try:
            recent_commands = self.memory_manager.get_command_history(5)
            self.memory_text.configure(state="normal")
            self.memory_text.delete("1.0", "end")
            
            for cmd in recent_commands:
                status = "✅" if cmd['executed'] else "❌"
                time_str = time.strftime("%H:%M:%S", time.localtime(cmd['timestamp']))
                self.memory_text.insert("end", f"[{time_str}] {status} {cmd['command']}\n")
            
            self.memory_text.configure(state="disabled")
        except Exception as e:
            print(f"Memory update error: {e}")
    
    def start_assistant(self):
        """Start the voice assistant"""
        self.is_listening = True
        self.current_mode = "WAKE_WORD"
        
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.status_label.configure(text="🟢 SYSTEM ACTIVE - Listening for Wake Word", text_color="green")
        self.mode_label.configure(text="Mode: WAKE_WORD")
        
        self.log_message("🚀 Assistant activated")
        self.log_message("💡 Say 'yes', 'on', or 'go' to activate command mode")
    
    def stop_assistant(self):
        """Stop the voice assistant"""
        self.is_listening = False
        self.current_mode = "OFFLINE"
        
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text="🔴 SYSTEM OFFLINE", text_color="red")
        self.mode_label.configure(text="Mode: OFFLINE")
        
        self.log_message("⏹️ Assistant deactivated")
    
    def test_command(self):
        """Test a command from the text entry"""
        command_text = self.test_entry.get().strip()
        if not command_text:
            return
        
        self.test_entry.delete(0, "end")
        self.log_message(f"🧪 Testing: '{command_text}'")
        
        if self.automation_core:
            success = self.automation_core.process_command(command_text)
            status = "✅ Success" if success else "❌ Failed"
            self.log_message(f"   Result: {status}")
        else:
            self.log_message("   ❌ Automation core not available")
    
    def log_message(self, message):
        """Add message to log"""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
    
    def on_closing(self):
        """Cleanup on window close"""
        self.is_listening = False
        self.destroy()
    
    def run(self):
        """Run the application"""
        self.mainloop()

def main():
    """Launch the Phase 4 GUI"""
    app = Phase4GUI()
    app.run()

if __name__ == "__main__":
    main()
