# scripts/llm/cognitive_engine.py (Unified LLM interface)
import os
from ctransformers import AutoModelForCausalLM

class CognitiveEngine:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load GGUF model with fallback"""
        if os.path.exists(self.model_path):
            try:
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_path, 
                    model_type="llama",
                    gpu_layers=0,
                    context_length=1024
                )
                print("✅ Cognitive Engine: GGUF model loaded")
            except Exception as e:
                print(f"⚠️ Cognitive Engine: {e}")
        else:
            print("❌ Cognitive Engine: Model file missing")
    
    def process_query(self, user_input, context=None):
        """Process user input with intelligence"""
        if self.model:
            # Use GGUF model for advanced reasoning
            prompt = self._format_prompt(user_input, context)
            response = self.model(
                prompt,
                max_new_tokens=80,
                temperature=0.3,
                top_p=0.7
            )
            return response.strip()
        else:
            # Fallback to rule-based responses
            return self._rule_based_response(user_input)
    
    def _format_prompt(self, user_input, context):
        """Format prompt for better responses"""
        base_prompt = f"User: {user_input}\nAssistant:"
        if context:
            base_prompt = f"Context: {context}\n{base_prompt}"
        return base_prompt
    
    def _rule_based_response(self, user_input):
        """Intelligent fallback responses"""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm your intelligent assistant."
        elif any(word in input_lower for word in ['remember', 'note']):
            return "I'll remember that for you."
        elif any(word in input_lower for word in ['open', 'start']):
            return "I can open applications like browser, notepad, or calculator."
        else:
            return "I understand. How can I assist you?"