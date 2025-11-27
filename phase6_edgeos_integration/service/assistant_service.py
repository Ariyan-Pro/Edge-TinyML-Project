import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import threading
import json
import os
import sys
from pathlib import Path

class EdgeAssistantService(win32serviceutil.ServiceFramework):
    """Windows Service for Edge-TinyML Assistant"""
    
    _svc_name_ = "EdgeTinyMLAssistant"
    _svc_display_name_ = "Edge TinyML AI Assistant"
    _svc_description_ = "Provides system-wide AI assistant capabilities with self-optimizing core"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = False
        self.assistant_thread = None
        
        # Service configuration
        self.config = self.load_config()
        
    def load_config(self):
        """Load service configuration"""
        config_path = Path(__file__).parent / "startup_config.json"
        default_config = {
            "service_port": 9845,
            "voice_trigger_enabled": True,
            "android_bridge_enabled": False,
            "check_interval": 5,
            "log_level": "INFO"
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                    return {**default_config, **loaded_config}
            except:
                return default_config
        return default_config
    
    def SvcStop(self):
        """Stop the service"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False
        win32event.SetEvent(self.hWaitStop)
        
    def SvcDoRun(self):
        """Main service execution"""
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                            servicemanager.PYS_SERVICE_STARTED,
                            (self._svc_name_, ''))
        self.main()
    
    def main(self):
        """Main service logic"""
        self.is_running = True
        servicemanager.LogInfoMsg("🚀 Edge TinyML Assistant Service Started")
        
        # Service ready message
        servicemanager.LogInfoMsg("✅ Edge TinyML Assistant is now system-wide!")
        
        # Main service loop
        while self.is_running:
            try:
                # Service heartbeat (simplified for now)
                rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
                if rc == win32event.WAIT_OBJECT_0:
                    break
                    
            except Exception as e:
                servicemanager.LogErrorMsg(f"Service error: {str(e)}")
                time.sleep(10)
        
        servicemanager.LogInfoMsg("🛑 Edge TinyML Assistant Service Stopped")
    
    def get_service_status(self):
        """Get current service status"""
        return {
            "service_name": self._svc_name_,
            "is_running": self.is_running,
            "config": self.config,
            "timestamp": time.time()
        }

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # Run as service
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(EdgeAssistantService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        # Handle command line (install, start, stop, etc.)
        win32serviceutil.HandleCommandLine(EdgeAssistantService)
