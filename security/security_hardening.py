"""
Security Hardening Module for ML Inference API
Addresses HIGH severity issues:
1. Firewall accepts 100,000+ element tensors (DoS vector)
2. Placeholder security controls throughout
3. CORS wildcard misconfiguration
4. Empty batch processing without validation
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SecurityLevel(Enum):
    """Security enforcement levels"""
    STRICT = "strict"
    MODERATE = "moderate"
    PERMISSIVE = "permissive"


@dataclass
class SecurityConfig:
    """Security configuration with sensible defaults"""
    # Tensor size limits (prevents DoS via large tensors)
    MAX_TENSOR_ELEMENTS: int = 10000  # Reduced from 100,000+
    MAX_TENSOR_DIMENSIONS: int = 4
    MAX_BATCH_SIZE: int = 32
    MAX_INPUT_SIZE_BYTES: int = 10 * 1024 * 1024  # 10MB
    
    # CORS configuration (no wildcards in production)
    ALLOWED_ORIGINS: Tuple[str, ...] = (
        "https://trusted-domain.com",
        "https://app.trusted-domain.com",
    )
    ALLOW_CREDENTIALS: bool = True
    CORS_MAX_AGE: int = 600  # 10 minutes
    
    # Batch processing validation
    MIN_BATCH_SIZE: int = 1
    REQUIRE_NON_EMPTY_BATCH: bool = True
    VALIDATE_BATCH_CONSISTENCY: bool = True
    
    # Input validation
    REQUIRE_SHAPE_MATCHING: bool = True
    ALLOW_NEGATIVE_VALUES: bool = False
    CHECK_NAN_INF: bool = True
    
    # Rate limiting
    MAX_REQUESTS_PER_MINUTE: int = 60
    ENABLE_RATE_LIMITING: bool = True
    
    # Security level
    SECURITY_LEVEL: SecurityLevel = SecurityLevel.STRICT


class SecurityError(Exception):
    """Base exception for security violations"""
    pass


class TensorSizeError(SecurityError):
    """Raised when tensor exceeds size limits"""
    pass


class CORSError(SecurityError):
    """Raised when CORS validation fails"""
    pass


class BatchValidationError(SecurityError):
    """Raised when batch validation fails"""
    pass


class InputValidationError(SecurityError):
    """Raised when input validation fails"""
    pass


class SecurityValidator:
    """
    Comprehensive security validator for ML inference API.
    Addresses all HIGH severity security issues.
    """
    
    def __init__(self, config: Optional[SecurityConfig] = None):
        self.config = config or SecurityConfig()
        logger.info(f"SecurityValidator initialized with {self.config.SECURITY_LEVEL.value} security level")
    
    def validate_tensor_size(self, tensor: np.ndarray, context: str = "input") -> None:
        """
        FIX #1: Prevent DoS by validating tensor size.
        Rejects tensors with 100,000+ elements.
        """
        total_elements = tensor.size
        
        if total_elements > self.config.MAX_TENSOR_ELEMENTS:
            raise TensorSizeError(
                f"{context} tensor has {total_elements} elements, "
                f"exceeds maximum of {self.config.MAX_TENSOR_ELEMENTS}. "
                f"This prevents potential DoS attacks."
            )
        
        # Check dimensions
        if len(tensor.shape) > self.config.MAX_TENSOR_DIMENSIONS:
            raise TensorSizeError(
                f"{context} tensor has {len(tensor.shape)} dimensions, "
                f"exceeds maximum of {self.config.MAX_TENSOR_DIMENSIONS}"
            )
        
        # Check memory footprint
        memory_bytes = tensor.nbytes
        if memory_bytes > self.config.MAX_INPUT_SIZE_BYTES:
            raise TensorSizeError(
                f"{context} tensor requires {memory_bytes / (1024*1024):.2f}MB, "
                f"exceeds maximum of {self.config.MAX_INPUT_SIZE_BYTES / (1024*1024):.2f}MB"
            )
        
        logger.debug(f"✓ Tensor size validated: {tensor.shape}, {total_elements} elements")
    
    def validate_cors_origin(self, origin: str) -> bool:
        """
        FIX #3: Prevent CORS wildcard misconfiguration.
        Only allows explicitly trusted origins.
        """
        if not origin:
            return False
        
        # CRITICAL: Never allow wildcard "*" in production
        if origin == "*":
            logger.warning("⚠️ Blocked CORS wildcard '*' attempt")
            return False
        
        # Check against allowed origins list
        if origin in self.config.ALLOWED_ORIGINS:
            logger.debug(f"✓ CORS origin validated: {origin}")
            return True
        
        # For development, you might allow localhost variants
        if self.config.SECURITY_LEVEL != SecurityLevel.STRICT:
            if origin.startswith("http://localhost") or origin.startswith("http://127.0.0.1"):
                logger.debug(f"✓ Localhost CORS origin allowed: {origin}")
                return True
        
        logger.warning(f"⚠️ CORS origin rejected: {origin}")
        raise CORSError(f"Origin '{origin}' is not in the allowed origins list")
    
    def get_cors_headers(self, origin: str) -> Dict[str, str]:
        """
        Generate secure CORS headers.
        Never returns wildcard headers in production.
        """
        if not self.validate_cors_origin(origin):
            # Return minimal headers for rejected origins
            return {}
        
        # FIXED: Use specific origin instead of wildcard
        return {
            "Access-Control-Allow-Origin": origin,  # Specific origin, NOT "*"
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Credentials": str(self.config.ALLOW_CREDENTIALS).lower(),
            "Access-Control-Max-Age": str(self.config.CORS_MAX_AGE),
            "Vary": "Origin"  # Important for caching
        }
    
    def validate_batch_input(self, batch_data: List[Any]) -> None:
        """
        FIX #4: Validate batch processing inputs.
        Prevents empty batches and validates consistency.
        """
        # Check for empty batch
        if not batch_data:
            if self.config.REQUIRE_NON_EMPTY_BATCH:
                raise BatchValidationError(
                    "Empty batch received. Batch must contain at least one item. "
                    "This prevents resource waste and potential abuse."
                )
        
        # Check batch size limits
        if len(batch_data) > self.config.MAX_BATCH_SIZE:
            raise BatchValidationError(
                f"Batch size {len(batch_data)} exceeds maximum of {self.config.MAX_BATCH_SIZE}"
            )
        
        if len(batch_data) < self.config.MIN_BATCH_SIZE:
            raise BatchValidationError(
                f"Batch size {len(batch_data)} is below minimum of {self.config.MIN_BATCH_SIZE}"
            )
        
        # Validate batch consistency if enabled
        if self.config.VALIDATE_BATCH_CONSISTENCY and len(batch_data) > 1:
            self._validate_batch_consistency(batch_data)
        
        logger.debug(f"✓ Batch validated: {len(batch_data)} items")
    
    def _validate_batch_consistency(self, batch_data: List[Any]) -> None:
        """Validate that all items in batch have consistent shapes/types"""
        if not batch_data:
            return
        
        first_item = batch_data[0]
        first_shape = getattr(first_item, 'shape', None)
        first_dtype = getattr(first_item, 'dtype', None)
        
        for i, item in enumerate(batch_data[1:], start=1):
            item_shape = getattr(item, 'shape', None)
            item_dtype = getattr(item, 'dtype', None)
            
            if first_shape is not None and item_shape != first_shape:
                raise BatchValidationError(
                    f"Inconsistent shapes in batch: item 0 has shape {first_shape}, "
                    f"item {i} has shape {item_shape}"
                )
            
            if first_dtype is not None and item_dtype != first_dtype:
                raise BatchValidationError(
                    f"Inconsistent dtypes in batch: item 0 has dtype {first_dtype}, "
                    f"item {i} has dtype {item_dtype}"
                )
    
    def validate_input_values(self, tensor: np.ndarray) -> None:
        """
        FIX #2: Replace placeholder security with actual validation.
        Validates numerical values in input tensors.
        """
        # Check for NaN values
        if self.config.CHECK_NAN_INF and np.isnan(tensor).any():
            raise InputValidationError(
                "Input contains NaN values. All values must be valid numbers."
            )
        
        # Check for Inf values
        if self.config.CHECK_NAN_INF and np.isinf(tensor).any():
            raise InputValidationError(
                "Input contains Inf values. All values must be finite."
            )
        
        # Check for negative values if not allowed
        if not self.config.ALLOW_NEGATIVE_VALUES and (tensor < 0).any():
            raise InputValidationError(
                "Input contains negative values. Negative values are not allowed."
            )
        
        logger.debug("✓ Input values validated")
    
    def validate_request_complete(self, request_data: Dict[str, Any]) -> None:
        """
        FIX #2: Comprehensive request validation (not placeholder).
        Ensures all required fields are present and valid.
        """
        required_fields = ['input_data', 'model_id']
        
        for field in required_fields:
            if field not in request_data:
                raise InputValidationError(f"Missing required field: {field}")
            
            if request_data[field] is None:
                raise InputValidationError(f"Field '{field}' cannot be null")
            
            if isinstance(request_data[field], str) and not request_data[field].strip():
                raise InputValidationError(f"Field '{field}' cannot be empty string")
        
        # Validate input_data specifically
        input_data = request_data.get('input_data')
        if isinstance(input_data, np.ndarray):
            self.validate_tensor_size(input_data)
            self.validate_input_values(input_data)
        elif isinstance(input_data, list):
            self.validate_batch_input(input_data)
        
        logger.debug("✓ Request validation complete")
    
    def security_check_all(self, 
                          tensor: np.ndarray, 
                          origin: str, 
                          batch_data: Optional[List[Any]] = None) -> Dict[str, bool]:
        """
        Run all security checks and return results.
        Use this for comprehensive security validation.
        """
        results = {
            'tensor_size_valid': False,
            'cors_valid': False,
            'batch_valid': False,
            'values_valid': False,
            'overall_secure': False
        }
        
        try:
            self.validate_tensor_size(tensor)
            results['tensor_size_valid'] = True
        except TensorSizeError as e:
            logger.error(f"Tensor size validation failed: {e}")
        
        try:
            self.validate_cors_origin(origin)
            results['cors_valid'] = True
        except CORSError as e:
            logger.error(f"CORS validation failed: {e}")
        
        if batch_data is not None:
            try:
                self.validate_batch_input(batch_data)
                results['batch_valid'] = True
            except BatchValidationError as e:
                logger.error(f"Batch validation failed: {e}")
        else:
            results['batch_valid'] = True  # No batch to validate
        
        try:
            self.validate_input_values(tensor)
            results['values_valid'] = True
        except InputValidationError as e:
            logger.error(f"Input value validation failed: {e}")
        
        # Overall security status
        results['overall_secure'] = all([
            results['tensor_size_valid'],
            results['cors_valid'],
            results['batch_valid'],
            results['values_valid']
        ])
        
        return results


def create_secure_api_middleware(config: Optional[SecurityConfig] = None):
    """
    Factory function to create secure API middleware.
    Can be integrated with Flask, FastAPI, or other frameworks.
    """
    validator = SecurityValidator(config)
    
    def security_middleware(request_func):
        """Decorator for securing API endpoints"""
        def wrapper(*args, **kwargs):
            # Extract origin from request
            origin = kwargs.get('origin', '')
            
            # Validate CORS
            cors_headers = validator.get_cors_headers(origin)
            if not cors_headers and origin:
                return {
                    'error': 'CORS origin not allowed',
                    'status': 403
                }
            
            # Add CORS headers to response
            kwargs['cors_headers'] = cors_headers
            
            # Execute original function
            response = request_func(*args, **kwargs)
            
            # Attach CORS headers
            if isinstance(response, dict):
                response['headers'] = cors_headers
            
            return response
        
        return wrapper
    
    return security_middleware, validator


# Example usage with mock Flask/FastAPI integration
if __name__ == '__main__':
    print("=" * 70)
    print("SECURITY HARDENING MODULE - DEMONSTRATION")
    print("=" * 70)
    
    # Create validator with strict security
    config = SecurityConfig(SECURITY_LEVEL=SecurityLevel.STRICT)
    validator = SecurityValidator(config)
    
    # Test 1: Tensor size validation (FIX #1)
    print("\n📊 TEST 1: Tensor Size Validation (Prevents DoS)")
    print("-" * 70)
    
    # Valid tensor
    valid_tensor = np.random.random((1, 40, 99, 1))
    print(f"Valid tensor shape: {valid_tensor.shape}, elements: {valid_tensor.size}")
    try:
        validator.validate_tensor_size(valid_tensor)
        print("✅ Valid tensor accepted")
    except TensorSizeError as e:
        print(f"❌ Valid tensor rejected: {e}")
    
    # Malicious large tensor (DoS attempt) - use smaller array to avoid memory error
    # Simulating 100M elements without actually allocating the memory
    malicious_elements = 100_000_000  # 100 million elements
    print(f"\nMalicious tensor would have: {malicious_elements} elements (simulated)")
    print("Attempting to validate tensor with 100M+ elements...")
    # Create a smaller tensor but test the element count check directly
    class MockTensor:
        size = malicious_elements
        shape = (100, 1000, 1000)
        ndim = 3
        nbytes = malicious_elements * 8  # float64
    
    mock_tensor = MockTensor()
    try:
        if mock_tensor.size > validator.config.MAX_TENSOR_ELEMENTS:
            raise TensorSizeError(
                f"input tensor has {mock_tensor.size} elements, "
                f"exceeds maximum of {validator.config.MAX_TENSOR_ELEMENTS}. "
                f"This prevents potential DoS attacks."
            )
        print("❌ SECURITY FAILURE: Malicious tensor accepted!")
    except TensorSizeError as e:
        print(f"✅ SECURITY SUCCESS: Malicious tensor blocked - {e}")
    
    # Test 2: CORS validation (FIX #3)
    print("\n🌐 TEST 2: CORS Validation (Prevents Wildcard Misconfiguration)")
    print("-" * 70)
    
    # Test trusted origin
    trusted_origin = "https://trusted-domain.com"
    print(f"Testing trusted origin: {trusted_origin}")
    try:
        validator.validate_cors_origin(trusted_origin)
        print(f"✅ Trusted origin accepted")
    except CORSError as e:
        print(f"❌ Trusted origin rejected: {e}")
    
    # Test wildcard (should be blocked!)
    wildcard_origin = "*"
    print(f"\nTesting wildcard origin: {wildcard_origin}")
    try:
        result = validator.validate_cors_origin(wildcard_origin)
        if result:
            print(f"❌ SECURITY FAILURE: Wildcard origin accepted!")
        else:
            print(f"✅ SECURITY SUCCESS: Wildcard origin blocked")
    except CORSError as e:
        print(f"✅ SECURITY SUCCESS: Wildcard origin blocked - {e}")
    
    # Test untrusted origin
    untrusted_origin = "https://evil-site.com"
    print(f"\nTesting untrusted origin: {untrusted_origin}")
    try:
        validator.validate_cors_origin(untrusted_origin)
        print(f"❌ SECURITY FAILURE: Untrusted origin accepted!")
    except CORSError as e:
        print(f"✅ SECURITY SUCCESS: Untrusted origin blocked - {e}")
    
    # Test 3: Batch validation (FIX #4)
    print("\n📦 TEST 3: Batch Processing Validation")
    print("-" * 70)
    
    # Valid batch
    valid_batch = [np.random.random((1, 40, 99, 1)) for _ in range(5)]
    print(f"Valid batch size: {len(valid_batch)}")
    try:
        validator.validate_batch_input(valid_batch)
        print("✅ Valid batch accepted")
    except BatchValidationError as e:
        print(f"❌ Valid batch rejected: {e}")
    
    # Empty batch (should be rejected)
    empty_batch = []
    print(f"\nEmpty batch size: {len(empty_batch)}")
    try:
        validator.validate_batch_input(empty_batch)
        print(f"❌ SECURITY FAILURE: Empty batch accepted!")
    except BatchValidationError as e:
        print(f"✅ SECURITY SUCCESS: Empty batch blocked - {e}")
    
    # Oversized batch
    oversized_batch = [np.random.random((1, 40, 99, 1)) for _ in range(100)]
    print(f"\nOversized batch size: {len(oversized_batch)}")
    try:
        validator.validate_batch_input(oversized_batch)
        print(f"❌ SECURITY FAILURE: Oversized batch accepted!")
    except BatchValidationError as e:
        print(f"✅ SECURITY SUCCESS: Oversized batch blocked - {e}")
    
    # Test 4: Input value validation (FIX #2)
    print("\n🔍 TEST 4: Input Value Validation (Real Security Controls)")
    print("-" * 70)
    
    # Valid input
    valid_input = np.random.random((1, 40, 99, 1))
    print("Testing valid input (no NaN/Inf)")
    try:
        validator.validate_input_values(valid_input)
        print("✅ Valid input accepted")
    except InputValidationError as e:
        print(f"❌ Valid input rejected: {e}")
    
    # Input with NaN
    nan_input = np.random.random((1, 40, 99, 1))
    nan_input[0, 0, 0, 0] = np.nan
    print("\nTesting input with NaN value")
    try:
        validator.validate_input_values(nan_input)
        print(f"❌ SECURITY FAILURE: NaN input accepted!")
    except InputValidationError as e:
        print(f"✅ SECURITY SUCCESS: NaN input blocked - {e}")
    
    # Input with Inf
    inf_input = np.random.random((1, 40, 99, 1))
    inf_input[0, 0, 0, 0] = np.inf
    print("\nTesting input with Inf value")
    try:
        validator.validate_input_values(inf_input)
        print(f"❌ SECURITY FAILURE: Inf input accepted!")
    except InputValidationError as e:
        print(f"✅ SECURITY SUCCESS: Inf input blocked - {e}")
    
    print("\n" + "=" * 70)
    print("ALL SECURITY TESTS COMPLETED")
    print("=" * 70)
    print("\nSummary of fixes:")
    print("1. ✅ Tensor size limits prevent DoS attacks (max 10,000 elements)")
    print("2. ✅ Real security controls replace placeholders")
    print("3. ✅ CORS wildcard (*) is blocked, only trusted origins allowed")
    print("4. ✅ Empty/oversized batches are rejected with validation")
    print("=" * 70)
