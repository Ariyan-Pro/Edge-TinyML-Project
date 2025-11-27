# phase1_baseline/scripts/prepare_audio.py
import os
import librosa
import numpy as np
from pathlib import Path
import soundfile as sf
from tqdm import tqdm
import argparse
import logging
import sys
from typing import List, Tuple, Optional, Dict, Any

# Import configuration
sys.path.append(str(Path(__file__).parent.parent))
from config import CONFIG

# Setup advanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(CONFIG.paths.logs_dir / 'audio_preprocessing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdvancedAudioProcessor:
    """Genius-level audio processor with comprehensive features"""
    
    def __init__(self, config=CONFIG.audio):
        self.config = config
        self.supported_formats = {'.wav', '.mp3', '.flac', '.m4a'}
        self.processing_stats = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'errors': []
        }
    
    def analyze_audio_file(self, file_path: Path) -> Dict[str, Any]:
        """Comprehensive audio file analysis"""
        try:
            audio, sr = librosa.load(str(file_path), sr=None)
            duration = len(audio) / sr
            rms_energy = np.sqrt(np.mean(audio**2))
            
            return {
                'original_sample_rate': sr,
                'duration': duration,
                'rms_energy': rms_energy,
                'max_amplitude': np.max(np.abs(audio)),
                'is_valid': duration >= 0.5  # Minimum duration check
            }
        except Exception as e:
            logger.warning(f"Analysis failed for {file_path}: {str(e)}")
            return {'is_valid': False, 'error': str(e)}
    
    def adaptive_audio_loading(self, file_path: Path) -> Optional[Tuple[np.ndarray, int]]:
        """Intelligent audio loading with format detection"""
        try:
            analysis = self.analyze_audio_file(file_path)
            
            if not analysis['is_valid']:
                logger.warning(f"Invalid audio file: {file_path}")
                return None
            
            # Load with target sample rate
            audio, sr = librosa.load(str(file_path), sr=self.config.sample_rate)
            
            # Normalize audio levels
            audio = self.normalize_audio(audio)
            
            logger.debug(f"Successfully loaded: {file_path} (duration: {len(audio)/sr:.2f}s)")
            return audio, sr
            
        except Exception as e:
            logger.error(f"Failed to load {file_path}: {str(e)}")
            self.processing_stats['errors'].append(str(e))
            return None
    
    def normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        """Audio normalization with peak detection"""
        peak = np.max(np.abs(audio))
        if peak > 0:
            return audio / peak * 0.9  # Leave some headroom
        return audio
    
    def compute_robust_melspectrogram(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """Advanced mel spectrogram computation with noise robustness"""
        try:
            # Advanced preprocessing chain
            audio_trimmed, _ = librosa.effects.trim(audio, top_db=25)
            
            # Compute mel spectrogram with advanced parameters
            mel_spec = librosa.feature.melspectrogram(
                y=audio_trimmed,
                sr=sr,
                n_mels=self.config.n_mels,
                n_fft=self.config.n_fft,
                hop_length=self.config.hop_length,
                fmin=50,  # Remove very low frequencies
                fmax=8000,  # Focus on speech frequencies
                power=2
            )
            
            # Log scaling with noise floor
            log_mel = librosa.power_to_db(mel_spec, ref=np.max, amin=1e-10)
            
            return log_mel.astype(np.float32)
            
        except Exception as e:
            logger.error(f"Spectrogram computation failed: {str(e)}")
            raise
    
    def intelligent_shape_normalization(self, spectrogram: np.ndarray) -> np.ndarray:
        """Advanced shape normalization with content preservation"""
        n_mels, n_frames = spectrogram.shape
        
        if n_frames < self.config.max_frames:
            # Smart padding with reflection and fade
            pad_width = self.config.max_frames - n_frames
            left_pad = pad_width // 2
            right_pad = pad_width - left_pad
            
            spectrogram = np.pad(
                spectrogram,
                ((0, 0), (left_pad, right_pad)),
                mode='reflect'
            )
            
        elif n_frames > self.config.max_frames:
            # Center cropping for important content
            start = (n_frames - self.config.max_frames) // 2
            spectrogram = spectrogram[:, start:start + self.config.max_frames]
        
        return spectrogram
    
    def process_file_with_quality_check(self, input_path: Path, output_path: Path) -> bool:
        """Process file with comprehensive quality checks"""
        self.processing_stats['total_files'] += 1
        
        try:
            # Load and validate audio
            audio_data = self.adaptive_audio_loading(input_path)
            if audio_data is None:
                self.processing_stats['failed'] += 1
                return False
            
            audio, sr = audio_data
            
            # Compute features
            mel_spec = self.compute_robust_melspectrogram(audio, sr)
            
            # Normalize shape
            mel_spec_normalized = self.intelligent_shape_normalization(mel_spec)
            
            # Quality check: ensure no NaN or Inf values
            if not np.isfinite(mel_spec_normalized).all():
                logger.warning(f"Invalid values in spectrogram: {input_path}")
                self.processing_stats['failed'] += 1
                return False
            
            # Save with compression
            output_path.parent.mkdir(parents=True, exist_ok=True)
            np.save(output_path, mel_spec_normalized)
            
            self.processing_stats['successful'] += 1
            return True
            
        except Exception as e:
            logger.error(f"Processing failed for {input_path}: {str(e)}")
            self.processing_stats['failed'] += 1
            self.processing_stats['errors'].append(f"{input_path}: {str(e)}")
            return False
    
    def process_dataset(self, input_dir: Path, output_dir: Path) -> Dict[str, Any]:
        """Process entire dataset with comprehensive reporting"""
        logger.info(f"🎯 Starting Genius-Level Audio Processing")
        logger.info(f"Input: {input_dir} -> Output: {output_dir}")
        
        # Find all supported audio files
        audio_files = []
        for fmt in self.supported_formats:
            audio_files.extend(input_dir.rglob(f"*{fmt}"))
        
        logger.info(f"📊 Found {len(audio_files)} audio files")
        
        # Filter by target classes if specified
        if hasattr(self.config, 'target_classes'):
            filtered_files = []
            for file_path in audio_files:
                if any(cls in str(file_path.parent) for cls in self.config.target_classes):
                    filtered_files.append(file_path)
            audio_files = filtered_files
            logger.info(f"🎯 Filtered to {len(audio_files)} files in target classes: {self.config.target_classes}")
        
        # Process with comprehensive progress tracking
        with tqdm(total=len(audio_files), desc="🔄 Processing Audio", unit="file") as pbar:
            for audio_file in audio_files:
                relative_path = audio_file.relative_to(input_dir)
                output_path = output_dir / relative_path.with_suffix('.npy')
                
                self.process_file_with_quality_check(audio_file, output_path)
                pbar.update(1)
        
        # Generate comprehensive report
        success_rate = (self.processing_stats['successful'] / self.processing_stats['total_files']) * 100
        logger.info(f"✅ Processing complete: {success_rate:.2f}% success rate")
        logger.info(f"📈 Successful: {self.processing_stats['successful']}, Failed: {self.processing_stats['failed']}")
        
        return self.processing_stats

def main():
    parser = argparse.ArgumentParser(description="🎯 Genius-Level Audio Preprocessor")
    parser.add_argument("--input", type=str, default=str(CONFIG.paths.data_raw),
                       help="Input directory with raw audio")
    parser.add_argument("--output", type=str, default=str(CONFIG.paths.data_processed),
                       help="Output directory for processed data")
    parser.add_argument("--verbose", action="store_true",
                       help="Enable verbose debug logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    processor = AdvancedAudioProcessor()
    stats = processor.process_dataset(Path(args.input), Path(args.output))
    
    # Save processing statistics
    stats_path = CONFIG.paths.artifacts_dir / "preprocessing_stats.json"
    import json
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n🎉 AUDIO PREPROCESSING COMPLETE!")
    print(f"📊 Success Rate: {(stats['successful']/stats['total_files'])*100:.2f}%")
    print(f"💾 Processed files saved to: {args.output}")
    print(f"📈 Statistics saved to: {stats_path}")

if __name__ == "__main__":
    main()