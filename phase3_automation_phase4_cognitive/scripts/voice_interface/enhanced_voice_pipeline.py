# scripts/enhanced_voice_pipeline.py - FIXED VERSION
import sys
import os
sys.path.append(os.path.dirname(__file__))

import sounddevice as sd
import vosk
import queue
import json
import threading
import time
from automation_core import AutomationCore
from working_llm_interface import WorkingLLMInterface
from memory_manager import MemoryManager
import pyttsx3

class EnhancedVoicePipeline:
    def __init__(self):
        # Initialize components
        self.automation = AutomationCore()
        self.llm = WorkingLLMInterface(r"models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf")
        self.memory = MemoryManager()
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 180)  # Faster speech
        
        # Vosk ASR setup - FIXED PATH
        # Try multiple possible model locations
        possible_paths = [
            r"models/vosk-model-small-en-us-0.15",
            r"models/vosk-model",
            r"../models/vosk-model-small-en-us-0.15",
            r"../models/vosk-model"
        ]
        
        self.model = None
        for model_path in possible_paths:
            full_path = os.path.abspath(model_path)
            print(f"🔍 Trying Vosk model path: {full_path}")
            if os.path.exists(full_path):
                try:
                    self.model = vosk.Model(full_path)
                    print(f"✅ Vosk model loaded from: {model_path}")
                    break
                except Exception as e:
                    print(f"❌ Failed to load from {model_path}: {e}")
        
        if not self.model:
            print("❌ No Vosk model found! Using interactive mode instead.")
            self.use_voice = False
        else:
            self.use_voice = True
        
        self.sample_rate = 16000
        self.audio_queue = queue.Queue()
        
        self.listening_for_command = False
        self.last_wake_word_time = 0
        self.wake_word_timeout = 10  # seconds
        
        print("🎤 ENHANCED VOICE PIPELINE INITIALIZED!")
        if self.use_voice:
            print("🔊 Say 'COMPUTER' clearly to activate")
            print("💬 Then speak your command within 10 seconds")
        else:
            print("🔊 VOICE MODE: DISABLED (no Vosk model)")
            print("💬 Using interactive text input instead")
        print("⚡ Automation commands execute instantly")
        print("🤖 Conversational queries use fast LLM mode")
    
    def speak(self, text, wait=True):
        """Speak text with TTS"""
        # Clean up text for better TTS
        clean_text = text.split('###')[0].split('User:')[0].strip()
        if len(clean_text) > 200:  # Limit long responses
            clean_text = clean_text[:200] + "..."
            
        print(f"🔊 ASSISTANT: {clean_text}")
        self.tts.say(clean_text)
        if wait:
            self.tts.runAndWait()
    
    def audio_callback(self, indata, frames, time, status):
        """Audio input callback"""
        self.audio_queue.put(bytes(indata))
    
    def is_wake_word(self, text):
        """Enhanced wake word detection"""
        text_lower = text.lower().strip()
        wake_words = ['computer', 'assistant', 'hey device', 'okay computer', 'hello computer']
        return any(word in text_lower for word in wake_words)
    
    def should_process_command(self, text):
        """Check if we should process this as a command"""
        if not self.listening_for_command:
            return False
        
        # Check if wake word timeout
        if time.time() - self.last_wake_word_time > self.wake_word_timeout:
            self.listening_for_command = False
            return False
            
        return True
    
    def process_command(self, text):
        """Process command text (from voice or keyboard)"""
        text = text.strip()
        if not text or len(text) < 2:
            return False
        
        print(f"🎤 COMMAND: '{text}'")
        
        # Check for wake words
        if self.is_wake_word(text):
            self.listening_for_command = True
            self.last_wake_word_time = time.time()
            self.speak("Yes, I'm listening. Speak your command.")
            return True
        
        # If we're in command mode, process the command
        if self.should_process_command(text) or not self.use_voice:
            if self.use_voice:
                self.listening_for_command = False  # Reset for next command
            
            # Store in memory
            self.memory.store_memory(text, "voice_command")
            
            # Check for automation commands (FAST PATH)
            matched_command = self.automation.match_command(text)
            if matched_command:
                command_name = matched_command['phrases'][0]
                self.speak(f"Okay, {command_name}")
                
                # Execute command immediately
                result = self.automation.execute_action(matched_command)
                
                if result:
                    self.speak("Done!")
                else:
                    self.speak("Sorry, command failed")
                    
                self.memory.store_memory(str(result), "command_result")
                return True
            else:
                # Use FAST LLM for conversational response (limited tokens)
                self.speak("Thinking...")
                try:
                    # Use shorter response for faster feedback
                    response = self.llm.query(text, max_tokens=60)
                    self.speak(response)
                    self.memory.store_memory(response, "llm_response")
                    return True
                except Exception as e:
                    self.speak("Sorry, I'm having trouble thinking right now")
                    print(f"LLM Error: {e}")
                    return False
        
        return False
    
    def start_voice_listening(self):
        """Start the enhanced voice listening loop"""
        print("🎧 Starting enhanced voice listener...")
        
        try:
            with sd.RawInputStream(samplerate=self.sample_rate, blocksize=8000,
                                 dtype='int16', channels=1, callback=self.audio_callback):
                
                recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)
                
                print("✅ Enhanced voice listener active!")
                self.speak("Enhanced voice assistant ready")
                
                while True:
                    data = self.audio_queue.get()
                    
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        text = result.get('text', '').strip()
                        if text:
                            self.process_command(text)
                            
        except Exception as e:
            print(f"❌ Audio error: {e}")
            self.speak("Audio system error")
    
    def start_interactive_mode(self):
        """Start interactive text input mode"""
        print("\n" + "="*60)
        print("🎤 ENHANCED VOICE ASSISTANT - INTERACTIVE MODE")
        print("="*60)
        print("Type commands as if you're speaking them:")
        print("Examples: 'computer' (wake word), then 'open browser'")
        print("Or direct commands: 'open browser', 'system info'")
        print("Type 'quit' to exit")
        print("-"*60)
        
        self.speak("Interactive mode activated")
        
        while True:
            try:
                user_input = input("\n🎤 YOU: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'stop']:
                    self.speak("Goodbye!")
                    break
                
                if user_input:
                    self.process_command(user_input)
                    
            except KeyboardInterrupt:
                self.speak("Assistant shutting down")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def start(self):
        """Start the enhanced voice pipeline"""
        print("🚀 STARTING ENHANCED VOICE ASSISTANT...")
        
        if self.use_voice:
            self.start_voice_listening()
        else:
            self.start_interactive_mode()

if __name__ == "__main__":
    pipeline = EnhancedVoicePipeline()
    pipeline.start()