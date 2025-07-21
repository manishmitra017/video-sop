#!/bin/bash

# This script runs the full video-to-journey pipeline.

# Ensure the virtual environment is activated
source .venv/bin/activate

echo "--- Cleaning up old results ---"
rm -rf analysis_results frames journeys
mkdir -p analysis_results frames journeys

echo "\n--- Installing Dependencies ---"
uv pip install -e .

echo "
--- Step 1: Extracting Frames ---"
python -m screenshare_to_text.extract_frames

echo "
--- Step 2: Initializing Journey File ---"
python -m screenshare_to_text.create_journey

echo "
--- Step 3: Analyzing Frames and Appending to Journey ---"
python -m screenshare_to_text.analyze_frames

echo "
--- Step 4: Generating Final Summary ---"
python -m screenshare_to_text.generate_summary


echo "\n--- Pipeline Complete ---"