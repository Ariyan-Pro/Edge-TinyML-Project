#!/usr/bin/env python3
"""
Integrated Voice Assistant - Phase 3
Combines wake word detection and voice commands
"""

import threading
import time
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

class IntegratedAssistant:
    def __init__(self):
        self.is_running = False
        self.current_mode = "sleep"  # sleep, wake_word, command
        
        # Import our components
        try:
            from wake_word_detector import WakeWordDetector
            from command_listener import VoiceCommandSystem
            
            self.wake_detector = WakeWordDetector()
            self.voice_system = VoiceCommandSystem()
            
            print("✅ All assistant components loaded!")
            
        except ImportError as e:
            print(f"❌ Failed to load components: {e}")
            sys.exit(1)
    
    def start_wake_word_detection(self):
        """Start listening for wake word"""
        print("\n🔔 Wake word detection started...")
        self.current_mode = "wake_word"
        
        # Modified wake word detection that calls command mode
        def wake_callback():
            print("🎯 Wake word detected! Switching to command mode...")
            self.start_command_mode()
        
        # We'll modify the wake detector to use a callback
        self.wake_detector.is_listening = True
        
        try:
            with self.wake_detector.audio_stream:
                while self.wake_detector.is_listening and self.is_running:
                    # Check for wake word in the callback
                    time.sleep(0.1)
                    
        except Exception as e:
            print(f"❌ Wake word detection error: {e}")
    
    def start_command_mode(self):
        """Start listening for voice commands"""
        print("\n🎙️ Command mode activated...")
        self.current_mode = "command"
        
        # Speak confirmation
        self.voice_system.speak("I'm listening for your command")
        
        # Listen for commands for 30 seconds
        self.voice_system.listen_for_commands(timeout=30)
        
        # Return to wake word detection
        print("\n🔔 Returning to wake word detection...")
        self.voice_system.speak("Going back to sleep")
        self.current_mode = "wake_word"
    
    def run(self):
        """Main assistant loop"""
        print("="*60)
        print("🤖 INTEGRATED VOICE ASSISTANT - PHASE 3")
        print("="*60)
        print("Modes:")
        print("  1. Wake Word Detection (always listening)")
        print("  2. Voice Commands (after wake word)")
        print("  3. Press Ctrl+C to exit")
        print("-"*60)
        
        self.is_running = True
        
        try:
            # Start with wake word detection
            while self.is_running:
                if self.current_mode == "wake_word":
                    print("💤 Sleeping... waiting for wake word")
                    # Simpler approach - just run wake word detection
                    self.wake_detector.listen_for_wake_word(timeout=30)
                    
                    # If we get here, either timeout or wake word detected
                    if self.is_running:
                        self.start_command_mode()
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n⏹️ Assistant stopped by user")
        finally:
            self.is_running = False

def main():
    """Main function"""
    assistant = IntegratedAssistant()
    assistant.run()

if __name__ == "__main__":
    main()
