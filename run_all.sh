#!/bin/bash

# This script runs the full video-to-journey pipeline.

# Ensure the virtual environment is activated
source .venv/bin/activate

echo "--- Cleaning up old results ---"
rm -rf analysis_results frames journeys
mkdir -p analysis_results frames journeys

echo "\n--- Installing Dependencies ---"
uv pip install -e .

echo "\n--- Step 1: Extracting Frames ---"
python -m screenshare_to_text.extract_frames

echo "\n--- Step 2: Analyzing Frames ---"
python -m screenshare_to_text.analyze_frames

echo "\n--- Step 3: Creating Final Journey ---"
python -m screenshare_to_text.create_journey

echo "\n--- Pipeline Complete ---"