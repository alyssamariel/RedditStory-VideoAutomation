from moviepy.editor import *
from moviepy.audio.fx.volumex import volumex
import numpy as np
from pydub import AudioSegment

# combine audio clips of all commetns
def combine_audio_clips(final_path, audio_paths, silence_duration, clip_limit=60000):
    combined = AudioSegment.empty()
    total_duration = 0
    has_exceeded_limit = False
    clip_limit_ms = int(clip_limit) * 1000

    for i, path in enumerate(audio_paths):
        clip = AudioSegment.from_file(path)
        clip_duration = len(clip)

        # add silence
        silence = AudioSegment.silent(duration=silence_duration) if i < len(audio_paths) - 1 else AudioSegment.empty()

        # allow a segment of clip to go pass 1 min mark once
        if total_duration + clip_duration + len(silence) > clip_limit_ms:
            if has_exceeded_limit:
                break
            else:
                has_exceeded_limit = True

        # add clip to combined clips and duration 
        combined += clip
        total_duration += clip_duration

        # add silence to combined clips and duration
        if len(silence) > 0:
            combined += silence
            total_duration += len(silence)

    # export audio
    combined.export(final_path, format="mp3")

def get_duration(path):
    return AudioFileClip(str(path)).duration