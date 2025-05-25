from title_image.title_maker import generate_reddit_title_image
from video.video_maker import generate_title_video, compile_final_video
from video.caption_maker import get_transcribed_text, get_text_clips
from reddit_api import get_reddit_object, get_reddit_post_comments
from audio.streamlabs_tts import streamlabs_tts
from audio.audio_func import combine_audio_clips
from moviepy.editor import *
from pathlib import Path
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# get reddit post url
url = input("Enter the url: ")
reddit_object = get_reddit_object(url)

# create folder for post
folder_path = Path("post_files") / reddit_object.name
folder_path.mkdir(parents=True, exist_ok=True)

# generate title image
title_image_path = generate_reddit_title_image(reddit_object)

# generate title audio
title_audio_path = folder_path / f"{reddit_object.name}_title-audio.mp3"
streamlabs_tts(reddit_object.title, config["tts"]["voice_choice"], title_audio_path)

# generate comments audio
comment_audio_paths  = []
comments =  get_reddit_post_comments(url)

for idx, comment in enumerate(comments, start=1):
    filename = folder_path / f"{reddit_object.name}_comment_{idx}.mp3"
    try:
        streamlabs_tts(f"{idx}. {comment}", config["tts"]["voice_choice"], filename)
        
        comment_audio_paths.append(filename)
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Failed to generate TTS for comment {idx}: {e}")

# combine all comments for captioning
all_comments_path = folder_path / f"{reddit_object.name}_all_comments.mp3"
all_comments_string = "\n".join([f"{idx+1}. {comment}" for idx, comment in enumerate(comments)])
combine_audio_clips(all_comments_path, comment_audio_paths)

# generate title image animation
title_clip = generate_title_video(title_image_path, title_audio_path)

transcribed_text = get_transcribed_text(all_comments_path, all_comments_string)
text_clips = get_text_clips(transcribed_text, title_clip.duration)

# background
background = ColorClip((1080, 1920), color=(255, 255, 255)).set_duration(70)

# compile final video
compile_final_video(reddit_object.name, background, title_clip, text_clips, all_comments_path)




