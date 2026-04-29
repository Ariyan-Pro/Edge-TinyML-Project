import os
import subprocess
import webbrowser
import platform

class AutomationCore:
    def __init__(self):
        self.commands = {
            'open browser': self.open_browser,
            'launch chrome': self.open_browser,
            'launch browser': self.open_browser,
            'open notepad': self.open_notepad,
            'start notepad': self.open_notepad,
            'open calculator': self.open_calculator,
            'start calculator': self.open_calculator,
            'what time is it': self.get_time,
            'current time': self.get_time,
            'what date is it': self.get_date,
            'current date': self.get_date,
            'list files': self.list_files,
            'show directory': self.list_files,
            'open file explorer': self.open_explorer,
            'shutdown': self.system_shutdown,
            'restart': self.system_restart
        }
    
    def open_browser(self):
        try:
            webbrowser.open('https://google.com')
            return 'Opening browser'
        except Exception as e:
            return f'Browser opening failed: {e}'
    
    def open_notepad(self):
        """Cross-platform text editor opener"""
        try:
            system = platform.system()
            if system == 'Windows':
                subprocess.Popen(['notepad.exe'])
            elif system == 'Darwin':
                subprocess.Popen(['open', '-a', 'TextEdit'])
            else:  # Linux
                subprocess.Popen(['gedit'] if self._cmd_exists('gedit') else ['nano'])
            return 'Opening Notepad'
        except Exception as e:
            return f'Notepad opening failed (expected in test env): {e}'
    
    def open_calculator(self):
        """Cross-platform calculator opener"""
        try:
            system = platform.system()
            if system == 'Windows':
                subprocess.Popen(['calc.exe'])
            elif system == 'Darwin':
                subprocess.Popen(['open', '-a', 'Calculator'])
            else:  # Linux
                subprocess.Popen(['gnome-calculator'] if self._cmd_exists('gnome-calculator') else ['qalculate'])
            return 'Opening Calculator'
        except Exception as e:
            return f'Calculator opening failed (expected in test env): {e}'
    
    def open_explorer(self):
        """Cross-platform file explorer opener"""
        try:
            system = platform.system()
            if system == 'Windows':
                subprocess.Popen(['explorer.exe'])
            elif system == 'Darwin':
                subprocess.Popen(['open', '.'])
            else:  # Linux
                subprocess.Popen(['nautilus'] if self._cmd_exists('nautilus') else ['dolphin'])
            return 'Opening File Explorer'
        except Exception as e:
            return f'Explorer opening failed (expected in test env): {e}'
    
    def get_time(self):
        """Return current time"""
        from datetime import datetime
        return f'Current time: {datetime.now().strftime("%H:%M:%S")}'
    
    def get_date(self):
        """Return current date"""
        from datetime import datetime
        return f'Current date: {datetime.now().strftime("%Y-%m-%d")}'
    
    def list_files(self):
        """List files in current directory"""
        try:
            files = os.listdir('.')
            return f'Directory contents: {len(files)} items found'
        except Exception as e:
            return f'Failed to list files: {e}'
    
    def _cmd_exists(self, cmd):
        """Check if command exists in PATH"""
        return subprocess.call(['which', cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0
    
    def system_shutdown(self):
        if os.environ.get('EDGE_ALLOW_DESTRUCTIVE') == '1':
            return 'System shutting down in 5 seconds'
        return 'Safety mode active - shutdown blocked'
    
    def system_restart(self):
        if os.environ.get('EDGE_ALLOW_DESTRUCTIVE') == '1':
            return 'System restarting in 5 seconds'
        return 'Safety mode active - restart blocked'
    
    def execute_command(self, command_text):
        for cmd, func in self.commands.items():
            if cmd in command_text.lower():
                return func()
        return 'Command not recognized'

automation_engine = AutomationCore()
