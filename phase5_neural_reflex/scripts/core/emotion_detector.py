import os
import numpy as np
import tensorflow as tf
import librosa
import time

class EmotionDetector:
    def __init__(self, model_path="../models/model_int8.tflite"):
        self.model_path = model_path
        # Map 10 output classes to emotions (adjust based on your model training)
        self.emotions = ['neutral', 'calm', 'happy', 'sad', 'angry', 'fearful', 'disgust', 'surprised', 'boredom', 'excited']
        self.load_model()
        
    def load_model(self):
        """Load TFLite model for emotion detection"""
        try:
            self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            print("✅ REAL Emotion model loaded successfully!")
            print(f"📊 Model Input: {self.input_details[0]['dtype']}, Shape: {self.input_details[0]['shape']}")
            print(f"📊 Model Output: {self.output_details[0]['dtype']}, Shape: {self.output_details[0]['shape']}")
            
        except Exception as e:
            print(f"❌ Failed to load emotion model: {e}")
            self.interpreter = None
            
    def extract_mel_spectrogram(self, audio_path, n_mels=40, hop_length=512, n_fft=2048):
        """Extract mel-spectrogram features for the model"""
        try:
            # Load audio file
            y, sr = librosa.load(audio_path, sr=22050)
            
            # Extract mel-spectrogram (40 bands, which matches model input)
            mel_spec = librosa.feature.melspectrogram(
                y=y, sr=sr, n_mels=n_mels, hop_length=hop_length, n_fft=n_fft
            )
            
            # Convert to log scale (dB)
            log_mel = librosa.power_to_db(mel_spec, ref=np.max)
            
            # Ensure correct dimensions [40, 99]
            target_frames = 99
            if log_mel.shape[1] > target_frames:
                # Trim to 99 frames
                log_mel = log_mel[:, :target_frames]
            else:
                # Pad to 99 frames
                pad_width = target_frames - log_mel.shape[1]
                log_mel = np.pad(log_mel, ((0, 0), (0, pad_width)), mode='constant')
            
            # Normalize to 0-255 for UINT8
            mel_min = log_mel.min()
            mel_max = log_mel.max()
            if mel_max - mel_min > 0:
                normalized = (log_mel - mel_min) / (mel_max - mel_min) * 255
            else:
                normalized = np.zeros_like(log_mel)
            
            # Convert to UINT8 and reshape for model [1, 40, 99, 1]
            input_data = normalized.astype(np.uint8)
            input_data = input_data.reshape(1, 40, 99, 1)
            
            return input_data, y, sr
            
        except Exception as e:
            print(f"❌ Error extracting features: {e}")
            return None, None, None
    
    def predict_emotion_from_audio(self, audio_path):
        """Predict emotion directly from audio file"""
        if self.interpreter is None:
            return {'emotion': 'neutral', 'confidence': 0.5, 'timestamp': time.time()}
            
        try:
            # Extract features
            input_data, audio, sr = self.extract_mel_spectrogram(audio_path)
            if input_data is None:
                return {'emotion': 'neutral', 'confidence': 0.0, 'timestamp': time.time()}
            
            # Set input tensor
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            
            # Run inference
            self.interpreter.invoke()
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
            
            # Dequantize output (UINT8 to FLOAT32)
            output_quant = self.output_details[0]['quantization']
            if output_quant[0] != 0:  # If quantized
                output_float = output_quant[0] * (output_data.astype(np.float32) - output_quant[1])
            else:
                output_float = output_data.astype(np.float32)
            
            # Process results
            emotion_idx = np.argmax(output_float[0])
            confidence = output_float[0][emotion_idx]
            
            # Apply softmax if needed
            if output_float[0].sum() > 1.5:  # If not already probabilities
                exp_output = np.exp(output_float[0] - np.max(output_float[0]))
                probabilities = exp_output / exp_output.sum()
                confidence = probabilities[emotion_idx]
            
            return {
                'emotion': self.emotions[emotion_idx],
                'confidence': float(confidence),
                'timestamp': time.time(),
                'all_probabilities': output_float[0].tolist(),
                'audio_duration': len(audio)/sr if audio is not None else 0
            }
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return {'emotion': 'neutral', 'confidence': 0.0, 'timestamp': time.time()}
    
    def get_emotional_state(self, emotion):
        """Convert emotion to reflex state"""
        state_map = {
            'neutral': 'calm',
            'calm': 'calm', 
            'happy': 'focused',
            'excited': 'focused',
            'surprised': 'alert',
            'angry': 'alert',
            'fearful': 'alert',
            'sad': 'calm',
            'disgust': 'alert',
            'boredom': 'calm'
        }
        return state_map.get(emotion, 'calm')

# Test the improved detector
if __name__ == "__main__":
    detector = EmotionDetector()
    
    # Test with a sample audio file
    test_file = "../data/emotion_dataset/Audio_Speech_Actors_01-24/Actor_01/03-01-01-01-01-01-01.wav"
    
    if os.path.exists(test_file):
        print("🧪 TESTING REAL AUDIO EMOTION DETECTION")
        result = detector.predict_emotion_from_audio(test_file)
        print(f"🎵 File: {os.path.basename(test_file)}")
        print(f"🎭 Predicted Emotion: {result['emotion']}")
        print(f"📊 Confidence: {result['confidence']:.3f}")
        print(f"⏱️ Duration: {result['audio_duration']:.2f}s")
        print(f"🔄 Reflex State: {detector.get_emotional_state(result['emotion'])}")
    else:
        print("❌ Test file not found")
