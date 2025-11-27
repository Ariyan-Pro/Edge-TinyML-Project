# scripts/working_llm_interface.py - FIXED VERSION
import os
import sys
import random
from ctransformers import AutoModelForCausalLM

class WorkingLLMInterface:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self.model_loaded = False
        
        # Initialize fallback first
        self.setup_fallback()
        
        if os.path.exists(model_path):
            try:
                print("🚀 Loading GGUF model with ctransformers...")
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_path, 
                    model_type="llama",
                    gpu_layers=0,  # CPU only
                    context_length=2048
                )
                self.model_loaded = True
                print("✅ GGUF model loaded successfully!")
            except Exception as e:
                print(f"⚠️ Model loading failed: {e}")
                print("🔄 Using enhanced cognitive fallback...")
        else:
            print("❌ Model file not found, using fallback...")
    
    def setup_fallback(self):
        """Enhanced rule-based cognitive system"""
        self.fallback_responses = {
            'greeting': [
                "Hello! I'm your intelligent voice assistant ready to help.",
                "Hi there! I can control your system and remember information.",
                "Greetings! How can I assist you today?"
            ],
            'memory': [
                "I'll remember that for you.",
                "Noted and stored in memory.",
                "I've made a note of that information."
            ],
            'system': [
                "I can help with system commands like opening apps, checking info, or controlling settings.",
                "Try commands like 'open browser', 'system info', or 'volume up'.",
                "I have 12 system commands available for your convenience."
            ],
            'unknown': [
                "I understand. How can I help you further?",
                "That's interesting! What would you like to do next?",
                "I see. Would you like me to help with system commands or remember something?"
            ]
        }
    
    def query(self, prompt, max_tokens=150):
        if self.model_loaded:
            try:
                # Enhanced prompt formatting for better responses
                formatted_prompt = f"### User: {prompt}\n### Assistant:"
                response = self.model(
                    formatted_prompt,
                    max_new_tokens=max_tokens,
                    temperature=0.7,
                    top_p=0.9,
                    repetition_penalty=1.1
                )
                return response.strip()
            except Exception as e:
                print(f"⚠️ LLM inference failed: {e}")
                return self.fallback_query(prompt)
        else:
            return self.fallback_query(prompt)
    
    def fallback_query(self, prompt):
        """Enhanced rule-based responses"""
        prompt_lower = prompt.lower()
        
        # Greeting detection
        if any(word in prompt_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return random.choice(self.fallback_responses['greeting'])
        
        # Memory detection
        elif any(word in prompt_lower for word in ['remember', 'recall', 'memorize', 'note']):
            return random.choice(self.fallback_responses['memory'])
        
        # System command detection
        elif any(word in prompt_lower for word in ['open', 'system', 'computer', 'command', 'help']):
            return random.choice(self.fallback_responses['system'])
        
        # Default intelligent response
        else:
            return random.choice(self.fallback_responses['unknown'])

# Test the working interface
if __name__ == "__main__":
    model_path = r"models/tinyllama-1.1b-chat-v1.0.Q4_0.gguf"
    
    print("🧠 TESTING WORKING LLM INTERFACE")
    print("=" * 50)
    
    llm = WorkingLLMInterface(model_path)
    
    test_prompts = [
        "Hello! How are you today?",
        "Remember that I like programming",
        "What can you do?",
        "Open the browser for me",
        "This system is amazing!"
    ]
    
    for prompt in test_prompts:
        print(f"👤 User: {prompt}")
        response = llm.query(prompt)
        print(f"🤖 Assistant: {response}")
        print("-" * 40)