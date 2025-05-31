from moviepy.editor import *
from moviepy.audio.fx.volumex import volumex
import numpy as np
from pydub import AudioSegment

def make_silence(duration=0.5, fps=44100, n_channels=2):
    def make_frame(t):
        if np.isscalar(t):
            return np.zeros((n_channels,))
        else:
            return np.zeros((len(t), n_channels))
    silence = AudioClip(make_frame=make_frame, duration=duration, fps=fps)
    return silence


def combine_audio_clips(final_path, audio_paths):
    combined = AudioSegment.empty()
    total_duration = 0  # in milliseconds

    for i, path in enumerate(audio_paths):
        clip = AudioSegment.from_file(path)
        clip_duration = len(clip)  # in milliseconds

        # Add 500ms silence between clips, but not after the last one
        silence = AudioSegment.silent(duration=500) if i < len(audio_paths) - 1 else AudioSegment.empty()

        # Check if adding this clip (plus silence) would exceed 60 seconds
        if total_duration + clip_duration + len(silence) > 60000:
            break

        combined += clip
        total_duration += clip_duration

        if len(silence) > 0:
            combined += silence
            total_duration += len(silence)

    # Export the final audio
    combined.export(final_path, format="mp3")  # or "wav"

def get_duration(path):
    return AudioFileClip(str(path)).duration