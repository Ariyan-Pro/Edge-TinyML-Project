# phase1_baseline/config.py
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any
import json

@dataclass
class AudioConfig:
    """Intelligent audio processing configuration"""
    sample_rate: int = 16000
    n_mels: int = 40
    n_fft: int = 512
    hop_length: int = 160
    max_frames: int = 99
    duration: float = 1.0
    target_classes: List[str] = field(default_factory=lambda: [
        'yes', 'no', 'up', 'down', 'left', 'right', 'on', 'off', 'stop', 'go'
    ])
    
@dataclass
class ModelConfig:
    """Advanced model configuration with flexibility"""
    input_shape: tuple = (40, 99, 1)
    conv_filters: List[int] = field(default_factory=lambda: [32, 64, 128])
    dense_units: List[int] = field(default_factory=lambda: [256, 128])
    dropout_rates: List[float] = field(default_factory=lambda: [0.3, 0.4, 0.5])
    learning_rate: float = 0.001
    batch_size: int = 64
    epochs: int = 50
    early_stopping_patience: int = 10
    lr_reduction_patience: int = 5

@dataclass
class TFLiteConfig:
    """TFLite conversion and optimization configuration"""
    enable_dynamic_range: bool = True
    enable_int8_quantization: bool = True
    representative_samples: int = 200

@dataclass
class PathConfig:
    """Comprehensive path management"""
    project_root: Path = Path("C:/Users/dell/Projects/Edge-TinyML-Project")
    
    @property
    def phase1_root(self) -> Path:
        return self.project_root / "phase1_baseline"
    
    @property
    def data_raw(self) -> Path:
        return self.phase1_root / "data" / "raw"
    
    @property
    def data_processed(self) -> Path:
        return self.phase1_root / "data" / "processed"
    
    @property
    def models_dir(self) -> Path:
        return self.phase1_root / "models"
    
    @property
    def scripts_dir(self) -> Path:
        return self.phase1_root / "scripts"
    
    @property
    def notebooks_dir(self) -> Path:
        return self.phase1_root / "notebooks"
    
    @property
    def logs_dir(self) -> Path:
        return self.phase1_root / "logs"
    
    @property
    def artifacts_dir(self) -> Path:
        return self.phase1_root / "artifacts"

@dataclass
class ExperimentConfig:
    """Complete experiment configuration"""
    audio: AudioConfig = field(default_factory=AudioConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    tflite: TFLiteConfig = field(default_factory=TFLiteConfig)
    paths: PathConfig = field(default_factory=PathConfig)
    
    def ensure_directories(self):
        """Create all necessary directories"""
        directories = [
            self.paths.data_raw, self.paths.data_processed,
            self.paths.models_dir, self.paths.logs_dir,
            self.paths.artifacts_dir
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"Created: {directory}")

# Global configuration instance
CONFIG = ExperimentConfig()
CONFIG.ensure_directories()

print("Genius-Level Configuration Loaded!")
print(f"Project root: {CONFIG.paths.project_root}")