import os
import sys
import litellm
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
litellm.api_key = os.getenv("GOOGLE_API_KEY")

def generate_summary(detailed_journey_path: str, summary_output_path: str):
    """
    Reads a detailed journey file and synthesizes it into a concise summary.
    """
    print(f"--- Creating summary from: {detailed_journey_path} ---")
    
    try:
        with open(detailed_journey_path, "r") as f:
            detailed_text = f.read()
    except FileNotFoundError:
        print(f"Error: Detailed journey file not found at {detailed_journey_path}")
        sys.exit(1)

    # Prepare the prompt for the summary synthesis
    synthesis_prompt = f"""
    The following is a highly detailed, step-by-step log of a user's actions from a screen recording, including full URLs and all visible text.
    Please synthesize this log into a simple, concise, and easy-to-read numbered list of the user's key actions.
    For each step, include the action taken and the full URL where the action occurred.
    Focus on the most significant steps the user took to achieve their goal.
    The output should be a clean Markdown document, suitable for a human to quickly understand the user's journey.

    ---
    {detailed_text}
    ---
    """

    messages = [{"role": "user", "content": synthesis_prompt}]
    
    try:
        synthesis_model = "gemini/gemini-1.5-pro-latest"
        print(f"Using synthesis model: {synthesis_model}")
        
        response = litellm.completion(model=synthesis_model, messages=messages)
        final_summary = response.choices[0].message.content
        
        # Save the final summary to the specified output file
        with open(summary_output_path, "w") as f:
            f.write(final_summary)
            
        print(f"\n--- Successfully generated summary! ---")
        print(f"Saved to: {summary_output_path}")

    except Exception as e:
        print(f"\n--- An error occurred during summary synthesis ---")
        print(e)

if __name__ == "__main__":
    # Read the video name from the metadata file
    try:
        with open(os.path.join("analysis_results", "metadata", "video_name.txt"), "r") as f:
            video_name = f.read().strip()
    except FileNotFoundError:
        print("Error: video_name.txt not found. Please run the prerequisite scripts first.")
        sys.exit(1)

    journeys_dir = "journeys"
    detailed_journey_filename = os.path.join(journeys_dir, f"{video_name}_journey.md")
    summary_filename = os.path.join(journeys_dir, f"{video_name}_summary.md")
    
    generate_summary(detailed_journey_filename, summary_filename)
