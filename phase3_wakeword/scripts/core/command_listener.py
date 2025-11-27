#!/usr/bin/env python3
"""
PROPER VOICE COMMAND LISTENER WITH CLASS STRUCTURE
Optimized for GUI integration and robustness
"""

import os
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import pyautogui
import pyttsx3
import threading
import time

class VoiceCommandListener:
    def __init__(self, model_path=r"..\models\vosk-model"):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.current_command = ""
        
        # Enhanced command dictionary
        self.commands = {
            "open browser": lambda: os.system("start chrome"),
            "open notepad": lambda: os.system("notepad"),
            "open calculator": lambda: os.system("calc"),
            "play music": lambda: os.system("start wmplayer"),
            "shutdown computer": lambda: os.system("shutdown /s /t 30"),
            "cancel shutdown": lambda: os.system("shutdown /a"),
            "sleep": lambda: os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0"),
            "what time is it": self.speak_time,
            "stop listening": self.stop_listening
        }
        
        print("✅ Voice Command Listener initialized")
    
    def speak_time(self):
        """Speak the current time"""
        from datetime import datetime
        current_time = datetime.now().strftime("%I:%M %p")
        self.engine.say(f"The time is {current_time}")
        self.engine.runAndWait()
    
    def stop_listening(self):
        """Stop the command listener"""
        self.is_listening = False
        print("🛑 Command listening stopped")
    
    def audio_callback(self, indata, frames, time, status):
        """Audio callback for command listening"""
        if self.is_listening:
            self.audio_queue.put(bytes(indata))
    
    def activate_command_mode(self, timeout=30):
        """Activate command listening mode"""
        print(f"🎤 COMMAND MODE ACTIVATED - Listening for {timeout} seconds")
        self.is_listening = True
        
        # Speak confirmation
        self.engine.say("Command mode activated. I'm listening for your commands.")
        self.engine.runAndWait()
        
        try:
            with sd.RawInputStream(
                samplerate=16000,
                blocksize=8000,
                dtype='int16',
                channels=1,
                callback=self.audio_callback
            ):
                command_start = time.time()
                
                while self.is_listening and (time.time() - command_start < timeout):
                    try:
                        data = self.audio_queue.get(timeout=1.0)
                        
                        if self.recognizer.AcceptWaveform(data):
                            result = json.loads(self.recognizer.Result())
                            text = result.get("text", "").lower().strip()
                            
                            if text:
                                print(f"🎤 Recognized: '{text}'")
                                self.current_command = text
                                
                                # Check for command matches
                                command_executed = False
                                for key, func in self.commands.items():
                                    if key in text:
                                        print(f"🎯 Executing: {key}")
                                        func()
                                        command_executed = True
                                        break
                                
                                if command_executed:
                                    break  # Return after executing one command
                    
                    except queue.Empty:
                        continue
                    except Exception as e:
                        print(f"❌ Command processing error: {e}")
                
        except Exception as e:
            print(f"❌ Command mode error: {e}")
        
        finally:
            self.is_listening = False
            print("🔁 Returning to wake word detection")
    
    def get_status(self):
        """Get current listener status"""
        return {
            "is_listening": self.is_listening,
            "current_command": self.current_command
        }

# Legacy function for backward compatibility
def listen():
    """Legacy function - use VoiceCommandListener class instead"""
    listener = VoiceCommandListener()
    listener.activate_command_mode()

if __name__ == "__main__":
    listen()
