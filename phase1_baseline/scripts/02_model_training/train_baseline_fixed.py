# phase1_baseline/scripts/02_model_training/train_baseline_fixed.py
import numpy as np
from pathlib import Path
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
import argparse
import logging
import sys
from sklearn.model_selection import train_test_split
import json
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent.parent))
from config import CONFIG

# Windows-compatible logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(CONFIG.paths.logs_dir / f'training_fixed_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FixedKWSModel:
    """Fixed model trainer - resolves Path object issues"""
    
    def __init__(self):
        self.model = None
        self.class_names = None
    
    def load_data_subset(self, npy_dir: Path, max_samples_per_class=1000):
        """Load balanced subset of data"""
        
        npy_dir = Path(npy_dir)
        classes = sorted([d.name for d in npy_dir.iterdir() if d.is_dir()])
        self.class_names = classes
        
        logger.info(f"Found {len(classes)} classes: {classes}")
        
        X, y = [], []
        
        for class_idx, class_name in enumerate(classes):
            class_files = list((npy_dir / class_name).glob("*.npy"))
            
            # Take only max_samples_per_class
            selected_files = class_files[:max_samples_per_class]
            logger.info(f"Class {class_name}: using {len(selected_files)}/{len(class_files)} samples")
            
            for file_path in selected_files:
                try:
                    # FIX: Add allow_pickle=True to handle .npy files properly
                    spectrogram = np.load(file_path, allow_pickle=True)
                    X.append(spectrogram)
                    y.append(class_idx)
                except Exception as e:
                    logger.warning(f"Failed to load {file_path}: {str(e)}")
                    continue
        
        X = np.array(X)
        y = np.array(y)
        
        logger.info(f"Loaded subset: {X.shape} features, {y.shape} labels")
        
        # Add channel dimension
        X = X[..., np.newaxis]
        
        return X, y
    
    def build_lightweight_model(self, input_shape, num_classes):
        """Build lightweight CNN"""
        
        inputs = layers.Input(shape=input_shape)
        
        # Compact architecture
        x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Dropout(0.3)(x)
        
        x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D((2, 2))(x)
        x = layers.Dropout(0.4)(x)
        
        x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dropout(0.5)(x)
        
        x = layers.Dense(128, activation='relu')(x)
        x = layers.Dropout(0.5)(x)
        
        outputs = layers.Dense(num_classes, activation='softmax')(x)
        
        model = models.Model(inputs=inputs, outputs=outputs)
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train_fixed(self, npy_dir: Path, output_model_path: Path, epochs=30, max_samples=1000):
        """Fixed training procedure"""
        
        logger.info("Starting Fixed Model Training")
        
        # Load balanced subset
        X, y = self.load_data_subset(npy_dir, max_samples_per_class=max_samples)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        X_train, X_val, y_train, y_val = train_test_split(
            X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
        )
        
        logger.info(f"Dataset splits:")
        logger.info(f"  Train: {X_train.shape} ({len(y_train)} samples)")
        logger.info(f"  Val:   {X_val.shape} ({len(y_val)} samples)")
        logger.info(f"  Test:  {X_test.shape} ({len(y_test)} samples)")
        
        # Build model
        input_shape = X_train.shape[1:]
        self.model = self.build_lightweight_model(input_shape, len(self.class_names))
        
        logger.info("Model Architecture:")
        self.model.summary(print_fn=logger.info)
        
        # FIX: Convert Path to string for ModelCheckpoint
        model_path_str = str(output_model_path)
        
        # Callbacks
        callbacks_list = [
            callbacks.ModelCheckpoint(
                model_path_str,  # FIX: Use string instead of Path object
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),
            callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                verbose=1
            )
        ]
        
        # Train
        logger.info("Starting training...")
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=32,
            callbacks=callbacks_list,
            verbose=1
        )
        
        # Load best model
        self.model = models.load_model(model_path_str)
        
        # Evaluate
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        
        # Save results
        results = {
            'test_accuracy': float(test_accuracy),
            'test_loss': float(test_loss),
            'total_samples': len(X),
            'classes': self.class_names,
            'samples_per_class': max_samples,
            'timestamp': datetime.now().isoformat()
        }
        
        results_path = CONFIG.paths.artifacts_dir / "fixed_training_results.json"
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Training complete! Test accuracy: {test_accuracy:.4f}")
        
        return results

def main():
    parser = argparse.ArgumentParser(description="Fixed KWS Training")
    parser.add_argument("--npy_dir", type=str, default=str(CONFIG.paths.data_processed),
                       help="Directory with processed .npy files")
    parser.add_argument("--output_model", type=str, 
                       default=str(CONFIG.paths.models_dir / "fixed_model.h5"),
                       help="Output model path")
    parser.add_argument("--epochs", type=int, default=30,
                       help="Number of training epochs")
    parser.add_argument("--max_samples", type=int, default=1000,
                       help="Max samples per class")
    
    args = parser.parse_args()
    
    trainer = FixedKWSModel()
    results = trainer.train_fixed(
        Path(args.npy_dir), 
        Path(args.output_model),
        epochs=args.epochs,
        max_samples=args.max_samples
    )
    
    print(f"\nFIXED TRAINING COMPLETE!")
    print(f"Test Accuracy: {results['test_accuracy']:.4f}")
    print(f"Model saved to: {args.output_model}")
    print(f"Using {results['samples_per_class']} samples per class")

if __name__ == "__main__":
    main()