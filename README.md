# Screen Recording to Detailed User Journey

This project transforms a screen recording video into a detailed, step-by-step user journey documented in Markdown. It leverages a multimodal large language model to analyze the video frames and generate a comprehensive narrative of the user's actions.

## How it Works

The pipeline automates the entire process of converting a video into a user journey:

1.  **Frame Extraction:** The script first extracts frames from the input video at a regular interval (e.g., every 2 seconds).
2.  **Overlapping Frame Analysis:** It then analyzes these frames in overlapping chunks (e.g., frames 1-2, 2-3, 3-4). This sliding window approach provides context and ensures that no user actions are missed between frames. A multimodal LLM describes the user's actions, including clicks, typing, URL navigation, and other interactions in detail for each chunk.
3.  **Journey Synthesis:** Finally, the script synthesizes the descriptions from all chunks into a single, coherent user journey. The output is a well-structured Markdown file that provides a clear, easy-to-follow narrative of the user's on-screen activity.

The final document is designed to be easily understood by both human readers and other AI systems.

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

The script will perform all the necessary steps and, upon completion, you will find the generated user journey in the `journeys/` directory. The output file will be a Markdown file named after the original video (e.g., `journeys/your_video_name_journey.md`).