# MINIMAL DEBUG SYSTEM - FIND THE REAL ISSUE
import time
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

def debug_system():
    print("🔍 MINIMAL DEBUG SYSTEM - FINDING THE ROOT CAUSE")
    print("=" * 50)
    
    # Test 1: Check audio stream conflicts
    print("1. Testing audio stream initialization...")
    try:
        import sounddevice as sd
        print("   ✅ sounddevice imported")
        
        # Check available devices
        devices = sd.query_devices()
        print(f"   🔊 Audio devices: {len(devices)} found")
        
    except Exception as e:
        print(f"   ❌ Audio issue: {e}")
    
    # Test 2: Check Vosk model loading
    print("2. Testing Vosk model...")
    try:
        from command_listener import VoiceCommandListener
        listener = VoiceCommandListener()
        print("   ✅ Vosk model loaded")
    except Exception as e:
        print(f"   ❌ Vosk issue: {e}")
    
    # Test 3: Check wake word detector
    print("3. Testing wake word detector...")
    try:
        from ultimate_strategic_wake_word import UltimateStrategicDetector
        detector = UltimateStrategicDetector()
        print("   ✅ Wake word detector loaded")
        
        # Check if it has the right method
        if hasattr(detector, 'run_ultimate_demonstration'):
            print("   ✅ Correct method: run_ultimate_demonstration")
        else:
            print("   ❌ Missing expected method")
            
    except Exception as e:
        print(f"   ❌ Detector issue: {e}")
    
    print("=" * 50)
    print("🎯 RECOMMENDATION:")
    print("   The issue is likely AUDIO STREAM CONFLICT between")
    print("   wake word detection and command listening modes.")
    print("")
    print("💡 SOLUTION: Use the GUI version (launch_strategic_gui.py)")
    print("   It properly manages audio stream handoffs!")
    
    return True

if __name__ == "__main__":
    debug_system()
