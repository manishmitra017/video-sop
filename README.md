# Screen Recording to Detailed User Journey

This project transforms a screen recording video into a detailed, step-by-step user journey documented in Markdown. It leverages a multimodal large language model to analyze the video frames and generate a comprehensive narrative of the user's actions.

## How it Works

The pipeline automates the entire process of converting a video into a user journey:

1.  **Frame Extraction:** The script first extracts frames from the input video at a regular interval (e.g., every 2 seconds).
2.  **Incremental Journey Creation:** It then analyzes these frames in overlapping chunks (e.g., frames 1-2, 2-3, 3-4). For each chunk, a multimodal LLM generates a highly detailed description of the user's actions, including clicks, typing, URL navigation, and all visible on-screen text. This detailed log is appended incrementally to a `_journey.md` file.
3.  **Summary Generation:** After the detailed journey is complete, a final script reads the entire log and uses an LLM to synthesize a concise, human-readable summary of the key actions and their corresponding URLs.

This process results in two distinct output files, one optimized for machine processing and the other for human review.

## How to Run

### Prerequisites

*   Python 3.10 or higher
*   `uv` installed (`pip install uv`)

### Setup and Execution

1.  **Set API Key:**
    *   Create a file named `.env` in the root of the project.
    *   Add your Google API key to the file like this:
        ```
        GOOGLE_API_KEY="your_google_api_key_here"
        ```

2.  **Add Video:**
    *   Place your screen recording video file (e.g., `.mp4`, `.mov`) into the `videos/` directory. The script will automatically process the first video it finds in this folder.

3.  **Run the Pipeline:**
    *   Execute the `run_all.sh` script from the project's root directory:
        ```bash
        ./run_all.sh
        ```

### Output

Upon completion, you will find two Markdown files in the `journeys/` directory, both named after the original video:

*   `your_video_name_journey.md`: An extremely detailed, step-by-step log of every action, including all visible on-screen text. This file is designed to be processed by another AI.
*   `your_video_name_summary.md`: A concise, human-readable summary of the user's key actions, with the corresponding URL for each step.