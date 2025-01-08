#!/usr/bin/env python3
import os
import random
import sys
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.Crop import Crop

def extract_snippets(input_video_path, output_folder, aspect_ratio, snippet_count=3):
    """
    Extract random snippets from the input video and save them in the specified aspect ratio.

    Args:
        input_video_path (str): Path to the input video file.
        output_folder (str): Folder to save the output snippets.
        aspect_ratio (tuple): Desired aspect ratio (width, height).
        snippet_count (int): Number of snippets to extract.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the input video
    video = VideoFileClip(input_video_path)
    video_duration = video.duration
    video_width, video_height = video.size

    # Generate random snippets
    for i in range(1, snippet_count + 1):
        snippet_duration = random.randint(10, 20)  # Random duration between 10-20 seconds
        start_time = random.uniform(0, max(0, video_duration - snippet_duration))

        # Extract the snippet
        snippet = video.subclip(start_time, start_time + snippet_duration) if hasattr(video, 'subclip') else video.subclipped(start_time, start_time + snippet_duration)

        # Determine cropping dimensions
        target_width = video_height * aspect_ratio[0] / aspect_ratio[1]
        target_height = video_width * aspect_ratio[1] / aspect_ratio[0]

        # Modify the cropping section:
        if target_width <= video_width:
            crop_x1 = int((video_width - target_width) / 2) // 2 * 2
            crop_x2 = crop_x1 + (int(target_width) // 2 * 2)
            crop_y1, crop_y2 = 0, video_height
        else:
            crop_y1 = int((video_height - target_height) / 2) // 2 * 2
            crop_y2 = crop_y1 + (int(target_height) // 2 * 2)
            crop_x1, crop_x2 = 0, video_width

        # Apply cropping
        snippet = Crop(x1=crop_x1, y1=crop_y1, x2=crop_x2, y2=crop_y2).apply(snippet)

        # Construct output file name
        base_name = os.path.splitext(os.path.basename(input_video_path))[0]
        aspect_ratio_str = f"{aspect_ratio[0]}x{aspect_ratio[1]}"
        output_file_name = f"{base_name}__{aspect_ratio_str}__{i:02d}.mov"
        output_file_path = os.path.join(output_folder, output_file_name)

        # Write the output video in .mov format
        snippet.write_videofile(
            output_file_path,
            codec="libx264",
            audio_codec="aac",
            preset="medium",
            ffmpeg_params=["-pix_fmt", "yuv420p"]
        )

    video.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./story-maker.py <input_video>")
        sys.exit(1)

    input_video = sys.argv[1]
    output_dir = "output_videos"
    desired_aspect_ratio = (9, 16)  # Aspect ratio for all outputs

    extract_snippets(input_video, output_dir, desired_aspect_ratio)
