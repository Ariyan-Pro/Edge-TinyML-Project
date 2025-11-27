#!/bin/bash
echo "📱 Edge TinyML - Termux Setup"
echo "=============================="

# Update packages
pkg update -y && pkg upgrade -y

# Install required packages
pkg install -y python git termux-api

# Install Python packages
pip install requests flask

# Create project directory
mkdir -p ~/edge-tinyml
cd ~/edge-tinyml

echo "✅ Termux setup complete!"
echo "🎯 Next: Enable Termux API in Android settings"
echo "🔧 Allow Termux accessibility permissions"

# Test Termux API
echo "Testing Termux API..."
termux-battery-status

echo "Setup complete! Your Android device is now Edge-TinyML ready!"
