import base64
import os
import sys
import litellm
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
litellm.api_key = os.getenv("GOOGLE_API_KEY")

def analyze_single_frame(image_path: str, output_dir: str):
    """
    Analyzes a single image and saves the description to a text file.
    """
    print(f"--- Analyzing: {os.path.basename(image_path)} ---")
    
    if not os.path.isfile(image_path):
        print(f"Error: File not found at {image_path}")
        return

    try:
        with open(image_path, "rb") as f:
            base64_frame = base64.b64encode(f.read()).decode("utf-8")

        vision_model = "gemini/gemini-1.5-flash-latest"
        messages = [{"role": "user", "content": [
            {"type": "text", "text": "Describe the user's action in this single frame of a screen recording. Focus on the most significant action."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_frame}"}},
        ]}]
        
        response = litellm.completion(model=vision_model, messages=messages)
        description = response.choices[0].message.content

        output_filename = os.path.splitext(os.path.basename(image_path))[0] + ".txt"
        output_path = os.path.join(output_dir, output_filename)
        with open(output_path, "w") as f:
            f.write(description)
        print(f"Saved analysis to: {output_path}")

    except Exception as e:
        print(f"An error occurred while processing {os.path.basename(image_path)}: {e}")

def process_all_frames(frames_dir: str, output_dir: str):
    """
    Processes all JPG frames in a directory and saves the analysis.
    """
    print(f"\n--- Starting batch analysis for directory: {frames_dir} ---")
    os.makedirs(output_dir, exist_ok=True)
    
    frame_files = sorted([f for f in os.listdir(frames_dir) if f.lower().endswith(".jpg")])
    if not frame_files:
        print("No JPG frames found to analyze.")
        return
        
    for frame_file in frame_files:
        image_path = os.path.join(frames_dir, frame_file)
        analyze_single_frame(image_path, output_dir)
        
    print("\n--- Batch analysis complete. ---")

if __name__ == "__main__":
    # Find the first subdirectory in the frames directory
    frames_base_dir = "frames"
    subdirectories = [d for d in os.listdir(frames_base_dir) if os.path.isdir(os.path.join(frames_base_dir, d))]
    
    if not subdirectories:
        print("No frame directories found.")
        sys.exit(1)
        
    frames_directory = os.path.join(frames_base_dir, subdirectories[0])
    results_directory = "analysis_results"
    process_all_frames(frames_directory, results_directory)