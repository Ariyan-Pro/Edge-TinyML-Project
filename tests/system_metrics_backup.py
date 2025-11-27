# tests/system_metrics.py
import psutil
import time
from prometheus_client import start_http_server, Histogram, Counter, Gauge

class MetricsExporter:
    def __init__(self, port=8000):
        self.port = port
        
        # Application metrics
        self.kws_latency = Histogram('kws_latency_ms', 'KWS inference latency', ['device'])
        self.command_count = Counter('assistant_commands_total', 'Total commands executed', ['command_id', 'status'])
        self.safety_blocks = Counter('safety_blocks_total', 'Destructive commands blocked')
        self.wakeword_detections = Counter('wakeword_detections_total', 'Wake word detections', ['keyword'])
        
        # System metrics
        self.service_uptime = Gauge('service_uptime_seconds', 'Service uptime')
        self.system_cpu = Gauge('system_cpu_percent', 'CPU utilization')
        self.system_memory = Gauge('system_memory_percent', 'Memory utilization')
        self.system_memory_mb = Gauge('system_memory_mb', 'Memory usage in MB')
        
        self.start_time = time.time()
    
    def update_system_metrics(self):
        memory = psutil.virtual_memory()
        self.system_cpu.set(psutil.cpu_percent())
        self.system_memory.set(memory.percent)
        self.system_memory_mb.set(memory.used / 1024 / 1024)
        self.service_uptime.set(time.time() - self.start_time)
    
    def record_kws_latency(self, latency_ms, device='windows'):
        self.kws_latency.labels(device=device).observe(latency_ms)
    
    def record_command_execution(self, command_id, status='success'):
        self.command_count.labels(command_id=command_id, status=status).inc()

    def record_safety_block(self):
        self.safety_blocks.inc()

    def record_wakeword_detection(self, keyword):
        self.wakeword_detections.labels(keyword=keyword).inc()

    def start_metrics_server(self):
        start_http_server(self.port)
        print(f"📈 Metrics exporter running on port {self.port}")

        def system_metrics_loop():
            while True:
                self.update_system_metrics()
                time.sleep(5)

        import threading
        threading.Thread(target=system_metrics_loop, daemon=True).start()
        return self

# Global instance
metrics_exporter = MetricsExporter()