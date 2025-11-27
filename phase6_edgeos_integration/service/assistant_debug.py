import time
import json
from pathlib import Path

class EdgeAssistantDebug:
    """Debug version of Edge Assistant that doesn't require admin rights"""
    
    def __init__(self):
        self.is_running = False
        self.config = self.load_config()
        
    def load_config(self):
        """Load service configuration"""
        config_path = Path(__file__).parent / "startup_config.json"
        default_config = {
            "service_port": 9845,
            "voice_trigger_enabled": True,
            "android_bridge_enabled": False,
            "check_interval": 5,
            "log_level": "DEBUG"
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                    return {**default_config, **loaded_config}
            except:
                return default_config
        return default_config
    
    def start(self):
        """Start debug mode"""
        print("🚀 EDGE TINYML ASSISTANT - DEBUG MODE")
        print("=" * 50)
        print("📊 Configuration Loaded:")
        for key, value in self.config.items():
            print(f"   {key}: {value}")
        
        print("\n🎯 Service Capabilities:")
        print("   ✅ System-wide availability (when installed)")
        print("   ✅ Voice trigger integration")
        print("   ✅ Android bridge (ADB + Termux)")
        print("   ✅ Self-optimizing core integration")
        print("   ✅ Boot-time initialization")
        
        self.is_running = True
        print(f"\n🔧 Running in DEBUG MODE")
        print("💡 To run as system service: Run setup_windows_service.bat as Administrator")
        
        # Simulate service operation
        try:
            counter = 0
            while self.is_running and counter < 10:  # Run for 10 cycles
                print(f"🔄 Service heartbeat {counter + 1}/10 - Press Ctrl+C to stop")
                time.sleep(3)
                counter += 1
                
        except KeyboardInterrupt:
            print("\n🛑 Debug mode stopped by user")
        
        print("✅ Debug session completed")
        print("🎯 Next: Run as Administrator to install system service")
    
    def stop(self):
        """Stop debug mode"""
        self.is_running = False
        print("🛑 Debug mode stopped")

if __name__ == '__main__':
    assistant = EdgeAssistantDebug()
    assistant.start()
