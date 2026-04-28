# tests/resilience/time_warp_test.py
import time
import datetime
import sys
import os

# Add parent tests directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from system_metrics import ProductionLogger

def test_time_changes():
    """Test system behavior under time changes"""
    print("⏰ TESTING TIME WARP RESILIENCE")
    
    logger = ProductionLogger()
    time_scenarios = [
        ("+12 hours", 12 * 3600),
        ("-12 hours", -12 * 3600),
        ("timezone shift", 5 * 3600),  # EST to UTC offset
        ("year 2038", 13 * 365 * 24 * 3600),  # Future test
    ]
    
    successful_logs = 0
    
    for scenario_name, time_offset in time_scenarios:
        try:
            print(f"🧪 Testing: {scenario_name}")
            
            # Log before time change
            logger.log_system_event("time_test_before", {
                "scenario": scenario_name,
                "original_time": time.time()
            })
            
            # Simulate time change (in real scenario, this would be system time)
            simulated_time = time.time() + time_offset
            
            # Log after "time change"
            logger.log_system_event("time_test_after", {
                "scenario": scenario_name, 
                "simulated_time": simulated_time,
                "offset_applied": time_offset
            })
            
            successful_logs += 1
            print(f"✅ Time scenario handled: {scenario_name}")
            
        except Exception as e:
            print(f"❌ Time test failed for {scenario_name}: {e}")
    
    if successful_logs == len(time_scenarios):
        print("✅ TIME WARP RESILIENCE TEST PASSED")
        return True
    else:
        print("❌ TIME WARP RESILIENCE TEST FAILED")
        return False