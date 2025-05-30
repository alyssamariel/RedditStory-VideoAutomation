from moviepy.editor import *
import os
from PIL import Image, ImageDraw
import numpy as np
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def generate_title_video(title_image_path, title_audio_path, background=(1080, 1920)):
    audio_clip = AudioFileClip(str(title_audio_path)) 
    video_path = (os.path.splitext(title_image_path)[0] + ".mp4")

    # scale settings
    scale_duration = float(config["title"]["scale_duration"])
    start_scale = float(config["title"]["start_scale"])
    end_scale = float(config["title"]["end_scale"])

    # outro animation settings
    outro_duration = float(config["title"]["outro_duration"])
    outro_animation = config["title"]["outro_animation"]

    # other setings
    corner_radius = 30
    total_duration = audio_clip.duration + outro_duration
    video_width = background[0]

    # imageclip title
    clip = CompositeVideoClip([ImageClip(str(title_image_path)).set_duration(total_duration)])
    clip.write_videofile(str(video_path), fps=24)

    title_clip = VideoFileClip(str(video_path))

    # rounded corners
    def make_rounded_mask(size, radius):
        w, h = size
        mask = Image.new('L', (w, h), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), (w, h)], radius=radius, fill=255)
        return np.array(mask) / 255.0

    mask = make_rounded_mask(title_clip.size, radius=corner_radius)
    title_clip = title_clip.set_mask(ImageClip(mask, ismask=True).set_duration(total_duration))

    # resize animation
    def resize(t):
        if t <= scale_duration:
            progress = t / scale_duration
            eased = progress ** 2  # ease-in
            return start_scale + eased * (end_scale - start_scale)
        else:
            return end_scale

    title_clip = title_clip.resize(lambda t: resize(t))
    title_clip = title_clip.set_position("center")

    # slide right animation
    def slide_out_position(t):
        if t <= audio_clip.duration:
            return ("center", "center")
        else:
            progress = min((t - audio_clip.duration) / outro_duration, 1)
            ease_out = 1 - (1 - progress) ** 2  # ease-out

            # map out x coordinate
            start_x = (video_width - title_clip.w) // 2
            end_x = video_width * 2  # offscreen right
            current_x = start_x + ease_out * (end_x - start_x)
            return (current_x, "center")

    # write if statement depending on animation
    if outro_animation == "fade_out":
        title_clip = title_clip.crossfadeout(outro_duration)
    elif outro_animation == "slide_right":
        title_clip = title_clip.set_position(slide_out_position)

    # add audio and sound effects
    intro_sfx = AudioFileClip("audio/idea.mp3").volumex(0.5).set_start(0)
    outro_sfx = AudioFileClip("audio/whoosh.mp3").volumex(0.5).set_start(audio_clip.duration)
    sfx_clips = [intro_sfx, outro_sfx]

    # combine main audio with sfx
    audio = CompositeAudioClip([audio_clip] + sfx_clips)
    title_clip = title_clip.set_audio(audio)

    return title_clip

def compile_final_video(file_name, video_background, title_clip, text_clips, all_comments_path):
    comments_audio = (AudioFileClip(str(all_comments_path)).set_start(title_clip.duration) if all_comments_path else None)
    all_audios = [title_clip.audio] + ([comments_audio] if comments_audio else [])

    # combine the audio and video of the title and comments
    final_video = CompositeVideoClip([video_background, title_clip] + text_clips)
    final_audio = CompositeAudioClip(all_audios)

    # set audio and duration and render
    final_video = final_video.set_audio(final_audio).set_duration(max(final_video.duration, title_clip.duration + (comments_audio.duration if comments_audio else 0)))

    final_video.write_videofile((file_name + ".mp4"), fps=24)
