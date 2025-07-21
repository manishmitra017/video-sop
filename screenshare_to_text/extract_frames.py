import cv2
import os
import sys

def extract_frames_directly(video_path: str, output_dir: str, frame_interval: int = 2):
    """
    Extracts frames from a video using OpenCV directly.
    """
    if not os.path.isfile(video_path):
        print(f"Error: Video file not found at {video_path}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    print(f"--- Extracting frames from '{os.path.basename(video_path)}' to '{output_dir}' ---")

    video_capture = cv2.VideoCapture(video_path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print("Warning: Could not determine video FPS. Defaulting to 30.")
        fps = 30
        
    frame_count = 0
    saved_frame_count = 0

    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break

        if frame_count % (int(fps) * frame_interval) == 0:
            frame_filename = os.path.join(output_dir, f"frame_{saved_frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_frame_count += 1

        frame_count += 1

    video_capture.release()
    print(f"--- Successfully extracted {saved_frame_count} frames. ---")

if __name__ == "__main__":
    videos_dir = "videos"
    video_files = [f for f in os.listdir(videos_dir) if f.endswith((".mp4", ".avi", ".mov", ".mkv"))]
    
    if not video_files:
        print("No video files found in the 'videos' directory.")
        sys.exit(1)
        
    # Process the first video found
    video_file = video_files[0]
    video_path = os.path.join(videos_dir, video_file)
    
    video_name_without_ext = os.path.splitext(video_file)[0]
    output_directory = os.path.join("frames", video_name_without_ext)
    
    extract_frames_directly(video_path, output_directory)