import json
import logging
import time
from datetime import datetime
import os

class ProductionLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.session_id = int(datetime.now().timestamp())
        self.setup_structured_logging()
    
    def setup_structured_logging(self):
        """Configure JSON-line logging for production"""
        log_file = os.path.join(self.log_dir, f"edgetinyml_{datetime.now().strftime('%Y%m%d')}.log")
        
        # Clear existing handlers
        logging.getLogger().handlers = []
        
        # Configure JSON logging
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('%(message)s'))
        
        logger = logging.getLogger('EdgeTinyML')
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.addHandler(logging.StreamHandler())
        
        self.logger = logger
    
    def log_detection_event(self, keyword, confidence, latency_ms, emotion, energy):
        """Log KWS detection events in JSON format"""
        event = {
            "ts": int(time.time() * 1000),  # milliseconds
            "session_id": self.session_id,
            "component": "kws",
            "event": "wakeword_detected",
            "keyword": keyword,
            "confidence": round(confidence, 4),
            "latency_ms": round(latency_ms, 2),
            "emotion": emotion,
            "audio_energy": round(energy, 6),
            "environment": "production"
        }
        self.logger.info(json.dumps(event))
    
    def log_safety_event(self, command, action, reason):
        """Log safety system events"""
        event = {
            "ts": int(time.time() * 1000),
            "session_id": self.session_id,
            "component": "safety",
            "event": "command_" + action,
            "command": command,
            "reason": reason,
            "environment": "production"
        }
        self.logger.info(json.dumps(event))
    
    def log_system_event(self, event_type, details):
        """Log system-level events"""
        event = {
            "ts": int(time.time() * 1000),
            "session_id": self.session_id,
            "component": "system",
            "event": event_type,
            "details": details,
            "environment": "production"
        }
        self.logger.info(json.dumps(event))

# Initialize production logger
production_logger = ProductionLogger()

# Test logging
if __name__ == '__main__':
    production_logger.log_system_event("startup", {"version": "1.0", "status": "initialized"})
    production_logger.log_detection_event("yes", 0.996, 3.64, "neutral", 0.015)
    production_logger.log_safety_event("shutdown", "blocked", "safety_mode_active")
    print("✅ Production logging initialized")
