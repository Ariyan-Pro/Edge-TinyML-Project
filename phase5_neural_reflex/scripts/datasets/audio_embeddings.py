# phase5_neural_reflex/scripts/01_audio_embeddings.py
import librosa
import numpy as np
import sounddevice as sd
import threading
import time

class RealTimeAudioProcessor:
    def __init__(self, sample_rate=22050, frame_length=1024):
        self.sample_rate = sample_rate
        self.frame_length = frame_length
        self.is_recording = False
        self.audio_buffer = []
        
    def start_capture(self):
        """Start real-time audio capture"""
        self.is_recording = True
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Audio error: {status}")
            self.audio_buffer.extend(indata[:, 0])
            
        self.stream = sd.InputStream(
            callback=audio_callback,
            channels=1,
            samplerate=self.sample_rate,
            blocksize=self.frame_length
        )
        self.stream.start()
        
    def extract_features(self, audio_data):
        """Extract MFCC, pitch, and spectral features"""
        features = {}
        
        # MFCC Features
        mfccs = librosa.feature.mfcc(y=audio_data, sr=self.sample_rate, n_mfcc=13)
        features['mfcc_mean'] = np.mean(mfccs, axis=1)
        features['mfcc_std'] = np.std(mfccs, axis=1)
        
        # Pitch features
        pitches, magnitudes = librosa.piptrack(y=audio_data, sr=self.sample_rate)
        pitch_values = pitches[pitches > 0]
        features['pitch_mean'] = np.mean(pitch_values) if len(pitch_values) > 0 else 0
        features['pitch_std'] = np.std(pitch_values) if len(pitch_values) > 0 else 0
        
        # Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=self.sample_rate)
        features['spectral_centroid'] = np.mean(spectral_centroids)
        
        return features
    
    def get_recent_audio(self, duration_ms=1000):
        """Get recent audio for emotion analysis"""
        samples_needed = int(self.sample_rate * (duration_ms / 1000))
        if len(self.audio_buffer) >= samples_needed:
            return np.array(self.audio_buffer[-samples_needed:])
        return None
