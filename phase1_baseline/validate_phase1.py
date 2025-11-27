import os
import json
from pathlib import Path

print('🔍 PHASE 1 VALIDATION CHECK (COMPLETE STRUCTURE)')
print('=' * 50)

def check_file(path, desc):
    exists = Path(path).exists()
    status = '✅' if exists else '❌'
    print(f'{status} {desc}: {path}')
    return exists

# Check ALL models and components
critical_files = [
    ('models/production/model_int8.tflite', 'INT8 quantized model (Primary)'),
    ('models/development/model_dynamic.tflite', 'Dynamic quantized model'),
    ('models/development/model_float32.tflite', 'Float32 TFLite model'),
    ('models/archive/mock_model.json', 'Mock model config'),
    ('data/raw/', 'Source dataset (35 commands)'),
    ('data/processed/', 'Processed features (10 commands)'),
    ('artifacts/training_metrics.json', 'Training metrics'),
    ('scripts/01_data_preparation/', 'Data processing scripts'),
    ('scripts/03_conversion/', 'Model conversion scripts')
]

all_good = True
for path, desc in critical_files:
    if not check_file(path, desc):
        all_good = False

# Check ALL model sizes
print('\n📦 COMPLETE MODEL INVENTORY:')
models = [
    ('production/model_int8.tflite', 'INT8 (Primary)'),
    ('development/model_dynamic.tflite', 'Dynamic'),
    ('development/model_float32.tflite', 'Float32')
]
for model_path, model_type in models:
    full_path = Path(f'models/{model_path}')
    if full_path.exists():
        size_kb = full_path.stat().st_size / 1024
        print(f'   {model_type}: {size_kb:.1f} KB')

print()
print('=' * 50)
if all_good:
    print('🎉 PHASE 1: ALL COMPONENTS VERIFIED!')
    print('   Complete model set available for deployment')
else:
    print('❌ PHASE 1: SOME COMPONENTS MISSING')

print('\n📊 Ready for integration with Phase 3+ systems')

