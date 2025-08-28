# -*- coding: utf-8 -*-

# import modules
import os
import glob
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_keyframes_sync(output_dir, max_workers=3):
    """Synchronous keyframes extraction - no async conflicts"""
    # Build keyframes path
    keyframes_path = f'{output_dir}/keyframes'
    if not os.path.exists(keyframes_path):
        os.makedirs(keyframes_path)

    # Get all video files
    video_path = f'{output_dir}/downloaded_videos'
    if not os.path.exists(video_path):
        return
    
    files = glob.glob(f'{video_path}/*.mp4')
    if not files:
        return

    # Videos already processed
    processed_videos = []
    if os.path.exists(keyframes_path):
        processed_videos = [d for d in os.listdir(keyframes_path) 
                          if os.path.isdir(os.path.join(keyframes_path, d))]

    def extract_single_video_keyframes(file):
        """Extract keyframes from a single video file"""
        try:
            # Get id from video filename
            video_id = os.path.basename(file).split('.')[0]
            if video_id in processed_videos:
                return
            
            # Create subdirectory for this video_id
            video_keyframes_dir = f'{keyframes_path}/{video_id}'
            if not os.path.exists(video_keyframes_dir):
                os.makedirs(video_keyframes_dir)
            
            # FFmpeg command to extract keyframes
            cmd = [
                'ffmpeg',
                '-i', file,
                '-vf', 'select=eq(pict_type\\,I)',
                '-vsync', 'vfr',
                '-q:v', '2',
                '-y',  # Overwrite output files
                f'{video_keyframes_dir}/keyframe_%04d.jpg'
            ]

            # Run FFmpeg synchronously
            subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
                
        except Exception:
            # Silently handle errors
            pass

    # Process videos with controlled concurrency
    max_workers = min(max_workers, len(files))
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_file = {executor.submit(extract_single_video_keyframes, file): file 
                        for file in files}
        
        # Process completed tasks silently
        for future in as_completed(future_to_file):
            result = future.result()
            # Silently handle results - no UI spam
            pass