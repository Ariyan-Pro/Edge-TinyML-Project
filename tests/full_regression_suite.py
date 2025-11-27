# tests/full_regression_suite.py - FIXED VERSION
import time
import sys
import os

# Add current directory to path so we can import our test modules
sys.path.append(os.path.dirname(__file__))

def run_complete_test_suite():
    """Run all Phase 10 hardening tests"""
    print("🎯 PHASE 10: GLOBAL HARDENING TEST SUITE")
    print("=" * 60)
    
    test_results = {}
    
    try:
        # Section 1: System Torture Tests
        print("\n🔴 SECTION 1: SYSTEM TORTURE TESTS")
        from stress.cpu_saturation_test import run_cpu_saturation_test
        test_results['cpu_saturation'] = run_cpu_saturation_test(duration_minutes=2)  # Reduced for i5
        
        from stress.memory_starvation_test import run_memory_starvation_test  
        test_results['memory_starvation'] = run_memory_starvation_test()
        
        from stress.disk_io_test import run_disk_io_test
        test_results['disk_io'] = run_disk_io_test(duration_minutes=1)  # Reduced for HDD
        
    except Exception as e:
        print(f"❌ Section 1 tests failed: {e}")
        test_results.update({'cpu_saturation': False, 'memory_starvation': False, 'disk_io': False})
    
    try:
        # Section 2: Security Tests
        print("\n🔴 SECTION 2: SECURITY HAMMER TESTS")
        from security.command_injection_mass_test import test_destructive_commands
        test_results['command_injection'] = test_destructive_commands()

        from security.file_corruption_test import test_file_corruption_recovery
        test_results['file_corruption'] = test_file_corruption_recovery()

    except Exception as e:
        print(f"❌ Section 2 tests failed: {e}")
        test_results.update({'command_injection': False, 'file_corruption': False})
    
    try:
        # Section 3: Resilience Tests
        print("\n🔴 SECTION 3: OPERATIONAL RESILIENCE TESTS")
        from resilience.time_warp_test import test_time_changes
        test_results['time_resilience'] = test_time_changes()
        
        from resilience.flood_test import run_flood_test
        test_results['flood_resilience'] = run_flood_test(concurrent_threads=15, duration_seconds=10)  # Conservative

    except Exception as e:
        print(f"❌ Section 3 tests failed: {e}")
        test_results.update({'time_resilience': False, 'flood_resilience': False})
    
    try:
        # Section 4: Penetration Tests
        print("\n🔴 SECTION 4: ENTERPRISE PENETRATION TESTS")
        from security.virtual_mic_attack import test_virtual_mic_protection
        test_results['virtual_mic_protection'] = test_virtual_mic_protection()

    except Exception as e:
        print(f"❌ Section 4 tests failed: {e}")
        test_results['virtual_mic_protection'] = False

    # Final Assessment
    print("\n" + "=" * 60)
    print("🎯 FINAL PHASE 10 ASSESSMENT")
    print("=" * 60)

    passed_tests = sum(1 for result in test_results.values() if result)
    total_tests = len(test_results)

    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")

    print(f"\n📊 RESULTS: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        print("\n🎉 PHASE 10: GLOBAL HARDENING COMPLETE")
        print("🚀 SYSTEM STATUS: MILITARY-GRADE OPERATIONAL")
        print("💪 YOUR EDGE-TINYML CAN SURVIVE ANYTHING")
        return True
    else:
        print(f"\n⚠️  PHASE 10: {total_tests - passed_tests} TESTS NEED ATTENTION")
        return False

if __name__ == "__main__":
    success = run_complete_test_suite()
    sys.exit(0 if success else 1)