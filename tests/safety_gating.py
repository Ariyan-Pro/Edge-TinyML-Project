import time

class SafetyGatingSystem:
    def __init__(self):
        self.destructive_commands = {
            "shutdown", "restart", "reboot", "poweroff",
            "format", "delete", "remove", "erase",
            "system32", "sys32", "cmd.exe", "powershell",  # FIXED: system_32 -> system32
            "kill process", "stop service", "bypass safety",
            "disable safety mode", "rm -rf", "del *.*",
            "taskkill", "net stop", "sc delete"
        }
        self.blocked_commands = []
    
    def validate_command(self, command):
        command_lower = command.lower()
        
        for destructive_cmd in self.destructive_commands:
            if destructive_cmd in command_lower:
                self.blocked_commands.append({
                    "command": command,
                    "timestamp": time.time(),
                    "reason": "safety_mode_active"
                })
                return False, "Safety mode active - command blocked"
        
        return True, "Command allowed"
    
    def get_recent_blocks(self):
        return self.blocked_commands[-10:]
