import os
import sys

def initialize_journey_file(output_file: str, video_name: str):
    """
    Creates and initializes the final journey markdown file with a title.
    """
    print(f"--- Initializing journey file: {output_file} ---")
    
    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Create the file and write the title
        with open(output_file, "w") as f:
            f.write(f"# User Journey: {video_name}\n\n")
            
        print(f"--- Successfully initialized journey file! ---")

    except Exception as e:
        print(f"\n--- An error occurred during file initialization ---")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    analysis_results_dir = "analysis_results"
    
    # Read the video name from the metadata file
    try:
        with open(os.path.join(analysis_results_dir, "metadata", "video_name.txt"), "r") as f:
            video_name = f.read().strip()
    except FileNotFoundError:
        print("Error: video_name.txt not found. Please run the extract_frames script first.")
        sys.exit(1)

    journeys_dir = "journeys"
    final_output_file = os.path.join(journeys_dir, f"{video_name}_journey.md")
    
    initialize_journey_file(final_output_file, video_name)

