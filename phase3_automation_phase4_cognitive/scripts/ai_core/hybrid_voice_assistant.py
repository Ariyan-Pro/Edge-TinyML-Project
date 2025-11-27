# scripts/hybrid_voice_assistant.py
import sys
import os
sys.path.append(os.path.dirname(__file__))

from automation_core import AutomationCore
from memory_manager import MemoryManager
from working_llm_interface import WorkingLLMInterface
import pyttsx3
import speech_recognition as sr
import time
import random

class HybridVoiceAssistant:
    def __init__(self):
        self.automation = AutomationCore()
        self.memory = MemoryManager()
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 160)
        
        # Initialize GGUF model OPTIONALLY (won't block startup)
        self.llm = None
        self.llm_available = False
        self.setup_llm_optionally()
        
        # High-quality speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Calibrate microphone
        print("🔧 Calibrating microphone...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("✅ Microphone calibrated!")
        
        # User preferences
        self.always_speak_results = False
        self.use_llm_for_cognitive = False  # Default to fast mode
        
        print("\n" + "="*70)
        print("🎤 HYBRID VOICE ASSISTANT - FAST + OPTIONAL LLM")
        print("="*70)
        print("⚡ DEFAULT: Instant rule-based responses")
        print("🧠 OPTIONAL: GGUF AI when you want it") 
        print("🔊 HIGH-QUALITY SPEECH RECOGNITION: ACTIVE")
        print("💬 OPTIONAL VOICE FEEDBACK: CONFIGURABLE")
        print("⚡ 12 INSTANT AUTOMATION COMMANDS")
        print("-"*70)
        
        self.setup_user_preferences()
    
    def setup_llm_optionally(self):
        """Setup GGUF model in background without blocking"""
        print("🔄 Setting up GGUF model optionally...")
        try:
            # Try to load GGUF but don't block if it fails
            self.llm = WorkingLLMInterface(r"models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf")
            self.llm_available = True
            print("✅ GGUF MODEL: AVAILABLE (use 'ai mode' to activate)")
        except Exception as e:
            print(f"❌ GGUF MODEL: Not available - {e}")
            self.llm_available = False
    
    def setup_user_preferences(self):
        """Setup user preferences"""
        print("\n🎯 VOICE FEEDBACK SETUP")
        print("Should I always speak results aloud?")
        print("1. YES - Always speak results (hands-free)")
        print("2. NO - Ask before speaking each time")
        print("3. ONLY ERRORS - Speak only when commands fail")
        
        choice = input("Choose (1/2/3): ").strip()
        
        if choice == "1":
            self.always_speak_results = True
            self.speak("I will always speak results aloud")
        elif choice == "2":
            self.always_speak_results = False
            self.speak("I will ask before speaking results")
        else:
            self.always_speak_results = "errors_only"
            self.speak("I will speak only for errors and confirmations")
        
        # Ask about AI mode
        print("\n🎯 AI MODE SETUP")
        print("Use GGUF AI for cognitive responses?")
        print("1. FAST MODE - Instant rule-based responses (recommended)")
        print("2. AI MODE - Use GGUF AI (slower but more intelligent)")
        
        ai_choice = input("Choose (1/2): ").strip()
        self.use_llm_for_cognitive = (ai_choice == "2")
        
        if self.use_llm_for_cognitive and self.llm_available:
            self.speak("AI mode activated. Using GGUF for intelligent responses.")
        else:
            self.speak("Fast mode activated. Using instant rule-based responses.")
    
    def speak(self, text, force_speak=False):
        """Speak text with TTS based on user preferences"""
        print(f"🔊 {text}")
        
        should_speak = force_speak or (
            self.always_speak_results == True or
            (self.always_speak_results == "errors_only" and "error" in text.lower()) or
            (self.always_speak_results == "errors_only" and "sorry" in text.lower()) or
            (self.always_speak_results == "errors_only" and "failed" in text.lower())
        )
        
        if should_speak:
            self.tts.say(text)
            self.tts.runAndWait()
        else:
            print("   [Voice feedback skipped based on preferences]")
    
    def ask_to_speak(self, prompt):
        """Ask user if they want to hear the response"""
        if self.always_speak_results == True:
            return True
        elif self.always_speak_results == "errors_only":
            return False
        
        print(f"\n💬 {prompt}")
        print("Should I speak this aloud? (y/n)")
        
        choice = input("Type 'y' to hear or 'n' to skip: ").strip().lower()
        return choice in ['y', 'yes']
    
    def listen_for_speech(self):
        """Listen for speech with high-quality recognition"""
        try:
            print("🎤 LISTENING... Speak your command!")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=5)
            
            print("🔄 Processing speech...")
            text = self.recognizer.recognize_google(audio)
            print(f"🎤 RECOGNIZED: '{text}'")
            return text.lower().strip()
            
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            self.speak("Sorry, I didn't understand that", force_speak=True)
            return None
        except sr.WaitTimeoutError:
            print("⏰ Listening timeout")
            return None
        except Exception as e:
            print(f"❌ Listening error: {e}")
            self.speak("Speech recognition error", force_speak=True)
            return None
    
    def process_with_fast_cognitive(self, user_input):
        """INSTANT rule-based cognitive responses"""
        user_input_lower = user_input.lower()
        
        # Mode switching commands
        if any(word in user_input_lower for word in ['ai mode', 'use ai', 'llm mode']):
            if self.llm_available:
                self.use_llm_for_cognitive = True
                return "AI mode activated! I'll use GGUF for intelligent responses."
            else:
                return "AI mode not available. GGUF model failed to load."
        
        if any(word in user_input_lower for word in ['fast mode', 'instant mode', 'rule mode']):
            self.use_llm_for_cognitive = False
            return "Fast mode activated! Using instant rule-based responses."
        
        # Greetings and basic conversation
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            responses = [
                "Hello! I'm your hybrid voice assistant.",
                "Hi there! Ready to help with commands.",
                "Greetings! How can I assist you?"
            ]
            return random.choice(responses)
        
        # Questions about capabilities
        elif any(word in user_input_lower for word in ['what can you', 'capabilities', 'how do you']):
            mode_info = " (AI Mode)" if self.use_llm_for_cognitive else " (Fast Mode)"
            return f"I can execute 12 automation commands: open apps, system control, volume, screenshots.{mode_info} Try 'open browser' or 'system info'."
        
        # Thanks and appreciation
        elif any(word in user_input_lower for word in ['thank', 'thanks', 'appreciate']):
            responses = [
                "You're welcome! Happy to help.",
                "My pleasure! What else can I do for you?",
                "Glad I could assist! Anything else?"
            ]
            return random.choice(responses)
        
        # Command suggestions for close matches
        elif 'browser' in user_input_lower or 'chrome' in user_input_lower:
            return "I think you want to open a browser. Say 'open browser' to launch Chrome."
        
        elif 'notepad' in user_input_lower or 'note' in user_input_lower:
            return "I think you want to open a text editor. Say 'open notepad' to launch Notepad."
        
        elif 'calculator' in user_input_lower or 'calc' in user_input_lower:
            return "I think you want to open calculator. Say 'open calculator' to launch it."
        
        elif 'system' in user_input_lower or 'info' in user_input_lower:
            return "I think you want system information. Say 'system info' to see CPU, memory, and OS details."
        
        elif 'file' in user_input_lower or 'explorer' in user_input_lower:
            return "I think you want to open file explorer. Say 'open files' to browse your files."
        
        elif 'network' in user_input_lower or 'internet' in user_input_lower:
            return "I think you want network status. Say 'network status' to check connection."
        
        # Default response
        else:
            return f"I'm not sure what you meant by '{user_input}'. Try commands like 'open browser', 'system info', or 'open notepad'."
    
    def process_with_llm(self, user_input):
        """Process with GGUF model (when available and enabled)"""
        if not self.llm_available or not self.use_llm_for_cognitive:
            return self.process_with_fast_cognitive(user_input)
        
        try:
            print("🧠 Thinking with AI... (this may take a moment)")
            enhanced_prompt = f"User said: '{user_input}'. Provide a helpful, concise response in plain text."
            
            response = self.llm.query(enhanced_prompt, max_tokens=60)
            
            # Clean up response
            clean_response = response.strip()
            clean_response = clean_response.split('###')[0]
            clean_response = clean_response.split('User:')[0]
            clean_response = clean_response.split('Assistant:')[-1]
            clean_response = clean_response.strip()
            
            if not clean_response or len(clean_response) < 10:
                return self.process_with_fast_cognitive(user_input)
                
            return f"🤖 {clean_response}"
        except Exception as e:
            print(f"❌ AI Error: {e}")
            return "AI is having trouble right now. Using fast mode instead."
    
    def suggest_similar_commands(self, user_input):
        """INSTANT command suggestions"""
        user_words = user_input.lower()
        
        command_mapping = {
            'browser': 'open browser', 'chrome': 'open browser',
            'notepad': 'open notepad', 'note': 'open notepad',
            'calculator': 'open calculator', 'calc': 'open calculator',
            'files': 'open files', 'explorer': 'open files', 'file': 'open files',
            'system': 'system info', 'info': 'system info',
            'network': 'network status', 'internet': 'network status',
            'volume': 'volume up', 'mute': 'mute volume',
            'screenshot': 'take screenshot'
        }
        
        suggestions = []
        for word, command in command_mapping.items():
            if word in user_words:
                suggestions.append(command)
        
        suggestions = list(set(suggestions))
        
        if suggestions:
            suggestion_text = f"Did you mean: {', '.join(suggestions[:3])}?"
            print(f"💡 {suggestion_text}")
            
            if self.ask_to_speak(suggestion_text):
                self.speak(suggestion_text, force_speak=True)
    
    def execute_voice_command(self, command_text):
        """Execute voice command with hybrid cognitive"""
        if not command_text:
            return False
        
        print(f"🎤 PROCESSING: '{command_text}'")
        
        # Store command
        self.memory.store_memory(command_text, "voice_command")
        
        # Check for quit command
        if any(word in command_text for word in ['quit', 'exit', 'stop', 'goodbye']):
            self.speak("Goodbye! Shutting down voice assistant.", force_speak=True)
            return "quit"
        
        # Check for automation commands
        matched = self.automation.match_command(command_text)
        if matched:
            command_name = matched['phrases'][0]
            
            self.speak(f"Executing {command_name}", force_speak=True)
            
            result = self.automation.execute_action(matched)
            
            if result:
                result_msg = f"Command '{command_name}' completed successfully"
            else:
                result_msg = f"Command '{command_name}' execution failed"
            
            if self.ask_to_speak(result_msg):
                self.speak(result_msg, force_speak=True)
            else:
                print(f"   ✅ {result_msg}")
            
            self.memory.store_memory(str(result), "command_result")
            return True
        else:
            # Command not recognized - use hybrid cognitive
            self.speak("Command not recognized.", force_speak=True)
            
            # Use appropriate cognitive system
            if self.use_llm_for_cognitive and self.llm_available:
                cognitive_response = self.process_with_llm(command_text)
            else:
                cognitive_response = self.process_with_fast_cognitive(command_text)
            
            print(f"🧠 RESPONSE: {cognitive_response}")
            
            if self.ask_to_speak(cognitive_response):
                self.speak(cognitive_response, force_speak=True)
            
            self.suggest_similar_commands(command_text)
            
            self.memory.store_memory(cognitive_response, "cognitive_response")
            return "cognitive"
    
    def start_hybrid_voice(self):
        """Start the hybrid voice assistant"""
        mode_info = "AI Mode" if self.use_llm_for_cognitive else "Fast Mode"
        print(f"\n🚀 HYBRID VOICE ASSISTANT ACTIVE! - {mode_info}")
        self.speak(f"Hybrid voice assistant ready in {mode_info}. Speak your commands.", force_speak=True)
        
        while True:
            try:
                print("\n" + "="*50)
                spoken_text = self.listen_for_speech()
                
                if spoken_text:
                    result = self.execute_voice_command(spoken_text)
                    
                    if result == "quit":
                        break
                
                print("🔄 Ready for next command...")
                
            except KeyboardInterrupt:
                self.speak("Voice assistant shutting down", force_speak=True)
                break
            except Exception as e:
                print(f"❌ System error: {e}")
                self.speak("A system error occurred", force_speak=True)
    
    def show_hybrid_help(self):
        """Show hybrid help"""
        help_text = f"""
        🎤 HYBRID VOICE ASSISTANT - FAST + OPTIONAL LLM
        
        🤖 AUTOMATION COMMANDS:
          - 'open browser' 'open notepad' 'open calculator' 'open files'
          - 'system info' 'network status' 
          - 'volume up' 'volume down' 'mute volume' 'take screenshot'
          - 'shutdown computer' 'restart computer'
        
        🧠 COGNITIVE MODES:
          - FAST MODE: Instant rule-based responses
          - AI MODE: GGUF AI (when available)
          - Switch with: 'ai mode' or 'fast mode'
        
        🔊 VOICE FEEDBACK:
          - Configurable: Always speak, Ask each time, or Errors only
        
        📸 SCREENSHOTS:
          - Saved to: ./screenshots/ folder
        """
        print(help_text)

if __name__ == "__main__":
    assistant = HybridVoiceAssistant()
    assistant.show_hybrid_help()
    assistant.start_hybrid_voice()