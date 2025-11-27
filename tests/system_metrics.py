import psutil
import time
import json
import os
from datetime import datetime
from prometheus_client import start_http_server, Histogram, Counter, Gauge

class ProductionLogger:
    def __init__(self, log_dir="../logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.session_id = int(time.time())
        
    def _write_log(self, data):
        timestamp = int(time.time() * 1000)
        log_file = f"{self.log_dir}/edgetinyml_{datetime.now().strftime('%Y%m%d')}.log"
        
        log_entry = {
            "ts": timestamp,
            "session_id": self.session_id,
            **data
        }
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"⚠️  Log write failed: {e}")
    
    def log_system_event(self, event, details):
        log_data = {
            "component": "system",
            "event": event,
            "details": details,
            "environment": "production"
        }
        self._write_log(log_data)
    
    def log_detection_event(self, keyword, confidence, latency_ms, emotion, audio_energy):
        log_data = {
            "component": "kws",
            "event": "wakeword_detected",
            "keyword": keyword,
            "confidence": confidence,
            "latency_ms": latency_ms,
            "emotion": emotion,
            "audio_energy": audio_energy,
            "environment": "production"
        }
        self._write_log(log_data)
    
    def log_safety_event(self, command, action, reason):
        log_data = {
            "component": "safety",
            "event": f"command_{action}",
            "command": command,
            "reason": reason,
            "environment": "production"
        }
        self._write_log(log_data)

class MetricsExporter:
    def __init__(self, port=8000):
        self.port = port
        
        self.kws_latency = Histogram('kws_latency_ms', 'KWS inference latency', ['device'])
        self.command_count = Counter('assistant_commands_total', 'Total commands executed', ['command_id', 'status'])
        self.safety_blocks = Counter('safety_blocks_total', 'Destructive commands blocked')  # FIXED: ADDED THIS LINE
        self.wakeword_detections = Counter('wakeword_detections_total', 'Wake word detections', ['keyword'])
        
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
        import threading
        def system_metrics_loop():
            while True:
                self.update_system_metrics()
                time.sleep(5)
        threading.Thread(target=system_metrics_loop, daemon=True).start()
        return self

metrics_exporter = MetricsExporter()
