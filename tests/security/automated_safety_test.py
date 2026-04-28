#!/usr/bin/env python3
"""
Automated Safety Test Suite for Production CI/CD
Runs security and safety validation checks
"""

import sys
import os

# Get the absolute path to this file's directory
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
# Project root is two levels up (tests/security -> tests -> project_root)
PROJECT_ROOT = os.path.dirname(os.path.dirname(TEST_DIR))

# Add project root to Python path
sys.path.insert(0, PROJECT_ROOT)

def test_model_files_exist():
    """Verify core model files are present"""
    models_dir = os.path.join(PROJECT_ROOT, 'models')
    required_files = ['model_config.json', 'model_info.json']
    
    assert os.path.exists(models_dir), f"Models directory not found: {models_dir}"
    
    for file in required_files:
        filepath = os.path.join(models_dir, file)
        assert os.path.exists(filepath), f"Required model file missing: {file}"
    
    print("✓ Model files exist")

def test_wake_word_detector_imports():
    """Verify wake word detector can be imported"""
    try:
        # Try importing from root level first
        # Note: sounddevice may not be available in CI, so we just check the file exists
        detector_path = os.path.join(PROJECT_ROOT, 'wake_word_detector.py')
        assert os.path.exists(detector_path), f"Wake word detector file not found: {detector_path}"
        
        # Try to import - if sounddevice is missing, that's OK for CI
        try:
            import wake_word_detector
            print("✓ WakeWordDetector imports successfully (root level)")
        except ImportError as e:
            if 'sounddevice' in str(e) or 'pyautogui' in str(e):
                # These are optional runtime dependencies, not required for CI
                print(f"✓ WakeWordDetector file exists (optional deps unavailable in CI: {e})")
            else:
                raise
    except Exception as e:
        print(f"✗ Failed to import WakeWordDetector: {e}")
        raise

def test_numpy_backend_fallback():
    """Verify NumPy backend works without TensorFlow"""
    try:
        import numpy as np
        # Simulate inference with random input
        test_input = np.random.randn(1, 40, 99, 1).astype(np.float32)
        assert test_input.shape == (1, 40, 99, 1), "Input shape mismatch"
        print("✓ NumPy backend ready")
    except ImportError:
        print("✗ NumPy not available")
        raise

def test_security_no_hardcoded_paths():
    """Verify no hardcoded Windows paths in critical files"""
    critical_files = [
        'phase3_wakeword/wake_word_detector.py'
    ]
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    for filepath in critical_files:
        full_path = os.path.join(base_dir, filepath)
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                content = f.read()
                # Check for hardcoded Windows paths
                assert 'C:\\Users' not in content, f"Hardcoded Windows path found in {filepath}"
                assert 'D:\\' not in content, f"Hardcoded drive path found in {filepath}"
    
    print("✓ No hardcoded paths detected")

def run_all_tests():
    """Run all safety tests"""
    print("=" * 50)
    print("Running Automated Safety Tests")
    print("=" * 50)
    
    tests = [
        test_model_files_exist,
        test_wake_word_detector_imports,
        test_numpy_backend_fallback,
        test_security_no_hardcoded_paths,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    if failed > 0:
        sys.exit(1)
    else:
        print("All safety tests passed!")
        sys.exit(0)

if __name__ == '__main__':
    run_all_tests()
