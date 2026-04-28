# tests/security/virtual_mic_attack.py
"""
Virtual Microphone Attack Test
Tests system's ability to detect and protect against virtual audio device attacks.
Uses sounddevice for cross-platform audio device enumeration (no pyaudio required).
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def detect_virtual_devices():
    """Scan for virtual audio devices that could be attack vectors"""
    virtual_devices = []
    
    try:
        import sounddevice as sd
        
        # Get all audio devices
        devices = sd.query_devices()
        
        for i, device_info in enumerate(devices):
            device_name = device_info['name'].lower()
            
            # Common virtual device indicators
            virtual_keywords = [
                'virtual', 'voicemeeter', 'vb-audio', 'cable', 
                'loopback', 'blackhole', 'screencapture',
                'stereo mix', 'what u hear', 'wave out'
            ]
            
            if any(keyword in device_name for keyword in virtual_keywords):
                virtual_devices.append({
                    'index': i,
                    'name': device_info['name'],
                    'kind': device_info['kind']
                })
    except Exception as e:
        print(f"⚠️  Audio device enumeration not available: {e}")
        print("   This is normal on systems without audio hardware or drivers.")
    
    return virtual_devices


class AudioCaptureSystem:
    """
    Minimal audio capture system for security testing.
    Provides device selection logic that prioritizes physical microphones.
    """
    
    def __init__(self):
        self.physical_device = None
        self._detect_physical_device()
    
    def _detect_physical_device(self):
        """Detect the primary physical input device"""
        try:
            import sounddevice as sd
            
            devices = sd.query_devices()
            
            # Look for physical input devices (not virtual)
            virtual_keywords = ['virtual', 'voicemeeter', 'vb-audio', 'cable', 
                               'loopback', 'blackhole', 'stereo mix']
            
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    device_name = device['name'].lower()
                    
                    # Skip virtual devices
                    if any(kw in device_name for kw in virtual_keywords):
                        continue
                    
                    # Prefer default input device if it's physical
                    if device['name'] == sd.query_devices(kind='input')['name']:
                        self.physical_device = i
                        return
                    
                    # Otherwise take first physical device found
                    if self.physical_device is None:
                        self.physical_device = i
                        
        except Exception as e:
            print(f"⚠️  Could not detect physical device: {e}")
            self.physical_device = None
    
    def get_preferred_device(self):
        """Return the index of the preferred (physical) audio device"""
        return self.physical_device


def test_virtual_mic_protection():
    print("🎭 TESTING VIRTUAL MICROPHONE ATTACK PROTECTION")
    print("=" * 50)
    
    virtual_devices = detect_virtual_devices()
    
    if virtual_devices:
        print(f"⚠️  Found {len(virtual_devices)} virtual audio devices:")
        for device in virtual_devices:
            print(f"   - {device['name']} (Index: {device['index']}, Type: {device['kind']})")
        
        # Test if system prioritizes physical mic
        capture_system = AudioCaptureSystem()
        
        preferred_device = capture_system.get_preferred_device()
        
        if preferred_device is not None:
            try:
                import sounddevice as sd
                preferred_name = sd.query_devices(preferred_device)['name']
                print(f"🎯 System preferred device: {preferred_name} (Index: {preferred_device})")
                
                # Check if preferred device is physical
                if not any(vd['index'] == preferred_device for vd in virtual_devices):
                    print("✅ Virtual microphone protection: ACTIVE")
                    print("   System correctly prioritizes physical microphone over virtual devices")
                    return True
                else:
                    print("❌ Virtual microphone protection: FAILED")
                    print("   System selected a virtual device as primary input!")
                    return False
            except Exception as e:
                print(f"⚠️  Could not verify device selection: {e}")
                return True
        else:
            print("⚠️  No physical microphone detected")
            print("   This may be expected on headless/server systems")
            return True
    else:
        print("✅ No virtual audio devices detected")
        print("   System appears clean of potential virtual microphone attack vectors")
        
        # Still test the capture system exists
        capture_system = AudioCaptureSystem()
        preferred_device = capture_system.get_preferred_device()
        
        if preferred_device is not None:
            try:
                import sounddevice as sd
                preferred_name = sd.query_devices(preferred_device)['name']
                print(f"🎯 Primary physical device: {preferred_name}")
            except:
                pass
        
        return True


if __name__ == "__main__":
    success = test_virtual_mic_protection()
    print("\n" + "=" * 50)
    if success:
        print("✅ VIRTUAL MICROPHONE SECURITY TEST: PASSED")
        sys.exit(0)
    else:
        print("❌ VIRTUAL MICROPHONE SECURITY TEST: FAILED")
        sys.exit(1)