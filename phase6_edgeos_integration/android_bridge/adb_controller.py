import subprocess
import json
import time
from pathlib import Path

class ADBController:
    """ADB Controller for Android device integration"""
    
    def __init__(self, adb_path="adb"):
        self.adb_path = adb_path
        self.connected_devices = []
        self.is_connected = False
        
    def check_adb_available(self):
        """Check if ADB is available"""
        try:
            result = subprocess.run([self.adb_path, "version"], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except:
            return False
    
    def connect_device(self, device_ip=None, port=5555):
        """Connect to Android device"""
        try:
            if device_ip:
                # Connect via network
                cmd = [self.adb_path, "connect", f"{device_ip}:{port}"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if "connected" in result.stdout:
                    self.is_connected = True
                    return True
            else:
                # Check for USB devices
                cmd = [self.adb_path, "devices"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                devices = [line.split('\\t')[0] for line in result.stdout.split('\\n') 
                          if line and 'device' in line and not line.startswith('List')]
                
                if devices:
                    self.connected_devices = devices
                    self.is_connected = True
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ ADB connection error: {e}")
            return False
    
    def send_command(self, command, device_id=None):
        """Send ADB command to device"""
        if not self.is_connected:
            print("⚠️  No devices connected")
            return None
            
        try:
            target_device = device_id or self.connected_devices[0] if self.connected_devices else ""
            device_param = ["-s", target_device] if target_device else []
            
            cmd = [self.adb_path] + device_param + command.split()
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def launch_app(self, package_name, device_id=None):
        """Launch Android app"""
        return self.send_command(f"shell am start -n {package_name}", device_id)
    
    def take_screenshot(self, filename="screenshot.png", device_id=None):
        """Take screenshot on Android device"""
        temp_path = f"/sdcard/{filename}"
        result = self.send_command(f"shell screencap -p {temp_path}", device_id)
        
        if result["success"]:
            # Pull screenshot to computer
            self.send_command(f"pull {temp_path} .", device_id)
            # Remove from device
            self.send_command(f"shell rm {temp_path}", device_id)
            
        return result
    
    def send_keyevent(self, key_code, device_id=None):
        """Send key event to Android device"""
        return self.send_command(f"shell input keyevent {key_code}", device_id)
    
    def get_device_info(self, device_id=None):
        """Get detailed device information"""
        info_commands = {
            "model": "shell getprop ro.product.model",
            "android_version": "shell getprop ro.build.version.release", 
            "battery": "shell dumpsys battery",
            "storage": "shell df -h",
            "memory": "shell cat /proc/meminfo"
        }
        
        device_info = {}
        for key, cmd in info_commands.items():
            result = self.send_command(cmd, device_id)
            if result["success"]:
                device_info[key] = result["output"]
        
        return device_info
    
    def install_apk(self, apk_path, device_id=None):
        """Install APK on device"""
        return self.send_command(f"install {apk_path}", device_id)

# Test the ADB controller
if __name__ == "__main__":
    print("📱 ADB CONTROLLER TEST")
    print("=" * 40)
    
    adb = ADBController()
    
    if adb.check_adb_available():
        print("✅ ADB is available")
        
        # Try to connect
        if adb.connect_device():
            print(f"✅ Connected to devices: {adb.connected_devices}")
            
            # Test device info
            if adb.connected_devices:
                info = adb.get_device_info()
                print(f"📊 Device Info: {len(info)} parameters retrieved")
        else:
            print("❌ No devices connected")
            print("💡 Connect Android device via USB or WiFi ADB")
    else:
        print("❌ ADB not found in PATH")
        print("💡 Install Android Platform Tools and add to PATH")
