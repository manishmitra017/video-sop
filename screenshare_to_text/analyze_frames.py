import base64
import os
import sys
import litellm
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
litellm.api_key = os.getenv("GOOGLE_API_KEY")

def analyze_frame_chunk(image_paths: list[str], output_dir: str, chunk_name: str):
    """
    Analyzes a chunk of images and saves the description to a text file.
    """
    print(f"--- Analyzing chunk: {chunk_name} ---")
    
    messages = [
        {
            "role": "user", 
            "content": [
                {"type": "text", "text": """
                    Analyze the user's actions across these consecutive frames from a screen recording.
                    Provide a detailed, step-by-step description of what the user is doing.
                    Focus on specific actions, such as mouse clicks, typing, scrolling, and navigating to URLs.
                    If a URL is visible, please extract and state it.
                    Describe the changes between the frames to create a narrative of the user's journey.
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
        vision_model = "gemini/gemini-1.5-flash-latest"
        response = litellm.completion(model=vision_model, messages=messages)
        description = response.choices[0].message.content

        output_filename = f"{chunk_name}.txt"
        output_path = os.path.join(output_dir, output_filename)
        with open(output_path, "w") as f:
            f.write(description)
        print(f"Saved analysis to: {output_path}")

    except Exception as e:
        print(f"An error occurred during analysis for chunk {chunk_name}: {e}")

def process_all_frames_in_chunks(frames_dir: str, output_dir: str, window_size: int = 2, stride: int = 1):
    """
    Processes all JPG frames in a directory in overlapping chunks and saves the analysis.
    """
    print(f"\n--- Starting batch analysis for directory: {frames_dir} ---")
    os.makedirs(output_dir, exist_ok=True)
    
    frame_files = sorted([f for f in os.listdir(frames_dir) if f.lower().endswith(".jpg")])
    if not frame_files:
        print("No JPG frames found to analyze.")
        return
        
    for i in range(0, len(frame_files) - window_size + 1, stride):
        chunk_files = frame_files[i:i+window_size]
        image_paths = [os.path.join(frames_dir, f) for f in chunk_files]
        chunk_name = f"chunk_{i:04d}_{os.path.splitext(chunk_files[0])[0]}_to_{os.path.splitext(chunk_files[-1])[0]}"
        analyze_frame_chunk(image_paths, output_dir, chunk_name)
        
    print("\n--- Batch analysis complete. ---")

if __name__ == "__main__":
    frames_base_dir = "frames"
    subdirectories = [d for d in os.listdir(frames_base_dir) if os.path.isdir(os.path.join(frames_base_dir, d))]
    
    if not subdirectories:
        print("No frame directories found.")
        sys.exit(1)
        
    frames_directory = os.path.join(frames_base_dir, subdirectories[0])
    results_directory = "analysis_results"
    process_all_frames_in_chunks(frames_directory, results_directory)