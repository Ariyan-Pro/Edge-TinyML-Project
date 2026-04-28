# Dependency Installation Guide

## ✅ Core Dependencies (Low-Disk Optimized)

The wake word detection system now works with **minimal dependencies** (~20MB) using a NumPy-based inference backend. TensorFlow is optional for production deployments.

### Quick Install (CI/CD & Low-Disk Environments)

```bash
# Minimal core dependencies - works in <50MB disk space
pip install numpy scipy soundfile sounddevice prometheus_client pytest
```

### What's Installed

| Package | Size | Purpose | Required? |
|---------|------|---------|-----------|
| `numpy` | ~15MB | Core numerical operations | ✅ Yes |
| `scipy` | ~30MB | Signal processing | ✅ Yes |
| `soundfile` | ~2MB | Audio file I/O | ✅ Yes |
| `sounddevice` | ~1MB | Real-time audio streaming | ✅ Yes |
| `prometheus_client` | ~1MB | Metrics & monitoring | ✅ Yes |
| `pytest` | ~5MB | Testing framework | ✅ For CI |
| **Total** | **~54MB** | | |

### Optional: Full Feature Set

For production with TensorFlow acceleration and advanced audio features:

```bash
# Production mode (~500MB total)
pip install tensorflow>=2.16.0 librosa pyaudio
```

| Package | Additional Size | Purpose |
|---------|----------------|---------|
| `tensorflow` | ~450MB | TFLite GPU/CPU acceleration |
| `librosa` | ~150MB | Advanced audio analysis |
| `pyaudio` | ~5MB | Alternative audio backend |

## Architecture

```
WakeWordDetector
├─ TensorFlow Available → TFLite Interpreter (Production, fast)
└─ TensorFlow Missing → NumPy Backend (Development, works everywhere)
```

## Verification

```bash
# Test installation
python -c "from wake_word_detector import WakeWordDetector; print('✅ Ready')"

# Run tests
pytest tests/security/automated_safety_test.py -v
```

## CI/CD Integration

See `.github/workflows/ci.yml` for GitHub Actions configuration that:
- Installs only minimal dependencies
- Works with limited disk space (<100MB available)
- Tests both import and inference functionality
- Passes even without TensorFlow

## Troubleshooting

### PortAudio Error (sounddevice)
```bash
# Linux
apt-get install libportaudio2

# macOS
brew install portaudio

# Windows
# PortAudio included with sounddevice wheel
```

### librosa Import Error
```python
# librosa is optional - system works without it
# Install only if you need advanced audio features
pip install librosa
```

### Disk Space Issues
```bash
# Check available space
df -h

# Clean pip cache
pip cache purge

# Use no-cache-dir for installs
pip install --no-cache-dir numpy scipy soundfile
```
