import librosa
import numpy as np

class EnhancedAudioProcessor:
    def __init__(self):
        print("✅ Enhanced audio processor ready")
        
    def extract_features_from_file(self, audio_file):
        """Extract features from audio file"""
        try:
            # Load audio file
            y, sr = librosa.load(audio_file, sr=22050)
            
            # Extract features
            features = {}
            
            # MFCCs
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            features['mfcc_mean'] = np.mean(mfccs, axis=1)
            
            # Spectral features
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
            features['spectral_centroid'] = np.mean(spectral_centroid)
            
            # Pitch
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            pitch_values = pitches[pitches > 0]
            features['pitch_mean'] = np.mean(pitch_values) if len(pitch_values) > 0 else 0
            
            return features
            
        except Exception as e:
            print(f"❌ Audio processing error: {e}")
            return None
