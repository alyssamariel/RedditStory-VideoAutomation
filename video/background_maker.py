import random
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
from pathlib import Path


VIDEO_FOLDER = video_folders = [Path("..") / "background" / name for name in ["battery", "jelly", "ladder", "roof"]]
  # Change this to your video folder
CLIP_DURATION = 15                   # seconds per video segment
TOTAL_DURATION = 60 

def get_random_clip(folder, duration, speed=1.25):
    # filter videos longer than duration
    valid_videos = []
    for path in folder.iterdir():
        if path.suffix.lower() in ('.mp4', '.mov', '.avi', '.mkv'):
            try:
                clip = VideoFileClip(str(path))
                clip.fx(vfx.speedx, factor=int(speed))
                if clip.duration > duration:
                    valid_videos.append(path)
                clip.close()
            except Exception:
                continue

    if not valid_videos:
        raise ValueError(f"No suitable video longer than {duration}s in folder {folder}")

    # pick a random clip
    clip = VideoFileClip(str(random.choice(valid_videos)))

    # pick subclip after resizing/cropping
    start = random.uniform(0, clip.duration - duration)
    return clip.subclip(start, start + duration)


# select random folder that's not consecutive
def pick_folder(folder_pool, all_folders, last_folder):
    # if folder pool is empty, replenish
    if not folder_pool:
        folder_pool = all_folders.copy()

    # avoid consecutive folders
    filtered_pool = [f for f in folder_pool if f != last_folder]
    if not filtered_pool:
        filtered_pool = [f for f in all_folders if f != last_folder]

    # pick a folder, then remove the folder in the folder pool
    chosen_folder = random.choice(filtered_pool)
    if chosen_folder in folder_pool:
        folder_pool.remove(chosen_folder)

    return chosen_folder, folder_pool

# mix all selected videos 
def create_mixed_video(folders, clip_duration, total_duration, speed):
    folder_pool = folders.copy()
    last_folder = None
    clips = []

    # full-length clips
    for _ in range(int(total_duration // clip_duration)):
        chosen_folder, folder_pool = pick_folder(folder_pool, folders, last_folder)
        clip = get_random_clip(chosen_folder, clip_duration, speed)
        clips.append(clip)
        last_folder = chosen_folder

    # remainder clip (if any)
    remainder = total_duration % clip_duration
    if remainder > 0:
        chosen_folder, _ = pick_folder(folder_pool, folders, last_folder)
        clip = get_random_clip(chosen_folder, remainder, speed)
        clips.append(clip)

    return concatenate_videoclips(clips, method="compose")


