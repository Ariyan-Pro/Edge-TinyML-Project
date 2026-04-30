"""
Security Hardening Module for ML Inference APIs

This module provides comprehensive security controls to address HIGH severity issues:
1. Tensor size limits to prevent DoS attacks
2. Real security controls (no placeholders)
3. Secure CORS configuration (no wildcards)
4. Batch processing validation

Usage:
    from security.security_hardening import SecurityValidator, SecurityConfig
    
    config = SecurityConfig()
    validator = SecurityValidator(config)
    
    # Validate tensor input
    validator.validate_tensor_size(input_tensor)
    
    # Validate CORS origin
    validator.validate_cors_origin(request_origin)
    
    # Validate batch processing
    validator.validate_batch_input(batch_data)
"""

from .security_hardening import (
    SecurityValidator,
    SecurityConfig,
    SecurityLevel,
    SecurityError,
    TensorSizeError,
    CORSError,
    BatchValidationError,
    InputValidationError,
    create_secure_api_middleware,
)

__all__ = [
    'SecurityValidator',
    'SecurityConfig',
    'SecurityLevel',
    'SecurityError',
    'TensorSizeError',
    'CORSError',
    'BatchValidationError',
    'InputValidationError',
    'create_secure_api_middleware',
]

__version__ = '1.0.0'
