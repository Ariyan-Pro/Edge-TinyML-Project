#!/usr/bin/env python3
"""
PHASE 4: ENHANCED AUTOMATION CORE
With advanced system controls
"""

import json
import subprocess
import os
import logging
import time
import pyttsx3
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
TTS_ENGINE = pyttsx3.init()
TTS_ENGINE.setProperty('rate', 150)

# Paths
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "commands_schema.json"

class AutomationCore:
    def __init__(self):
        self.commands = self.load_commands()
        print("🎯 ENHANCED AUTOMATION CORE INITIALIZED")
        print(f"📋 Loaded {len(self.commands)} commands")
    
    def load_commands(self):
        """Load command schema from JSON - handles BOM automatically"""
        try:
            # Use utf-8-sig to handle BOM if present
            with open(CONFIG_PATH, 'r', encoding='utf-8-sig') as f:
                config = json.load(f)
            return config['commands']
        except Exception as e:
            logging.error(f"Failed to load commands: {e}")
            # Try alternative encoding
            try:
                with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                return config['commands']
            except Exception as e2:
                logging.error(f"Alternative load also failed: {e2}")
                return []
    
    def match_command(self, recognized_text):
        """Match recognized text to commands"""
        recognized_text = recognized_text.lower().strip()
        
        for command in self.commands:
            for phrase in command['phrases']:
                if phrase in recognized_text:
                    logging.info(f"🎯 Matched: '{recognized_text}' -> {command['id']}")
                    return command
        
        logging.info(f"❌ No match for: '{recognized_text}'")
        return None
    
    def speak(self, text):
        """Text-to-speech with error handling"""
        try:
            TTS_ENGINE.say(text)
            TTS_ENGINE.runAndWait()
        except Exception as e:
            logging.error(f"TTS failed: {e}")
    
    def execute_action(self, command):
        """Execute the matched command action"""
        action = command['action']
        
        try:
            if action['type'] == 'shell':
                # Execute shell command
                result = subprocess.run(action['cmd'], shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    logging.info(f"✅ Executed: {action['cmd']}")
                    self.speak("Command executed successfully")
                    return True
                else:
                    logging.error(f"❌ Command failed: {result.stderr}")
                    self.speak("Command execution failed")
                    return False
            
            elif action['type'] == 'python':
                # Execute Python function
                function_name = action['function']
                if hasattr(self, function_name):
                    return getattr(self, function_name)()
                else:
                    logging.error(f"❌ Unknown Python function: {function_name}")
                    return False
            
            else:
                logging.error(f"❌ Unknown action type: {action['type']}")
                return False
                
        except Exception as e:
            logging.error(f"❌ Execution error: {e}")
            self.speak("Error executing command")
            return False
    
    def get_system_info(self):
        """Get system information"""
        try:
            import psutil
            import platform
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # System info
            system_info = f"""
System Information:
- OS: {platform.system()} {platform.release()}
- CPU Usage: {cpu_percent}%
- Memory Usage: {memory_percent}%
- Platform: {platform.platform()}
"""
            print(system_info)
            self.speak(f"CPU at {cpu_percent} percent, Memory at {memory_percent} percent")
            return True
            
        except Exception as e:
            logging.error(f"❌ System info error: {e}")
            self.speak("Could not retrieve system information")
            return False
    
    def get_network_info(self):
        """Get network information"""
        try:
            import psutil
            import socket
            
            # Network info
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Network stats
            net_io = psutil.net_io_counters()
            
            network_info = f"""
Network Information:
- Hostname: {hostname}
- Local IP: {local_ip}
- Bytes Sent: {net_io.bytes_sent}
- Bytes Received: {net_io.bytes_recv}
"""
            print(network_info)
            self.speak(f"Network active. Hostname is {hostname}")
            return True
            
        except Exception as e:
            logging.error(f"❌ Network info error: {e}")
            self.speak("Could not retrieve network information")
            return False
    
    def volume_up(self):
        """Increase system volume"""
        try:
            import pyautogui
            pyautogui.press('volumeup')
            self.speak("Volume increased")
            return True
        except Exception as e:
            logging.error(f"❌ Volume up error: {e}")
            self.speak("Could not adjust volume")
            return False
    
    def volume_down(self):
        """Decrease system volume"""
        try:
            import pyautogui
            pyautogui.press('volumedown')
            self.speak("Volume decreased")
            return True
        except Exception as e:
            logging.error(f"❌ Volume down error: {e}")
            self.speak("Could not adjust volume")
            return False
    
    def mute_volume(self):
        """Mute system volume"""
        try:
            import pyautogui
            pyautogui.press('volumemute')
            self.speak("Volume muted")
            return True
        except Exception as e:
            logging.error(f"❌ Mute error: {e}")
            self.speak("Could not mute volume")
            return False
    
    def take_screenshot(self):
        """Take a screenshot"""
        try:
            import pyautogui
            import datetime
            
            # Create screenshots directory
            screenshots_dir = Path(__file__).resolve().parent.parent / "screenshots"
            screenshots_dir.mkdir(exist_ok=True)
            
            # Take screenshot
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = screenshots_dir / f"screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            
            self.speak("Screenshot taken and saved")
            print(f"📸 Screenshot saved: {screenshot_path}")
            return True
            
        except Exception as e:
            logging.error(f"❌ Screenshot error: {e}")
            self.speak("Could not take screenshot")
            return False
    
    def process_command(self, recognized_text):
        """Main method to process recognized commands"""
        command = self.match_command(recognized_text)
        
        if not command:
            self.speak("Command not recognized")
            return False
        
        # Check if confirmation is required
        if command.get('confirm', False):
            self.speak(f"Please confirm you want to {command['phrases'][0]}. Say yes to confirm.")
            # In full system, this would wait for confirmation
            # For now, we'll auto-confirm after a brief pause
            time.sleep(2)
        
        # Execute the command
        success = self.execute_action(command)
        
        if success:
            logging.info(f"🎉 Command '{command['id']}' executed successfully")
        else:
            logging.error(f"💥 Command '{command['id']}' failed")
        
        return success

def main():
    """Test the enhanced automation core"""
    automation = AutomationCore()
    
    print("🚀 ENHANCED AUTOMATION CORE TEST")
    print("💡 Type commands to test (or 'quit' to exit)")
    print("📋 Available commands:")
    
    for cmd in automation.commands:
        print(f"   - {cmd['phrases'][0]} -> {cmd['id']}")
    
    while True:
        try:
            user_input = input("\n🎤 Enter command: ").strip()
            
            if user_input.lower() == 'quit':
                break
            
            automation.process_command(user_input)
            
        except KeyboardInterrupt:
            print("\n🛑 Test interrupted")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
