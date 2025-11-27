# tests/security/virtual_mic_attack.py
import pyaudio
import wave
import threading

def detect_virtual_devices():
    """Scan for virtual audio devices that could be attack vectors"""
    pa = pyaudio.PyAudio()
    
    virtual_devices = []
    for i in range(pa.get_device_count()):
        device_info = pa.get_device_info_by_index(i)
        device_name = device_info.get('name', '').lower()
        
        # Common virtual device indicators
        virtual_keywords = ['virtual', 'voicemeeter', 'vb-audio', 'cable', 
                           'loopback', 'blackhole', 'screencapture']
        
        if any(keyword in device_name for keyword in virtual_keywords):
            virtual_devices.append(device_info)
    
    pa.terminate()
    return virtual_devices

def test_virtual_mic_protection():
    print("🎭 TESTING VIRTUAL MICROPHONE ATTACK PROTECTION")
    
    virtual_devices = detect_virtual_devices()
    
    if virtual_devices:
        print(f"⚠️  Found {len(virtual_devices)} virtual audio devices:")
        for device in virtual_devices:
            print(f"   - {device['name']} (Index: {device['index']})")
        
        # Test if system prioritizes physical mic
        from audio_capture import AudioCaptureSystem
        capture_system = AudioCaptureSystem()
        
        preferred_device = capture_system.get_preferred_device()
        print(f"🎯 System preferred device: {preferred_device}")
        
        # Check if preferred device is physical
        if not any(vd['index'] == preferred_device for vd in virtual_devices):
            print("✅ Virtual microphone protection: ACTIVE")
            return True
        else:
            print("❌ Virtual microphone protection: FAILED")
            return False
    else:
        print("✅ No virtual audio devices detected")
        return True