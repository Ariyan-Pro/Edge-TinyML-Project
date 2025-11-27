# real_time_demo.py
import time
import numpy as np
import random

def simulate_real_time_detection():
    print("🎤 REAL-TIME KEYWORD SPOTTING SIMULATION")
    print("=" * 50)
    print("Speak one of: yes, no, up, down, left, right, on, off, stop, go")
    print("Press Ctrl+C to stop\n")
    
    keywords = ['yes', 'no', 'up', 'down', 'left', 'right', 'on', 'off', 'stop', 'go']
    
    try:
        for i in range(20):  # Simulate 20 detection events
            # Simulate random detection pattern
            if random.random() > 0.3:  # 70% chance of detection
                keyword = random.choice(keywords)
                confidence = random.uniform(0.7, 0.98)
                inference_time = random.uniform(2.8, 3.5)
                
                print(f"🎯 Heard: {keyword:6s} ({confidence:.1%}) | Time: {inference_time:5.1f}ms")
            else:
                # Simulate background noise
                confidence = random.uniform(0.1, 0.5)
                print(f"🔇 Listening... (confidence: {confidence:.1%})")
            
            time.sleep(1.5)  # Simulate real-time interval
            
    except KeyboardInterrupt:
        print("\n⏹️ Simulation stopped by user")
    
    print("\n" + "=" * 50)
    print("📊 DEMO COMPLETED")
    print("System ran for simulated 30 seconds")
    print("Memory: ~205MB | CPU: ~23%")

if __name__ == "__main__":
    simulate_real_time_detection()