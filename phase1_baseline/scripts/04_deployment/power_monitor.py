#!/usr/bin/env python3
"""
Power consumption monitoring for Raspberry Pi
Requires: sudo apt install powertop
"""

import subprocess
import time
import csv
from datetime import datetime
import os

def run_power_measurement(duration=60, output_file="power_metrics.csv"):
    """Run power measurement using powertop"""
    
    print(f"🔋 Starting power measurement for {duration} seconds...")
    
    # Check if powertop is installed
    try:
        subprocess.run(["which", "powertop"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ powertop not installed. Install with: sudo apt install powertop")
        return
    
    metrics = []
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration:
            # Get power metrics
            timestamp = datetime.now().isoformat()
            
            # Get temperature
            temp_result = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, text=True)
            temperature = temp_result.stdout.strip().split('=')[1].replace("'C", "")
            
            # Get voltage
            volt_result = subprocess.run(["vcgencmd", "measure_volts"], capture_output=True, text=True)
            voltage = volt_result.stdout.strip().split('=')[1].replace("V", "")
            
            # Get clock speed
            clock_result = subprocess.run(["vcgencmd", "measure_clock", "arm"], capture_output=True, text=True)
            clock_speed = str(int(clock_result.stdout.split('=')[1]) // 1000000)
            
            # Get throttling status
            throttle_result = subprocess.run(["vcgencmd", "get_throttled"], capture_output=True, text=True)
            throttled = throttle_result.stdout.strip().split('=')[1]
            
            metrics.append({
                'timestamp': timestamp,
                'temperature': temperature,
                'voltage': voltage,
                'clock_speed': clock_speed,
                'throttled': throttled
            })
            
            print(f"🌡️  {timestamp} - Temp: {temperature}°C, Voltage: {voltage}V, Clock: {clock_speed}MHz")
            time.sleep(5)  # Measure every 5 seconds
            
    except KeyboardInterrupt:
        print("\n🛑 Power measurement stopped by user")
    
    # Save to CSV
    if metrics:
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=metrics[0].keys())
            writer.writeheader()
            writer.writerows(metrics)
        print(f"✅ Power metrics saved to {output_file}")
    
    return metrics

if __name__ == "__main__":
    run_power_measurement(duration=300)  # 5 minutes