import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
from emotion_detector import EmotionDetector
from reflex_feedback import ReflexFeedbackSystem

class RAVDESSProcessor:
    def __init__(self, data_path="../data/emotion_dataset"):
        self.data_path = data_path
        self.emotion_detector = EmotionDetector()
        self.reflex_system = ReflexFeedbackSystem()
        
        # RAVDESS emotion mapping
        self.emotion_map = {
            '01': 'neutral',
            '02': 'calm', 
            '03': 'happy',
            '04': 'sad',
            '05': 'angry',
            '06': 'fearful',
            '07': 'disgust',
            '08': 'surprised'
        }
        
    def parse_filename(self, filename):
        """Parse RAVDESS filename to extract emotion info"""
        parts = filename.split('-')
        if len(parts) >= 3:
            modality = parts[0]  # 03 = audio-only
            emotion_code = parts[2]  # emotion type
            intensity = parts[3]  # 01=normal, 02=strong
            return self.emotion_map.get(emotion_code, 'unknown')
        return 'unknown'
    
    def process_audio_file(self, file_path):
        """Process a single audio file and detect emotion"""
        try:
            # Load audio file
            y, sr = librosa.load(file_path, sr=22050)
            
            # Extract features (placeholder - adjust based on your model)
            features = self.extract_audio_features(y, sr)
            
            # Predict emotion using TFLite model
            emotion_result = self.emotion_detector.predict_emotion(features)
            
            # Get ground truth from filename
            filename = os.path.basename(file_path)
            ground_truth = self.parse_filename(filename)
            
            return {
                'file': filename,
                'ground_truth': ground_truth,
                'predicted_emotion': emotion_result['emotion'],
                'confidence': emotion_result['confidence'],
                'features': features
            }
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            return None
    
    def extract_audio_features(self, audio_data, sample_rate):
        """Extract audio features for emotion detection"""
        features = {}
        
        # MFCC Features
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=13)
        features['mfcc_mean'] = np.mean(mfccs, axis=1)
        features['mfcc_std'] = np.std(mfccs, axis=1)
        
        # Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=sample_rate)
        features['spectral_centroid'] = np.mean(spectral_centroids)
        
        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(audio_data)
        features['zcr_mean'] = np.mean(zcr)
        
        return features
    
    def test_dataset_samples(self, num_samples=10):
        """Test emotion detection on random dataset samples"""
        print("🧪 TESTING RAVDESS DATASET EMOTION DETECTION")
        print("=" * 60)
        
        # Find audio files
        audio_files = []
        speech_path = os.path.join(self.data_path, "Audio_Speech_Actors_01-24")
        
        for actor_dir in os.listdir(speech_path):
            actor_path = os.path.join(speech_path, actor_dir)
            if os.path.isdir(actor_path):
                for file in os.listdir(actor_path):
                    if file.endswith('.wav'):
                        audio_files.append(os.path.join(actor_path, file))
        
        print(f"📁 Found {len(audio_files)} audio files")
        
        # Test random samples
        import random
        test_files = random.sample(audio_files, min(num_samples, len(audio_files)))
        
        results = []
        for file_path in test_files:
            print(f"\\n🎵 Processing: {os.path.basename(file_path)}")
            result = self.process_audio_file(file_path)
            if result:
                results.append(result)
                print(f"   Ground Truth: {result['ground_truth']}")
                print(f"   Predicted: {result['predicted_emotion']} ({result['confidence']:.2f})")
                
                # Test reflex system
                test_data = {
                    'emotion': result['predicted_emotion'],
                    'confidence': result['confidence'],
                    'timestamp': np.datetime64('now')
                }
                reflex_state = self.reflex_system.update_emotion(test_data)
                print(f"   Reflex State: {reflex_state}")
        
        return results
    
    def analyze_emotion_distribution(self):
        """Analyze emotion distribution in the dataset"""
        print("\\n📊 ANALYZING DATASET EMOTION DISTRIBUTION")
        print("=" * 50)
        
        emotion_counts = {}
        speech_path = os.path.join(self.data_path, "Audio_Speech_Actors_01-24")
        
        for actor_dir in os.listdir(speech_path):
            actor_path = os.path.join(speech_path, actor_dir)
            if os.path.isdir(actor_path):
                for file in os.listdir(actor_path):
                    if file.endswith('.wav'):
                        emotion = self.parse_filename(file)
                        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Display distribution
        for emotion, count in emotion_counts.items():
            print(f"   {emotion}: {count} files")
        
        return emotion_counts

# Test the dataset processor
if __name__ == "__main__":
    processor = RAVDESSProcessor()
    
    # Analyze dataset
    processor.analyze_emotion_distribution()
    
    # Test emotion detection on samples
    print("\\n" + "="*60)
    results = processor.test_dataset_samples(num_samples=5)
    
    print(f"\\n🎉 Successfully processed {len(results)} audio samples!")
    print("📈 Neural Reflex System is now working with REAL emotional audio!")
