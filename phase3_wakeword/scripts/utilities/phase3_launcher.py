#!/usr/bin/env python3
"""
Phase 3 Starter - Quick Launch
Use this to test individual components easily
"""

import sys
import time

def main():
    print("🚀 PHASE 3 VOICE ASSISTANT - QUICK LAUNCH")
    print("="*50)
    print("1. Test Wake Word Detection")
    print("2. Test Voice Commands") 
    print("3. Run Integrated Assistant")
    print("4. Run Full Test Suite")
    print("5. Exit")
    print("-"*50)
    
    while True:
        choice = input("Choose option (1-5): ").strip()
        
        if choice == "1":
            print("\n🎯 Launching Wake Word Detector...")
            try:
                from wake_word_detector import WakeWordDetector
                detector = WakeWordDetector()
                detector.run_demo()
            except Exception as e:
                print(f"❌ Error: {e}")
                
        elif choice == "2":
            print("\n🎯 Launching Voice Commands...")
            try:
                from command_listener import VoiceCommandSystem
                voice_system = VoiceCommandSystem()
                if hasattr(voice_system, 'recognizer'):
                    voice_system.run_demo()
                else:
                    print("❌ Voice recognition not available")
            except Exception as e:
                print(f"❌ Error: {e}")
                
        elif choice == "3":
            print("\n🎯 Launching Integrated Assistant...")
            try:
                from integrated_assistant import IntegratedAssistant
                assistant = IntegratedAssistant()
                assistant.run()
            except Exception as e:
                print(f"❌ Error: {e}")
                
        elif choice == "4":
            print("\n🎯 Running Test Suite...")
            try:
                from test_suite import main as test_main
                test_main()
            except Exception as e:
                print(f"❌ Error: {e}")
                
        elif choice == "5":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1-5.")
        
        print("\n" + "-"*50)

if __name__ == "__main__":
    main()
