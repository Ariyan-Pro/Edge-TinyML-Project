# scripts/main.py - FIXED WITH CORRECT STRUCTURE
import sys
import os

# Add the scripts directory to Python path
sys.path.append(os.path.dirname(__file__))

from automation_core import AutomationCore
from working_llm_interface import WorkingLLMInterface
from memory_manager import MemoryManager

class IntelligentVoiceAssistant:
    def __init__(self):
        self.automation = AutomationCore()
        self.llm = WorkingLLMInterface(r"models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf")
        self.memory = MemoryManager()
        print("🚀 Intelligent Voice Assistant Initialized!")
        
        # Show available commands
        print("📋 Available Commands:")
        for cmd in self.automation.commands[:3]:  # Show first 3 as sample
            print(f"   - {cmd['id']}: {cmd['phrases']}")
    
    def process_command(self, voice_input):
        """Main processing pipeline"""
        print(f"🎤 Processing: '{voice_input}'")
        
        # Store in memory
        self.memory.store_memory(voice_input, "user_command")
        
        # Check for automation commands using match_command
        matched_command = self.automation.match_command(voice_input)
        if matched_command:
            print(f"🔧 Matched automation command: {matched_command['id']}")
            # Execute the command
            result = self.automation.execute_action(matched_command)
            self.memory.store_memory(result, "command_result")
            return f"🤖 {result}"
        else:
            # Use LLM for intelligent responses
            print("🧠 Using LLM for response")
            response = self.llm.query(voice_input, max_tokens=100)
            self.memory.store_memory(response, "llm_response")
            return f"🧠 {response}"

# Test the unified system
if __name__ == "__main__":
    assistant = IntelligentVoiceAssistant()
    
    test_commands = [
        "open browser",
        "hello!",
        "system info", 
        "what can you do?",
        "open notepad"
    ]
    
    print("\n🧠 INTELLIGENT VOICE ASSISTANT TEST")
    print("=" * 50)
    
    for cmd in test_commands:
        response = assistant.process_command(cmd)
        print(f"👤: {cmd}")
        print(f"{response}\n")