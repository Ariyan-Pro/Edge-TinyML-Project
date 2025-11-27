import os
import subprocess
import webbrowser

class AutomationCore:
    def __init__(self):
        self.commands = {
            'open browser': self.open_browser,
            'launch chrome': self.open_browser,
            'open notepad': self.open_notepad,
            'open calculator': self.open_calculator,
            'open file explorer': self.open_explorer,
            'shutdown': self.system_shutdown,
            'restart': self.system_restart
        }
    
    def open_browser(self):
        webbrowser.open('https://google.com')
        return 'Opening browser'
    
    def open_notepad(self):
        subprocess.Popen('notepad.exe')
        return 'Opening Notepad'
    
    def open_calculator(self):
        subprocess.Popen('calc.exe')
        return 'Opening Calculator'
    
    def open_explorer(self):
        subprocess.Popen('explorer.exe')
        return 'Opening File Explorer'
    
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
