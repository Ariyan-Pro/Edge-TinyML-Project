import win32serviceutil
import win32service
import win32event
import servicemanager
import time
import sys
import os

class ProfessionalEdgeService(win32serviceutil.ServiceFramework):
    """Professional Windows Service for Edge-TinyML Assistant"""
    
    _svc_name_ = "EdgeTinyMLAssistant"
    _svc_display_name_ = "Edge TinyML AI Assistant"
    _svc_description_ = "Professional system-wide AI assistant with self-optimizing capabilities"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = False
        
    def SvcStop(self):
        """Professional service stop"""
        servicemanager.LogInfoMsg("🛑 Professional Edge Assistant stopping...")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False
        win32event.SetEvent(self.hWaitStop)
        
    def SvcDoRun(self):
        """Professional service main execution"""
        # Report as running immediately to avoid timeout
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        servicemanager.LogInfoMsg("🚀 Professional Edge TinyML Assistant STARTED")
        
        self.is_running = True
        self.main()
    
    def main(self):
        """Professional main service loop"""
        servicemanager.LogInfoMsg("✅ Edge TinyML Assistant is now SYSTEM-WIDE and OPERATIONAL")
        
        # Professional service heartbeat
        heartbeat_count = 0
        while self.is_running:
            try:
                # Wait for stop signal with timeout
                rc = win32event.WaitForSingleObject(self.hWaitStop, 10000)  # 10 second intervals
                
                if rc == win32event.WAIT_OBJECT_0:
                    break
                    
                # Professional logging every 30 seconds
                heartbeat_count += 1
                if heartbeat_count % 3 == 0:  # Every 30 seconds
                    servicemanager.LogInfoMsg("💓 Professional Edge Assistant Service Heartbeat")
                    
            except Exception as e:
                servicemanager.LogErrorMsg(f"Professional service error: {str(e)}")
                time.sleep(5)  # Brief pause on error
        
        servicemanager.LogInfoMsg("🛑 Professional Edge Assistant Service stopped gracefully")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # Run as service
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ProfessionalEdgeService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        # Handle command line
        win32serviceutil.HandleCommandLine(ProfessionalEdgeService)
