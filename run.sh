#!/bin/bash
# Run script for Optimal Samples Selection System

cd "$(dirname "$0")"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Python3 is required but not installed."
    exit 1
fi

# Install dependencies if needed
pip3 install -r requirements.txt -q

# Run the application
python3 main.py
