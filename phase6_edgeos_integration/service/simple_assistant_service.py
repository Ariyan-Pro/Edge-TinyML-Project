import win32serviceutil
import win32service
import win32event
import servicemanager
import time
import sys

class SimpleEdgeAssistantService(win32serviceutil.ServiceFramework):
    """Simplified Windows Service for Edge-TinyML Assistant"""
    
    _svc_name_ = "EdgeTinyMLAssistant"
    _svc_display_name_ = "Edge TinyML AI Assistant"
    _svc_description_ = "System-wide AI assistant with self-optimizing capabilities"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = False
        
    def SvcStop(self):
        """Stop the service"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False
        win32event.SetEvent(self.hWaitStop)
        
    def SvcDoRun(self):
        """Main service execution - SIMPLIFIED"""
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                            servicemanager.PYS_SERVICE_STARTED,
                            (self._svc_name_, ''))
        
        # Immediately report as running
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        servicemanager.LogInfoMsg("🚀 Edge TinyML Assistant Service STARTED")
        
        self.is_running = True
        self.main()
    
    def main(self):
        """Simple main loop that responds quickly"""
        servicemanager.LogInfoMsg("✅ Edge TinyML Assistant is now SYSTEM-WIDE")
        
        # Simple heartbeat loop
        counter = 0
        while self.is_running:
            try:
                # Check for stop signal every 5 seconds
                rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
                
                if rc == win32event.WAIT_OBJECT_0:
                    break
                    
                # Log heartbeat occasionally
                counter += 1
                if counter % 12 == 0:  # Every minute
                    servicemanager.LogInfoMsg("💓 Edge Assistant Service Heartbeat")
                    
            except Exception as e:
                servicemanager.LogErrorMsg(f"Service error: {str(e)}")
                time.sleep(10)
        
        servicemanager.LogInfoMsg("🛑 Edge TinyML Assistant Service Stopped")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(SimpleEdgeAssistantService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(SimpleEdgeAssistantService)
