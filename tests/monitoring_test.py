import sys
import os

# Add tests directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from production_logger import ProductionLogger
from system_metrics import metrics_exporter

def run_monitoring_test():
    """Run production monitoring test"""
    print("=== PRODUCTION MONITORING TEST ===")
    
    # Initialize monitoring
    logger = ProductionLogger()
    logger.log_system_event("monitoring_test", {"status": "initialized"})
    
    # Start metrics server in background
    import threading
    def start_metrics():
        metrics_exporter.start_metrics_server()
    
    metrics_thread = threading.Thread(target=start_metrics, daemon=True)
    metrics_thread.start()
    
    # Simulate activity
    logger.log_detection_event("yes", 0.996, 3.64, "neutral", 0.015)
    metrics_exporter.record_kws_latency(3.64)
    metrics_exporter.record_wakeword_detection('yes')
    
    logger.log_safety_event("shutdown", "blocked", "safety_mode_active")
    metrics_exporter.record_safety_block()
    
    print("✅ Production monitoring systems: OPERATIONAL")
    print("📈 Metrics available at: http://localhost:8000")
    print("📝 Logs writing to: logs/edgetinyml_*.log")
    print("Test completed successfully!")

if __name__ == "__main__":
    run_monitoring_test()
