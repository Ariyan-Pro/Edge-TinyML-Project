import subprocess
import json
import time
from pathlib import Path

class MockADBController:
    """Mock ADB Controller for testing without Android SDK"""
    
    def __init__(self):
        self.connected_devices = ["emulator-5554"]  # Mock device
        self.is_connected = True
        
    def check_adb_available(self):
        """Mock ADB availability check"""
        print("⚠️  Using Mock ADB Controller - No Android Platform Tools installed")
        return True
    
    def connect_device(self, device_ip=None, port=5555):
        """Mock device connection"""
        print(f"🔗 Mock: Connected to device {device_ip or 'emulator-5554'}")
        self.is_connected = True
        return True
    
    def send_command(self, command, device_id=None):
        """Mock command execution"""
        print(f"🖥️  Mock ADB Command: {command}")
        
        # Simulate different responses based on command
        if "devices" in command:
            return {
                "success": True,
                "output": "List of devices attached\nemulator-5554\tdevice",
                "error": ""
            }
        elif "getprop" in command:
            return {
                "success": True, 
                "output": "Pixel 4\nAndroid 11\n",
                "error": ""
            }
        else:
            return {
                "success": True,
                "output": "Mock command executed successfully",
                "error": ""
            }
    
    def launch_app(self, package_name, device_id=None):
        """Mock app launch"""
        print(f"📱 Mock: Launching {package_name}")
        return {"success": True, "output": f"Started: {package_name}"}
    
    def get_device_info(self, device_id=None):
        """Mock device information"""
        return {
            "model": "Pixel 4 (Mock)",
            "android_version": "11", 
            "battery": "100%",
            "storage": "64GB available",
            "memory": "4GB RAM"
        }

# Test the mock ADB controller
if __name__ == "__main__":
    print("📱 MOCK ADB CONTROLLER TEST")
    print("=" * 45)
    
    adb = MockADBController()
    
    if adb.check_adb_available():
        print("✅ Mock ADB is available")
        
        if adb.connect_device():
            print(f"✅ Connected to mock devices: {adb.connected_devices}")
            
            # Test device info
            info = adb.get_device_info()
            print(f"📊 Mock Device Info:")
            print(f"   Model: {info['model']}")
            print(f"   Android: {info['android_version']}")
            print(f"   Battery: {info['battery']}")
            
        print("\n💡 To use real ADB:")
        print("   1. Install Android Platform Tools")
        print("   2. Add to PATH or specify adb_path parameter")
        print("   3. Enable USB debugging on Android device")
