#!/bin/bash

# This script sets up a venv and runs both fetch scripts.
# Safe for GitHub (no API keys committed).

BASE_DIR="/home/ubuntu/cron_assignment"
VENV_DIR="${BASE_DIR}/venv"

# Load API key from environment (not stored in GitHub)
export OPENWEATHER_API_KEY="YOUR_API_KEY_HERE"

# Create venv if missing
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Install dependencies
pip install --upgrade pip
pip install -r "${BASE_DIR}/requirements.txt"

# Run weather fetch
echo "Running weather fetch..."
python3 "${BASE_DIR}/fetch_weather.py"

# Run exchange rate fetch
echo "Running exchange rate fetch..."
python3 "${BASE_DIR}/fetch_exchange.py"

echo "Done!"