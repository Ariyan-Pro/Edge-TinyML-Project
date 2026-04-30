# Security Hardening Module

This module addresses **4 HIGH severity security issues** in ML inference APIs:

## Issues Fixed

### 1. 🔒 Tensor Size Limits (DoS Prevention)
**Problem:** Firewall accepts 100,000+ element tensors, creating a DoS vector.

**Solution:** 
- Maximum tensor elements: **10,000** (configurable)
- Maximum dimensions: **4**
- Maximum memory footprint: **10MB**

```python
from security import SecurityValidator

validator = SecurityValidator()
validator.validate_tensor_size(input_tensor)  # Raises TensorSizeError if too large
```

### 2. ✅ Real Security Controls (No Placeholders)
**Problem:** Placeholder security controls throughout the codebase.

**Solution:**
- Input validation for NaN/Inf values
- Negative value detection
- Required field validation
- Null/empty string checks
- Comprehensive request validation

```python
validator.validate_input_values(tensor)  # Checks for NaN, Inf, negatives
validator.validate_request_complete(request_data)  # Full request validation
```

### 3. 🌐 Secure CORS Configuration
**Problem:** CORS wildcard (`*`) misconfiguration allows any origin.

**Solution:**
- Explicit allowed origins list (no wildcards)
- Origin-specific headers
- Credentials support with proper Vary header
- Configurable max-age

```python
# Trusted origins only - NO wildcards!
config = SecurityConfig(
    ALLOWED_ORIGINS=(
        "https://trusted-domain.com",
        "https://app.trusted-domain.com",
    )
)
validator = SecurityValidator(config)
cors_headers = validator.get_cors_headers(origin)
```

### 4. 📦 Batch Processing Validation
**Problem:** Empty batch processing without validation.

**Solution:**
- Reject empty batches
- Maximum batch size limits
- Batch consistency validation (shape/dtype)
- Configurable thresholds

```python
validator.validate_batch_input(batch_data)  # Raises BatchValidationError if invalid
```

## Installation

The module is located at `/workspace/security/` and requires numpy:

```bash
pip install numpy
```

## Quick Start

```python
from security import SecurityValidator, SecurityConfig, SecurityLevel

# Create configuration
config = SecurityConfig(
    MAX_TENSOR_ELEMENTS=10000,
    MAX_BATCH_SIZE=32,
    SECURITY_LEVEL=SecurityLevel.STRICT,
    ALLOWED_ORIGINS=("https://your-domain.com",)
)

# Initialize validator
validator = SecurityValidator(config)

# Use in your API endpoint
@app.route('/inference', methods=['POST'])
def inference():
    origin = request.headers.get('Origin', '')
    
    # Validate CORS
    cors_headers = validator.get_cors_headers(origin)
    if not cors_headers and origin:
        return {'error': 'Origin not allowed'}, 403
    
    # Get and validate input
    input_data = request.json['input_data']
    tensor = np.array(input_data)
    
    # Security validation
    validator.validate_tensor_size(tensor)
    validator.validate_input_values(tensor)
    
    # Process inference...
    result = model.predict(tensor)
    
    response = {'result': result.tolist()}
    response.headers.update(cors_headers)
    return response
```

## Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MAX_TENSOR_ELEMENTS` | 10,000 | Maximum number of elements in a tensor |
| `MAX_TENSOR_DIMENSIONS` | 4 | Maximum number of dimensions |
| `MAX_BATCH_SIZE` | 32 | Maximum batch size for inference |
| `MAX_INPUT_SIZE_BYTES` | 10MB | Maximum memory footprint |
| `ALLOWED_ORIGINS` | Tuple | List of trusted CORS origins |
| `REQUIRE_NON_EMPTY_BATCH` | True | Reject empty batches |
| `CHECK_NAN_INF` | True | Validate against NaN/Inf values |
| `SECURITY_LEVEL` | STRICT | STRICT, MODERATE, or PERMISSIVE |

## Exception Types

- `TensorSizeError`: Tensor exceeds size/dimension/memory limits
- `CORSError`: Origin not in allowed list or is wildcard
- `BatchValidationError`: Batch is empty, oversized, or inconsistent
- `InputValidationError`: Input contains invalid values (NaN, Inf, etc.)
- `SecurityError`: Base exception for all security violations

## Testing

Run the built-in test suite:

```bash
python security/security_hardening.py
```

Expected output shows all 4 security fixes working:
```
✅ Valid tensor accepted
✅ SECURITY SUCCESS: Malicious tensor blocked
✅ SECURITY SUCCESS: Wildcard origin blocked
✅ SECURITY SUCCESS: Empty batch blocked
✅ SECURITY SUCCESS: NaN input blocked
```

## Integration Examples

### Flask Integration

```python
from flask import Flask, request, jsonify
from security import SecurityValidator

app = Flask(__name__)
validator = SecurityValidator()

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin', '')
    cors_headers = validator.get_cors_headers(origin)
    for key, value in cors_headers.items():
        response.headers[key] = value
    return response

@app.route('/api/infer', methods=['POST'])
def infer():
    data = request.json
    validator.validate_request_complete(data)
    # ... process inference
    return jsonify({'status': 'success'})
```

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from security import SecurityValidator

app = FastAPI()
validator = SecurityValidator()

@app.middleware("http")
async def security_middleware(request: Request, call_next):
    origin = request.headers.get('Origin', '')
    
    # Store origin for later use
    request.state.origin = origin
    request.state.cors_headers = validator.get_cors_headers(origin)
    
    response = await call_next(request)
    
    # Add CORS headers
    for key, value in request.state.cors_headers.items():
        response.headers[key] = value
    
    return response

@app.post("/api/infer")
async def infer(request: Request):
    data = await request.json()
    
    try:
        validator.validate_request_complete(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # ... process inference
    return {"status": "success"}
```

## Security Best Practices

1. **Always use STRICT mode in production**
2. **Never allow CORS wildcard (*)** - explicitly list trusted domains
3. **Set appropriate tensor size limits** based on your model's actual requirements
4. **Enable rate limiting** in high-traffic scenarios
5. **Log all security violations** for monitoring and alerting
6. **Regularly review and update** allowed origins list
7. **Validate all inputs** before processing, even from trusted sources

## License

MIT License - See LICENSE file for details.
