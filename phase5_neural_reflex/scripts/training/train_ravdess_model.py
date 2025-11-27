import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import librosa
import pickle
from pathlib import Path

class RAVDESSModelTrainer:
    """Train emotion detection model on RAVDESS dataset"""
    
    def __init__(self, data_path="data/emotion_dataset"):
        self.data_path = Path(data_path)
        self.emotion_labels = {
            '01': 'neutral', '02': 'calm', '03': 'happy', '04': 'sad',
            '05': 'angry', '06': 'fearful', '07': 'disgust', '08': 'surprised'
        }
        self.features = []
        self.labels = []
        
    def extract_ravdess_features(self, audio_path):
        """Extract features from RAVDESS audio files"""
        try:
            # Load audio file
            y, sr = librosa.load(audio_path, sr=22050)
            
            # Extract features (matching real-time system)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            mfcc_mean = np.mean(mfccs, axis=1)
            mfcc_std = np.std(mfccs, axis=1)
            
            spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
            spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
            zcr = np.mean(librosa.feature.zero_crossing_rate(y))
            rms = np.mean(librosa.feature.rms(y=y))
            
            # Pitch detection
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            pitch_mean = np.mean(pitches[pitches > 0]) if np.any(pitches > 0) else 0
            
            # Combine features
            feature_vector = np.concatenate([
                mfcc_mean, mfcc_std,
                [spectral_centroid, spectral_rolloff, zcr, rms, pitch_mean]
            ])
            
            return feature_vector
            
        except Exception as e:
            print(f"Error processing {audio_path}: {e}")
            return None
    
    def load_ravdess_dataset(self):
        """Load and process RAVDESS dataset"""
        print("📁 Loading RAVDESS dataset...")
        
        for dataset_type in ['Audio_Speech_Actors_01-24', 'Audio_Song_Actors_01-24']:
            dataset_path = self.data_path / dataset_type
            
            for actor_dir in dataset_path.iterdir():
                if actor_dir.is_dir():
                    for audio_file in actor_dir.glob("*.wav"):
                        # Extract emotion from filename
                        filename = audio_file.stem
                        parts = filename.split('-')
                        emotion_code = parts[2]
                        
                        if emotion_code in self.emotion_labels:
                            emotion = self.emotion_labels[emotion_code]
                            
                            # Extract features
                            features = self.extract_ravdess_features(audio_file)
                            if features is not None:
                                self.features.append(features)
                                self.labels.append(emotion)
                        
                        # Progress indicator
                        if len(self.features) % 100 == 0:
                            print(f"Processed {len(self.features)} samples...")
        
        print(f"✅ Loaded {len(self.features)} samples with {len(set(self.labels))} emotions")
    
    def create_model(self, input_dim):
        """Create optimized TFLite-compatible model"""
        model = keras.Sequential([
            keras.layers.Dense(128, activation='relu', input_shape=(input_dim,)),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(len(self.emotion_labels), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train_and_export(self):
        """Train model and export to TFLite"""
        print("🧠 Training emotion detection model...")
        
        # Encode labels
        label_encoder = LabelEncoder()
        labels_encoded = label_encoder.fit_transform(self.labels)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            self.features, labels_encoded, test_size=0.2, random_state=42
        )
        
        # Create and train model
        model = self.create_model(len(X_train[0]))
        
        history = model.fit(
            X_train, y_train,
            epochs=50,
            batch_size=32,
            validation_data=(X_test, y_test),
            verbose=1
        )
        
        # Evaluate model
        test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
        print(f"🎯 Final Test Accuracy: {test_accuracy:.3f}")
        
        # Convert to TFLite
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        tflite_model = converter.convert()
        
        # Save TFLite model
        tflite_path = "models/emotion_detector_ravdess.tflite"
        with open(tflite_path, 'wb') as f:
            f.write(tflite_model)
        
        # Save label encoder
        with open("models/label_encoder.pkl", 'wb') as f:
            pickle.dump(label_encoder, f)
        
        print(f"✅ TFLite model saved: {tflite_path}")
        print(f"📊 Model size: {len(tflite_model)} bytes")
        
        return test_accuracy

if __name__ == "__main__":
    print("🎵 RAVDESS EMOTION MODEL TRAINING")
    print("=" * 50)
    
    trainer = RAVDESSModelTrainer()
    trainer.load_ravdess_dataset()
    
    if trainer.features:
        accuracy = trainer.train_and_export()
        print(f"🎉 Training complete! Accuracy: {accuracy:.1%}")
        
        if accuracy >= 0.85:
            print("✅ TARGET ACHIEVED: ≥85% accuracy!")
        else:
            print("⚠️  Accuracy below target - consider model tuning")
    else:
        print("❌ No features extracted - check dataset path")
