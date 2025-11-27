import requests
import json

class LinuxInferenceClient:
    def __init__(self, host='localhost', port=8080):
        self.base_url = f"http://{host}:{port}"
    
    def infer(self, audio_data):
        """Send audio to Linux microservice for 2.99ms inference"""
        response = requests.post(
            f"{self.base_url}/infer",
            json={"audio": audio_data.tolist()},
            timeout=0.1  # 100ms timeout
        )
        return response.json()