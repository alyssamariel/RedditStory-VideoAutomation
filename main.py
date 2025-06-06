from title_image.title_maker import generate_reddit_title_image
from video.video_maker import generate_title_video, compile_final_video
from video.caption_maker import get_transcribed_text, get_text_clips
from video.background_maker import create_mixed_video
from utils.text_func import clean_text
from reddit_api import get_reddit_object, get_reddit_post_comments
from audio.streamlabs_tts import streamlabs_tts
from audio.audio_func import combine_audio_clips, get_duration
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

# generate title image animation
title_clip = generate_title_video(title_image_path, title_audio_path)

# generate post description 
post_desc_audio_path = folder_path / f"{reddit_object.name}_post_desc.mp3"
post_desc = input("Include the post description? (y/n): ")

if post_desc == 'y':
    paragraphs = [p.strip() for p in clean_text(reddit_object.selftext).split("\n\n") if p.strip()]
    streamlabs_tts(reddit_object.selftext, config["tts"]["voice_choice"], post_desc_audio_path)
    

# generate comments audio
comment_audio_paths  = []
comments =  get_reddit_post_comments(url)

idx = 1
for comment in comments:
    # split the paragraphs
    paragraphs = [p.strip() for p in clean_text(comment).split("\n\n") if p.strip()]
    
    for p_idx, paragraph in enumerate(paragraphs, 1):
        filename = folder_path / f"{reddit_object.name}_comment_{idx}_{p_idx}.mp3"
        try:
            # prefix only the first paragraph with the idx
            if p_idx == 1:
                text = f"{idx}. {paragraph}"
            else:
                text = paragraph

            streamlabs_tts(text, config["tts"]["voice_choice"], filename)
            comment_audio_paths.append(filename)
            print(f"Saved: {filename}")
        except Exception as e:
            print(f"Failed to generate TTS for comment {idx}.{p_idx}: {e}")
    idx += 1


# combine all comments for captioning
clip_limit = input("how many seconds should the clip be: ")

all_comments_path = folder_path / f"{reddit_object.name}_all_comments.mp3" if comment_audio_paths else ""
all_comments_string = "\n".join([f"{idx+1}. {comment}" for idx, comment in enumerate(comments)])
if comments:
    combine_audio_clips(all_comments_path, comment_audio_paths, 500, clip_limit)
    transcribed_comments = get_transcribed_text(all_comments_path, all_comments_string)
    comment_clips = get_text_clips(transcribed_comments, title_clip.duration)
else:
    comment_clips = []

# background
video_folders = [Path("background") / name for name in ["assemble", "battery", "ladder", "roof"]]
clip_duration = 15

background = create_mixed_video(video_folders, clip_duration, title_clip.duration + get_duration(all_comments_path))

# compile final video
compile_final_video(reddit_object.name, background, title_clip, comment_clips, all_comments_path)




