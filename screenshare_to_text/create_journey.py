import os
import sys
import litellm
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
litellm.api_key = os.getenv("GOOGLE_API_KEY")

def generate_final_journey(analysis_dir: str, output_file: str):
    """
    Reads all analysis files, synthesizes them into a coherent journey,
    and saves the result to a markdown file.
    """
    print(f"--- Creating final journey from analyses in: {analysis_dir} ---")
    
    if not os.path.isdir(analysis_dir):
        print(f"Error: Analysis directory not found at {analysis_dir}")
        sys.exit(1)

    # Read all the individual analysis files
    analysis_files = sorted([f for f in os.listdir(analysis_dir) if f.endswith(".txt")])
    if not analysis_files:
        print("No analysis files found to process.")
        return
        
    full_text = ""
    for file in analysis_files:
        with open(os.path.join(analysis_dir, file), "r") as f:
            full_text += f"## Chunk: {file}\n{f.read()}\n\n"
            
    # Prepare the prompt for the final synthesis
    synthesis_prompt = f"""
    The following is a series of detailed descriptions of a user's actions, captured from consecutive, overlapping frames of a screen recording.
    Please synthesize these descriptions into a single, coherent, and highly detailed step-by-step user journey.
    The final output must be a clear narrative that explains precisely what the user was trying to accomplish, including any URLs they visited, text they entered, and buttons they clicked.
    This document will be used by another AI system and a human, so it must be unambiguous and easy to follow.
    Format the output as a clean, well-structured Markdown document.

    ---
    {full_text}
    ---
    """

    messages = [{"role": "user", "content": synthesis_prompt}]
    
    try:
        synthesis_model = "gemini/gemini-1.5-pro-latest"
        print(f"Using synthesis model: {synthesis_model}")
        
        response = litellm.completion(model=synthesis_model, messages=messages)
        final_journey = response.choices[0].message.content
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Save the final journey to the specified output file
        with open(output_file, "w") as f:
            f.write(final_journey)
            
        print(f"\n--- Successfully generated final journey! ---")
        print(f"Saved to: {output_file}")

    except Exception as e:
        print(f"\n--- An error occurred during final synthesis ---")
        print(e)

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
    
    generate_final_journey(analysis_results_dir, final_output_file)
