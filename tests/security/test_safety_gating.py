import pytest
import os
import sys
sys.path.append('phase3_automation_phase4_cognitive/scripts')

class TestSafetyGating:
    def test_destructive_commands_blocked(self):
        """Ensure destructive commands are always blocked in production"""
        os.environ['EDGE_ALLOW_DESTRUCTIVE'] = '0'
        from automation_core import automation_engine
        
        destructive_patterns = [
            'shutdown', 'restart', 'reboot', 'poweroff',
            'format', 'delete', 'remove', 'erase',
            'system32', 'sys32', 'cmd.exe', 'powershell'
        ]
        
        for pattern in destructive_patterns:
            result = automation_engine.execute_command(pattern)
            assert self._is_safe_response(result), f"Unsafe response for: {pattern}"
            print(f"✅ {pattern}: SAFELY HANDLED")
    
    def test_environment_variable_enforcement(self):
        """Test EDGE_ALLOW_DESTRUCTIVE enforcement"""
        os.environ['EDGE_ALLOW_DESTRUCTIVE'] = '0'
        from automation_core import automation_engine
        
        result = automation_engine.execute_command('shutdown')
        assert 'Safety mode active' in result or 'blocked' in result
        
        # Test that even with destructive intent, system blocks
        os.environ['EDGE_ALLOW_DESTRUCTIVE'] = '0'  # Force reset
        result2 = automation_engine.execute_command('restart computer')
        assert self._is_safe_response(result2)
    
    def _is_safe_response(self, response):
        """Check if response indicates safe handling"""
        safe_indicators = [
            'Safety mode active',
            'blocked',
            'Command not recognized',
            'not understood'
        ]
        return any(indicator in response for indicator in safe_indicators)

def run_safety_regression():
    suite = TestSafetyGating()
    suite.test_destructive_commands_blocked()
    suite.test_environment_variable_enforcement()
    print("🔒 SAFETY GATING REGRESSION: ALL TESTS PASSED")

if __name__ == '__main__':
    run_safety_regression()
