"""
Weather Tool Plugin
Provides weather information for locations
"""

__description__ = "Get current weather information for any location"
__safety_level__ = "safe"
__version__ = "1.0"
__author__ = "System"

import requests
import json

class WeatherTool:
    def __init__(self):
        self.base_url = "http://api.weatherapi.com/v1"
        # Note: In production, you'd use a real API key
        self.api_key = "demo_key"
    
    def get_weather(self, location: str) -> dict:
        """Get current weather for a location"""
        try:
            # Simulated weather data for demo
            weather_data = {
                "location": location,
                "temperature": 22,
                "condition": "Sunny",
                "humidity": 65,
                "wind_speed": 15,
                "forecast": "Clear skies throughout the day"
            }
            return {"success": True, "data": weather_data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_forecast(self, location: str, days: int = 3) -> dict:
        """Get weather forecast"""
        forecast = {
            "location": location,
            "days": [
                {"day": "Today", "high": 24, "low": 18, "condition": "Sunny"},
                {"day": "Tomorrow", "high": 23, "low": 17, "condition": "Partly Cloudy"},
                {"day": "Day after", "high": 21, "low": 16, "condition": "Rainy"}
            ]
        }
        return {"success": True, "data": forecast}

# Plugin interface function
def execute(command: str, parameters: dict) -> dict:
    """Main plugin execution function"""
    tool = WeatherTool()
    
    if command == "get_weather":
        return tool.get_weather(parameters.get("location", "Unknown"))
    elif command == "get_forecast":
        return tool.get_forecast(parameters.get("location", "Unknown"), parameters.get("days", 3))
    else:
        return {"success": False, "error": f"Unknown command: {command}"}
