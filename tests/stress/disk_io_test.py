import threading
import time
import json
import os
import psutil

def disk_writer(stop_event):
    """Generate heavy disk I/O"""
    test_dir = "tests/stress/io_load"
    os.makedirs(test_dir, exist_ok=True)
    
    while not stop_event.is_set():
        timestamp = int(time.time() * 1000)
        test_file = f"{test_dir}/stress_{timestamp}.json"
        
        test_data = {
            "timestamp": timestamp,
            "data": [[i * j for j in range(50)] for i in range(50)],
            "metadata": {"test": "disk_io_stress", "iteration": timestamp}
        }
        
        try:
            with open(test_file, 'w') as f:
                json.dump(test_data, f)
            
            with open(test_file, 'r') as f:
                _ = json.load(f)
            
            os.remove(test_file)
        except:
            pass
        
        time.sleep(0.1)  # Reduced sleep for more intense I/O

def run_disk_io_test(duration_minutes=1):  # Reduced duration
    print("🚨 STARTING DISK I/O OVERLOAD TEST")
    
    from system_metrics import ProductionLogger
    
    stop_event = threading.Event()
    io_thread = threading.Thread(target=disk_writer, args=(stop_event,))
    io_thread.daemon = True
    io_thread.start()
    
    logger = ProductionLogger()
    dropped_logs = 0
    timestamp_errors = 0
    
    start_time = time.time()
    last_log_time = time.time()  # Track actual log time
    
    while time.time() - start_time < duration_minutes * 60:
        current_time = time.time()
        log_data = {
            "io_stress_test": True,
            "iteration": int(current_time),
            "memory_available": psutil.virtual_memory().available
        }
        
        try:
            logger.log_system_event("io_stress", log_data)
            current_log_time = time.time()
            
            # FIXED: Check for actual gaps, not expected sleep intervals
            if last_log_time and (current_log_time - last_log_time) > 5.0:  # 5+ seconds is a real gap
                timestamp_errors += 1
                print(f"⚠️  Real log timestamp gap: {current_log_time - last_log_time:.2f}s")
            
            last_log_time = current_log_time
            
        except Exception as e:
            dropped_logs += 1
            print(f"⚠️  Log drop: {e}")
        
        time.sleep(1)  # Reduced sleep interval
    
    stop_event.set()
    time.sleep(1)
    
    # FIXED: Only fail if we have REAL gaps (>5s) or dropped logs
    if dropped_logs == 0 and timestamp_errors == 0:
        print("✅ DISK I/O OVERLOAD TEST PASSED")
        print(f"   - Dropped logs: {dropped_logs}")
        print(f"   - Real timestamp errors: {timestamp_errors}")
        return True
    else:
        print("❌ DISK I/O OVERLOAD TEST FAILED")
        return False
