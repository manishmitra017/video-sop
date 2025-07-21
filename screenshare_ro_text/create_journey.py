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
            full_text += f"## Frame: {file}\n{f.read()}\n\n"
            
    # Prepare the prompt for the final synthesis
    synthesis_prompt = f"""
    The following is a series of descriptions from individual frames of a screen recording.
    Please synthesize these descriptions into a single, coherent, step-by-step user journey.
    Focus on creating a clear narrative that explains what the user was trying to accomplish.
    Format the output as a clean, easy-to-read Markdown document.

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
        
        # Save the final journey to the specified output file
        with open(output_file, "w") as f:
            f.write(final_journey)
            
        print(f"\n--- Successfully generated final journey! ---")
        print(f"Saved to: {output_file}")

    except Exception as e:
        print(f"\n--- An error occurred during final synthesis ---")
        print(e)

if __name__ == "__main__":
    analysis_directory = "analysis_results"
    final_output_file = "final_user_journey.md"
    generate_final_journey(analysis_directory, final_output_file)