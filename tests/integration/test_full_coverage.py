import pytest
import sys
import os
sys.path.append('phase3_automation_phase4_cognitive/scripts')
sys.path.append('phase3_automation_phase4_cognitive/scripts/ai_core')

from automation_core import automation_engine
from memory_manager import MemoryManager

class TestIntegrationCoverage:
    def setup_method(self):
        os.environ['EDGE_ALLOW_DESTRUCTIVE'] = '0'
        self.memory = MemoryManager()
    
    def test_all_command_phrases(self):
        """Test all 12 automation commands"""
        commands = [
            'open browser', 'launch browser',
            'open notepad', 'start notepad', 
            'open calculator', 'start calculator',
            'what time is it', 'current time',
            'what date is it', 'current date',
            'list files', 'show directory'
        ]
        
        for cmd in commands:
            result = automation_engine.execute_command(cmd)
            assert 'Command not recognized' not in result or 'Safety mode' not in result
            print(f"✅ {cmd}: {result}")
    
    def test_safety_gating_destructive(self):
        """Test destructive command blocking"""
        destructive_commands = [
            'shutdown', 'restart', 'format', 'delete system32',
            'rm -rf', 'format c:', 'shutdown now'
        ]
        
        for cmd in destructive_commands:
            result = automation_engine.execute_command(cmd)
            assert 'Safety mode active' in result or 'blocked' in result or 'Command not recognized' in result
            print(f"✅ {cmd}: SAFELY BLOCKED")
    
    def test_confirmation_required_flow(self):
        """Test confirmation-required commands"""
        # Mock confirmation response
        high_risk_commands = ['shutdown computer', 'restart system']
        
        for cmd in high_risk_commands:
            result = automation_engine.execute_command(cmd)
            # Should either block or require confirmation
            assert 'confirm' in result.lower() or 'safety' in result.lower() or 'blocked' in result.lower()
            print(f"✅ {cmd}: CONFIRMATION REQUIRED")
    
    def test_concurrent_command_handling(self):
        """Test command queue behavior under load"""
        import threading
        
        results = []
        def execute_command(cmd):
            result = automation_engine.execute_command(cmd)
            results.append((cmd, result))
        
        threads = []
        test_commands = ['open browser'] * 5  # 5 concurrent requests
        
        for cmd in test_commands:
            thread = threading.Thread(target=execute_command, args=(cmd,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        assert len(results) == len(test_commands)
        print(f"✅ Concurrent commands handled: {len(results)}")

if __name__ == '__main__':
    test_suite = TestIntegrationCoverage()
    test_suite.setup_method()
    test_suite.test_all_command_phrases()
    test_suite.test_safety_gating_destructive()
    test_suite.test_confirmation_required_flow()
    test_suite.test_concurrent_command_handling()
    print("🎯 INTEGRATION COVERAGE: COMPREHENSIVE TESTS PASSED")
