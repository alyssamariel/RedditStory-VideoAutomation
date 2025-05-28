import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips

def get_random_video_path(folder):
    videos = [os.path.join(folder, f) for f in os.listdir(folder)
              if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
    if not videos:
        raise ValueError("No video files found in the folder.")
    return random.choice(videos)

def get_random_clip(folder, duration):
    while True:
        path = get_random_video_path(folder)
        try:
            clip = VideoFileClip(path)
            if clip.duration > duration:
                start = random.uniform(0, clip.duration - duration)
                return clip.subclip(start, start + duration)
            else:
                print(f"Skipping short video: {path}")
        except Exception as e:
            print(f"Error loading video {path}: {e}")

def create_mixed_video(folder, clip_duration, total_duration):
    clips = []
    for _ in range(total_duration // clip_duration):
        clip = get_random_clip(folder, clip_duration)
        clips.append(clip)
    final_clip = concatenate_videoclips(clips, method="compose")
    return final_clip


