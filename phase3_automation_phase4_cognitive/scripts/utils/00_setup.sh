#!/bin/bash
# Phase 4 Setup Script - Run in Git Bash or WSL on Windows

echo \"🚀 SETTING UP PHASE 4: AUTOMATION & COGNITIVE INTELLIGENCE\"
echo \"===========================================================\"

# Create virtual environment
echo \"�� Creating virtual environment...\"
python -m venv venv
source venv/bin/activate

# Install Python dependencies
echo \"📥 Installing Python dependencies...\"
pip install --upgrade pip
pip install -r requirements.txt

# Download Vosk model (if not already present)
echo \"🎤 Ensuring Vosk model is available...\"
if [ ! -d \"models/vosk-model-small-en-us-0.15\" ]; then
    echo \"Downloading Vosk model...\"
    wget -P models/ https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
    unzip models/vosk-model-small-en-us-0.15.zip -d models/
    mv models/vosk-model-small-en-us-0.15 models/vosk-model
    rm models/vosk-model-small-en-us-0.15.zip
fi

# Initialize database
echo \"🗃️ Initializing cognitive memory database...\"
python scripts/06_memory_manager.py

echo \"✅ SETUP COMPLETE!\"
echo \"💡 Next steps:\"
echo \"   1. Download a GGUF model from Hugging Face\"
echo \"   2. Place it in models/ folder\" 
echo \"   3. Run: python scripts/09_agent_loop.py\"
echo \"   4. Or test individual components\"
