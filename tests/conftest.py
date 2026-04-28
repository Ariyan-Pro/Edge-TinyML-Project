"""
Pytest configuration for Edge-TinyML test suite
"""
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers",
        [
            "slow: marks tests as slow (deselect with '-m \"not slow\"')",
            "integration: marks tests as integration tests",
            "security: marks tests as security-related",
        ]
    )
