import requests
import json
import subprocess
from pathlib import Path

class TermuxClient:
    """Termux API Client for Android automation"""
    
    def __init__(self, adb_controller=None):
        self.adb = adb_controller
        self.termux_api_url = "http://localhost:8080"
        
    def execute_termux_command(self, command, wait_for_completion=True):
        """Execute command via Termux"""
        if not self.adb or not self.adb.is_connected:
            return {"success": False, "error": "No ADB connection"}
        
        # Execute via ADB shell
        adb_command = f"shell am start -a com.termux.service_execute -e command '{command}'"
        result = self.adb.send_command(adb_command)
        
        if wait_for_completion:
            time.sleep(2)  # Wait for command execution
            
        return result
    
    def send_sms(self, phone_number, message):
        """Send SMS via Termux"""
        command = f'termux-sms-send -n {phone_number} "{message}"'
        return self.execute_termux_command(command)
    
    def make_call(self, phone_number):
        """Make phone call"""
        command = f"termux-telephony-call {phone_number}"
        return self.execute_termux_command(command)
    
    def get_location(self):
        """Get device location"""
        command = "termux-location"
        return self.execute_termux_command(command)
    
    def vibrate_device(self, duration_ms=1000):
        """Vibrate device"""
        command = f"termux-vibrate -d {duration_ms}"
        return self.execute_termux_command(command)
    
    def torch_toggle(self, enable=True):
        """Toggle flashlight/torch"""
        command = "termux-torch on" if enable else "termux-torch off"
        return self.execute_termux_command(command)
    
    def share_file(self, file_path, share_with=None):
        """Share file from device"""
        command = f"termux-share {file_path}"
        if share_with:
            command += f" -a {share_with}"
        return self.execute_termux_command(command)
    
    def clipboard_get(self):
        """Get clipboard content"""
        command = "termux-clipboard-get"
        return self.execute_termux_command(command)
    
    def clipboard_set(self, text):
        """Set clipboard content"""
        command = f'termux-clipboard-set "{text}"'
        return self.execute_termux_command(command)
    
    def battery_status(self):
        """Get battery status"""
        command = "termux-battery-status"
        return self.execute_termux_command(command)
    
    def sensor_data(self):
        """Get sensor data"""
        command = "termux-sensor -l"
        return self.execute_termux_command(command)
    
    def notification(self, title, content, sound=True):
        """Send notification"""
        sound_flag = "" if sound else "--ongoing --alert-once"
        command = f'termux-notification --title "{title}" --content "{content}" {sound_flag}'
        return self.execute_termux_command(command)

# Test Termux client
if __name__ == "__main__":
    print("📱 TERMUX CLIENT TEST")
    print("=" * 40)
    
    # This requires ADB connection first
    from adb_controller import ADBController
    
    adb = ADBController()
    termux = TermuxClient(adb)
    
    if adb.check_adb_available() and adb.connect_device():
        print("✅ ADB connected - Termux ready")
        print("Available Termux commands:")
        print("  • send_sms(phone, message)")
        print("  • make_call(phone)")
        print("  • get_location()")
        print("  • vibrate_device()")
        print("  • torch_toggle()")
        print("  • battery_status()")
        print("  • notification(title, content)")
    else:
        print("❌ ADB not available - Termux requires Android connection")
