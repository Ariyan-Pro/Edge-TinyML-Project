import time
import sys
import os

# Add parent tests directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from safety_gating import SafetyGatingSystem

def test_destructive_commands():
    """Test all known destructive commands"""
    destructive_commands = [
        "shutdown", "restart", "reboot", "poweroff",
        "format", "delete", "remove", "erase",
        "system32", "sys32", "cmd.exe", "powershell",
        "kill process", "stop service", "bypass safety",
        "disable safety mode", "rm -rf", "del *.*",
        "taskkill", "net stop", "sc delete"
    ]
    
    safety_system = SafetyGatingSystem()
    blocked_count = 0
    total_commands = len(destructive_commands)

    print("🔒 TESTING DESTRUCTIVE COMMAND BLOCKING")

    for command in destructive_commands:
        is_safe, reason = safety_system.validate_command(command)

        # FIXED: When is_safe=False, command IS BLOCKED (GOOD!)
        if not is_safe:
            blocked_count += 1
            print(f"✅ BLOCKED: {command} (Reason: {reason})")
        else:
            print(f"❌ FAILED TO BLOCK: {command} (Safe: {is_safe}, Reason: {reason})")

    # Verify logging
    time.sleep(1)
    log_entries = safety_system.get_recent_blocks()

    print(f"\n📊 Safety System Results:")
    print(f"   - Commands tested: {total_commands}")
    print(f"   - Commands blocked: {blocked_count}")
    print(f"   - Security events logged: {len(log_entries)}")

    # We WANT all commands blocked (is_safe=False)
    if blocked_count == total_commands:
        print(f"✅ COMMAND INJECTION TEST PASSED")
        return True
    else:
        print(f"❌ COMMAND INJECTION TEST FAILED")
        print(f"   - Expected to block {total_commands}, but blocked {blocked_count}")
        return False
