import base64
import os
import sys
import litellm
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
litellm.api_key = os.getenv("GOOGLE_API_KEY")

def analyze_and_append_chunk(image_paths: list[str], journey_file_path: str, chunk_name: str):
    """
    Analyzes a chunk of images and appends the detailed analysis to the journey file.
    """
    print(f"--- Analyzing chunk: {chunk_name} ---")
    
    messages = [
        {
            "role": "user", 
            "content": [
                {"type": "text", "text": """
                    Analyze the user's actions across these consecutive frames from a screen recording with extreme detail.
                    Your output will be used by another AI, so precision is critical.
                    
                    For each step, provide the following in Markdown format:
                    1.  **Action:** A detailed, step-by-step description of the user's action (e.g., "Clicked the 'Search' button," "Typed 'hello world' into the search bar").
                    2.  **URL:** The full, exact URL visible in the address bar.
                    3.  **Visible Text:** A verbatim copy of all text visible on the screen.
                    
                    Describe the changes between the frames to create a narrative of the user's journey. Do not summarize or make assumptions.
                    """
                }
            ]
        }
    ]

    for image_path in image_paths:
        if not os.path.isfile(image_path):
            print(f"Error: File not found at {image_path}")
            continue
        try:
            with open(image_path, "rb") as f:
                base64_frame = base64.b64encode(f.read()).decode("utf-8")
            messages[0]["content"].append(
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_frame}"}}
            )
        except Exception as e:
            print(f"An error occurred while processing {os.path.basename(image_path)}: {e}")
            return

    if len(messages[0]["content"]) <= 1:
        print("No images to analyze.")
        return

    try:
        vision_model = "gemini/gemini-1.5-pro-latest" # Using a more powerful model for better text extraction
        response = litellm.completion(model=vision_model, messages=messages)
        description = response.choices[0].message.content

        with open(journey_file_path, "a") as f:
            f.write(f"## Step: {chunk_name}\n\n")
            f.write(description)
            f.write("\n\n---\n\n")
        print(f"Appended analysis to: {journey_file_path}")

    except Exception as e:
        print(f"An error occurred during analysis for chunk {chunk_name}: {e}")

def process_all_frames_in_chunks(frames_dir: str, journey_file_path: str, window_size: int = 2, stride: int = 1):
    """
    Processes all JPG frames in a directory in overlapping chunks and saves the analysis.
    """
    print(f"\n--- Starting batch analysis for directory: {frames_dir} ---")
    
    frame_files = sorted([f for f in os.listdir(frames_dir) if f.lower().endswith(".jpg")])
    if not frame_files:
        print("No JPG frames found to analyze.")
        return
        
    for i in range(0, len(frame_files) - window_size + 1, stride):
        chunk_files = frame_files[i:i+window_size]
        image_paths = [os.path.join(frames_dir, f) for f in chunk_files]
        chunk_name = f"chunk_{i:04d}_{os.path.splitext(chunk_files[0])[0]}_to_{os.path.splitext(chunk_files[-1])[0]}"
        analyze_and_append_chunk(image_paths, journey_file_path, chunk_name)
        
    print("\n--- Batch analysis complete. ---")

if __name__ == "__main__":
    frames_base_dir = "frames"
    subdirectories = [d for d in os.listdir(frames_base_dir) if os.path.isdir(os.path.join(frames_base_dir, d))]
    
    if not subdirectories:
        print("No frame directories found.")
        sys.exit(1)
        
    frames_directory = os.path.join(frames_base_dir, subdirectories[0])
    
    # Read the video name from the metadata file
    try:
        with open(os.path.join("analysis_results", "metadata", "video_name.txt"), "r") as f:
            video_name = f.read().strip()
    except FileNotFoundError:
        print("Error: video_name.txt not found. Please run the extract_frames and create_journey scripts first.")
        sys.exit(1)

    journeys_dir = "journeys"
    final_output_file = os.path.join(journeys_dir, f"{video_name}_journey.md")

    process_all_frames_in_chunks(frames_directory, final_output_file)