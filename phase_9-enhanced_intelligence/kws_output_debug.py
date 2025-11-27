# kws_output_debug.py
from hybrid_model_router_optimized import Phase9EnhancedIntelligence
import numpy as np

def debug_kws_outputs():
    """Debug the exact KWS model outputs"""
    print("🔍 DEBUGGING KWS MODEL OUTPUTS...")
    
    hybrid = Phase9EnhancedIntelligence()
    
    # Test with different audio inputs
    test_cases = [
        ("Silence", np.random.normal(0, 0.001, 16000).astype(np.float32)),
        ("Loud noise", np.random.normal(0, 0.1, 16000).astype(np.float32)),
        ("Actual speech simulation", np.sin(2 * np.pi * 440 * np.arange(16000) / 16000).astype(np.float32))
    ]
    
    for name, audio in test_cases:
        print(f"\n🧪 TEST CASE: {name}")
        result = hybrid.process_audio_intelligently(audio)
        
        # Check wakeword results
        wakeword_result = result.get('wakeword', {})
        print(f"📊 Wakeword Result: {wakeword_result}")
        
        # Check hybrid prediction
        hybrid_pred = result.get('hybrid_prediction', {})
        print(f"🎯 Hybrid Prediction: {hybrid_pred}")
        
        # Check if we can access the raw KWS model
        if hasattr(hybrid, 'wakeword_model'):
            print(f"🔧 Wakeword Model: {type(hybrid.wakeword_model)}")
        
        # Check emotion results for comparison
        emotion_result = result.get('emotion', {})
        print(f"🎭 Emotion Result: {emotion_result}")

def check_hybrid_router_internals():
    """Check the internal structure of the hybrid router"""
    print("\n🔧 CHECKING HYBRID ROUTER INTERNALS...")
    
    hybrid = Phase9EnhancedIntelligence()
    
    # Check available attributes
    print("📋 Available attributes in hybrid router:")
    for attr in dir(hybrid):
        if not attr.startswith('_'):  # Skip private attributes
            try:
                value = getattr(hybrid, attr)
                if callable(value):
                    print(f"   🏗️  {attr}: {type(value).__name__}")
                else:
                    print(f"   📦 {attr}: {type(value).__name__} = {value}")
            except:
                print(f"   ❌ {attr}: [Unable to access]")

if __name__ == "__main__":
    debug_kws_outputs()
    check_hybrid_router_internals()
    check_hybrid_router_internals()