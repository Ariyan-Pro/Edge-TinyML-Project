# scripts/core/automation_engine.py (Enhanced version)
import os
import sqlite3
import psutil
import pyautogui
from datetime import datetime

class AutomationEngine:
    def __init__(self):
        self.commands = self.load_commands()
        self.setup_database()
    
    def load_commands(self):
        """12 proven system commands"""
        return {
            'open browser': {'action': 'start chrome', 'type': 'system'},
            'open notepad': {'action': 'notepad.exe', 'type': 'system'},
            'open calculator': {'action': 'calc.exe', 'type': 'system'},
            'open files': {'action': 'explorer .', 'type': 'system'},
            'system info': {'action': 'self.system_info', 'type': 'function'},
            'network status': {'action': 'self.network_status', 'type': 'function'},
            'volume up': {'action': 'self.volume_up', 'type': 'function'},
            'volume down': {'action': 'self.volume_down', 'type': 'function'},
            'mute volume': {'action': 'self.volume_mute', 'type': 'function'},
            'take screenshot': {'action': 'self.take_screenshot', 'type': 'function'},
            'shutdown computer': {'action': 'shutdown /s /t 30', 'type': 'system'},
            'restart computer': {'action': 'shutdown /r /t 30', 'type': 'system'}
        }
    
    def setup_database(self):
        """Initialize memory database"""
        os.makedirs('../db', exist_ok=True)
        self.conn = sqlite3.connect('../db/cognitive_memory.db')
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS command_history 
            (id INTEGER PRIMARY KEY, command TEXT, result TEXT, timestamp TEXT)
        ''')
        self.conn.commit()
    
    def execute_command(self, command_text):
        """Execute command with memory logging"""
        if command_text in self.commands:
            cmd = self.commands[command_text]
            try:
                if cmd['type'] == 'system':
                    result = os.system(cmd['action'])
                else:  # function
                    result = getattr(self, cmd['action'].replace('self.', ''))()
                
                # Log to database
                self.log_command(command_text, "SUCCESS")
                return f"Executed: {command_text}"
                
            except Exception as e:
                self.log_command(command_text, f"ERROR: {e}")
                return f"Error executing {command_text}: {e}"
        return f"Unknown command: {command_text}"
    
    def system_info(self):
        return f"CPU: {psutil.cpu_percent()}% | Memory: {psutil.virtual_memory().percent}%"
    
    def log_command(self, command, result):
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO command_history (command, result, timestamp) VALUES (?, ?, ?)',
            (command, result, datetime.now().isoformat())
        )
        self.conn.commit()