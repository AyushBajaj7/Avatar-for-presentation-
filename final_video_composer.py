# Final Video Composer with Slide Backgrounds
# Creates the final video with PowerPoint slides as backgrounds and animated avatars

import os
import subprocess
import logging
from pathlib import Path
from typing import List

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def compose_final_video_with_slides():
    """Compose final video with slide backgrounds and animated avatars"""
    print("Creating final video with slide backgrounds...")
    
    # Check if we have the required files
    video_dir = "video"
    slide_dir = "slide_images"
    output_dir = "output"
    
    # Find animated videos
    animated_videos = []
    for file in os.listdir(video_dir):
        if file.endswith("_animated.mp4"):
            animated_videos.append(os.path.join(video_dir, file))
    
    # Find slide images
    slide_images = []
    for file in os.listdir(slide_dir):
        if file.endswith(".png"):
            slide_images.append(os.path.join(slide_dir, file))
    
    print(f"Found {len(animated_videos)} animated videos")
    print(f"Found {len(slide_images)} slide images")
    
    if not animated_videos:
        print("ERROR: No animated videos found")
        return False
    
    if not slide_images:
        print("ERROR: No slide images found")
        return False
    
    # Sort files to match them properly
    animated_videos.sort()
    slide_images.sort()
    
    try:
        # Create temporary directory
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Process each slide
        processed_videos = []
        
        for i, (video_path, slide_path) in enumerate(zip(animated_videos, slide_images)):
            print(f"Processing slide {i+1}...")
            
            if not os.path.exists(video_path) or not os.path.exists(slide_path):
                print(f"WARNING: Missing files for slide {i+1}, skipping")
                continue
            
            # Create a composite video with slide background and avatar
            output_path = os.path.join(temp_dir, f"slide_{i+1:03d}_composite.mp4")
            
            # Use ffmpeg to overlay the animated avatar on the slide image
            # Position avatar in bottom right corner with proper size for lip-sync visibility
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", slide_path,  # Slide image as background
                "-i", video_path,  # Animated avatar video
                "-filter_complex", 
                f"[0:v]scale=1920:1080[bg];[1:v]scale=320:320[avatar];[bg][avatar]overlay=1600:760[out]",  # Smaller avatar, bottom right corner
                "-map", "[out]",
                "-map", "1:a",  # Use audio from avatar video
                "-c:v", "libx264",
                "-c:a", "aac",
                "-shortest",
                output_path
            ]
            
            print(f"  Creating composite video for slide {i+1}...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                processed_videos.append(output_path)
                print(f"  SUCCESS: Created composite video for slide {i+1}")
            else:
                print(f"  ERROR: Failed to create composite video for slide {i+1}")
                print(f"  Error: {result.stderr}")
        
        if not processed_videos:
            print("ERROR: No composite videos created")
            return False
        
        # Concatenate all composite videos
        print("Concatenating all slides...")
        
        # Create file list for ffmpeg
        file_list_path = os.path.join(temp_dir, "video_list.txt")
        with open(file_list_path, 'w') as f:
            for video_path in processed_videos:
                f.write(f"file '{os.path.abspath(video_path)}'\n")
        
        # Concatenate videos
        final_output = os.path.join(output_dir, "final_presentation_with_slides.mp4")
        concat_cmd = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", file_list_path,
            "-c", "copy",
            final_output
        ]
        
        print("Concatenating videos...")
        result = subprocess.run(concat_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"SUCCESS: Final video created: {final_output}")
            return True
        else:
            print(f"ERROR: Failed to concatenate videos: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"ERROR: Video composition failed: {e}")
        return False

def main():
    """Main function"""
    print("Final Video Composer with Slide Backgrounds")
    print("=" * 50)
    
    success = compose_final_video_with_slides()
    
    if success:
        print("\nSUCCESS: Video composition completed!")
        print("Your final video with slide backgrounds is ready!")
        print("Check the output directory for 'final_presentation_with_slides.mp4'")
    else:
        print("\nERROR: Video composition failed!")
        print("Check the error messages above for details.")

if __name__ == "__main__":
    main()
