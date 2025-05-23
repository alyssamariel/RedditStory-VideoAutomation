from moviepy.editor import *
import os
from PIL import Image, ImageDraw
import numpy as np

def generate_title_video(title_image_path, title_audio_path):
    audio_clip = AudioFileClip(str(title_audio_path)) 
    video_path = (os.path.splitext(title_image_path)[0] + ".mp4")

    # settings
    scale_duration = audio_clip.duration 
    fade_duration = 0.25
    corner_radius = 30
    total_duration = scale_duration + fade_duration

    # imageclip title
    clip = CompositeVideoClip([ImageClip(str(title_image_path)).set_duration(total_duration)])
    clip.write_videofile(str(video_path), fps=24)

    # add the title audio in the title image
    title_clip = VideoFileClip(str(video_path))
    title_clip = title_clip.set_audio(audio_clip)

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

    return title_clip

def compile_final_video(file_name, video_background, title_clip, text_clips, all_comments_path):
    comments_audio = AudioFileClip(str(all_comments_path)).set_start(title_clip.duration)
    
    # combine the audio and video of the title and comments
    final_video = CompositeVideoClip([video_background, title_clip] + text_clips)
    final_audio = CompositeAudioClip([title_clip.audio, comments_audio])

    # set audio and duration and render
    final_video = final_video.set_audio(final_audio).set_duration(max(final_video.duration, title_clip.duration + comments_audio.duration))
    final_video.write_videofile((file_name + ".mp4"), fps=24)
