from moviepy.editor import *
import os
from PIL import Image, ImageDraw
import numpy as np

def generate_reddit_video(folder_path, output_audio, title_image_path):
    audio_clip = AudioFileClip(str(output_audio)) 
    video_path = folder_path / "temp_image.mp4"

    # settings
    final_size = (1080, 1920)
    scale_duration = audio_clip.duration 
    fade_duration = 0.5
    corner_radius = 30
    total_duration = scale_duration + fade_duration

    # imageclip title
    clip = CompositeVideoClip([ImageClip(str(title_image_path)).set_duration(total_duration)])
    clip.write_videofile(str(video_path), fps=24)

    title_clip = VideoFileClip(str(video_path)).without_audio()

    # rounded corners
    def make_rounded_mask(size, radius):
        w, h = size
        mask = Image.new('L', (w, h), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), (w, h)], radius=radius, fill=255)
        return np.array(mask) / 255.0

    mask = make_rounded_mask(title_clip.size, radius=corner_radius)
    title_clip = title_clip.set_mask(ImageClip(mask, ismask=True).set_duration(total_duration))

    # scale animation
    def resize(t):
        if t <= scale_duration:
            start_scale = 0.9
            end_scale = 1.1
            return start_scale + (t / scale_duration) * (end_scale - start_scale)
        else:
            return 1.1

    title_clip = title_clip.resize(lambda t: resize(t))
    title_clip = title_clip.set_position("center")

    # fadeout animation
    title_clip = title_clip.crossfadeout(fade_duration)

    # background video
    background = ColorClip(final_size, color=(255, 255, 255)).set_duration(total_duration)

    # final video
    video = CompositeVideoClip([background, title_clip])
    video = video.set_audio(audio_clip)

    video.write_videofile("final.mp4", fps=24)

    # cleanup
    title_clip.close()
    if os.path.exists(str(video_path)):
        os.remove(str(video_path))
