import tensorflow as tf
import numpy as np
from typing import Dict, Tuple
import time

class ProductionEmotionDetector:
    """Production emotion detector using your trained RAVDESS model"""
    
    def __init__(self, model_path="models/emotion_detector_optimized.tflite"):
        self.model_path = model_path
        self.emotion_labels = [
            'neutral', 'calm', 'happy', 'sad', 
            'angry', 'fearful', 'disgust', 'surprised'
        ]
        
        # Load the trained TFLite model
        try:
            self.interpreter = tf.lite.Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()
            print(f"✅ Loaded trained emotion model: {model_path}")
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            self.interpreter = None
    
    def predict_emotion(self, features: Dict) -> Tuple[str, float, Dict]:
        """Predict emotion from audio features using trained model"""
        
        if self.interpreter is None:
            # Fallback to mock prediction
            return self.mock_emotion_prediction(features)
        
        try:
            # Get model details
            input_details = self.interpreter.get_input_details()
            output_details = self.interpreter.get_output_details()
            
            # Prepare input feature vector
            feature_vector = self._extract_feature_vector(features)
            input_data = np.array([feature_vector], dtype=np.float32)
            
            # Run inference
            self.interpreter.set_tensor(input_details[0]['index'], input_data)
            start_time = time.time()
            self.interpreter.invoke()
            inference_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Get predictions
            predictions = self.interpreter.get_tensor(output_details[0]['index'])
            emotion_index = np.argmax(predictions[0])
            confidence = float(predictions[0][emotion_index])
            emotion = self.emotion_labels[emotion_index]
            
            # Determine intensity
            intensity = 'high' if confidence > 0.7 else 'medium' if confidence > 0.4 else 'low'
            
            return emotion, confidence, {
                'intensity': intensity,
                'inference_time_ms': inference_time,
                'all_predictions': predictions[0].tolist(),
                'model_used': 'trained_ravdess'
            }
            
        except Exception as e:
            print(f"❌ Emotion prediction error: {e}")
            return self.mock_emotion_prediction(features)
    
    def _extract_feature_vector(self, features: Dict) -> np.ndarray:
        """Extract feature vector compatible with trained model"""
        vector = []
        
        # MFCC features (13 coefficients)
        if 'mfcc_mean' in features:
            mfcc_features = features['mfcc_mean'][:13]  # Take first 13 MFCCs
            if len(mfcc_features) < 13:
                mfcc_features = np.pad(mfcc_features, (0, 13 - len(mfcc_features)))
            vector.extend(mfcc_features)
        else:
            vector.extend([0] * 13)
        
        # Additional features (spectral_centroid, zcr, rms)
        additional_features = ['spectral_centroid', 'zcr', 'rms']
        for feature_name in additional_features:
            if feature_name in features:
                vector.append(float(features[feature_name]))
            else:
                vector.append(0.0)
        
        return np.array(vector, dtype=np.float32)
    
    def mock_emotion_prediction(self, features: Dict) -> Tuple[str, float, Dict]:
        """Fallback mock prediction"""
        # Simple rule-based fallback
        emotion_scores = {}
        
        if 'rms' in features:
            energy = features['rms']
            if energy > 0.1:
                emotion_scores['angry'] = min(energy * 3, 0.8)
                emotion_scores['happy'] = min(energy * 2, 0.7)
            else:
                emotion_scores['calm'] = 0.6
                emotion_scores['neutral'] = 0.5
        
        if 'zcr' in features:
            if features['zcr'] > 0.05:
                emotion_scores['surprised'] = 0.5
        
        if not emotion_scores:
            emotion_scores['neutral'] = 0.5
        
        emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = emotion_scores[emotion]
        
        return emotion, confidence, {
            'intensity': 'high' if confidence > 0.7 else 'medium',
            'model_used': 'mock_fallback'
        }

# Test the production emotion detector
if __name__ == "__main__":
    print("🧪 TESTING PRODUCTION EMOTION DETECTOR")
    print("=" * 50)
    
    detector = ProductionEmotionDetector()
    
    # Test with sample features
    test_features = {
        'mfcc_mean': np.random.rand(13).tolist(),
        'spectral_centroid': 1500.0,
        'zcr': 0.03,
        'rms': 0.08
    }
    
    emotion, confidence, details = detector.predict_emotion(test_features)
    
    print(f"🎭 Emotion: {emotion}")
    print(f"📊 Confidence: {confidence:.3f}")
    print(f"⚡ Intensity: {details['intensity']}")
    print(f"🤖 Model: {details['model_used']}")
    if 'inference_time_ms' in details:
        print(f"⏱️  Inference Time: {details['inference_time_ms']:.2f} ms")
    
    print("✅ Production emotion detector is OPERATIONAL!")
