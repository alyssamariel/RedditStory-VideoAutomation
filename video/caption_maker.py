
import whisper_timestamped as whisper
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip
import numpy as np
import os

def get_transcribed_text(filename, guide_text, model_size="small"):
    audio = whisper.load_audio(filename)
    model = whisper.load_model(model_size, device="cpu")
    result = whisper.transcribe(model,audio,language="en",initial_prompt=guide_text)
    return result

def get_text_clips(text):
    # settings
    font_path="fonts/Poppins-Bold.ttf"
    font_size=100
    stroke_width=5
    stroke_color="black"
    fill_color="white"
    video_size=(1080, 1920)
    offset=(0, 8)
    
    if not os.path.isfile(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")
    
    font = ImageFont.truetype(font_path, font_size)

    text_clips_array = []
    segments = text["segments"]
    for segment in segments:
        for word in segment["words"]:
            word_text = word["text"]
            start = word["start"]
            end = word["end"]

            # transparent background base
            img = Image.new("RGBA", video_size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # get text width x height
            bbox = draw.textbbox((0, 0), word_text, font=font, stroke_width=stroke_width)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # get x and y coordinates
            x = (video_size[0] - text_width) // 2
            y = (video_size[1] - text_height) // 2

            # draw offset stroke for text
            draw.text(
                    (x + offset[0], y + offset[1]),
                    word_text,
                    font=font,
                    fill=stroke_color,
                    stroke_width=stroke_width,
                    stroke_fill=stroke_color
                )

            # draw main text
            draw.text(
                    (x, y),
                    word_text,
                    font=font,
                    fill=fill_color,
                    stroke_width=stroke_width,
                    stroke_fill=stroke_color
                )

            # Downscale and keep alpha
            #img = img.resize(video_size, Image.LANCZOS)

            # convert to image clip with transparency
            clip = ImageClip(np.array(img), ismask=False).set_start(start).set_end(end).set_position("center")

            text_clips_array.append(clip)

    return text_clips_array