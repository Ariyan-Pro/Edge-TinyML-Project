# tests/production_logger.py
import json
import time
import os
from datetime import datetime

class ProductionLogger:
    def __init__(self, log_dir="logs"):
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
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    
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