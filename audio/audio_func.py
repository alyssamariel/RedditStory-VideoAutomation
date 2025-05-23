from moviepy.editor import *
import numpy as np

def make_silence(duration=0.5):
    return AudioClip(
        make_frame=lambda t: np.zeros((1,)),
        duration=duration,
        fps=44100
    )

def combine_audio_clips(final_path, audio_paths):
    audio_clips = []
    for path in audio_paths:
        audio_clips.append(AudioFileClip(str(path)))
        audio_clips.append(make_silence(0.5))

    combined_audio = concatenate_audioclips(audio_clips)
    print(final_path)
    combined_audio.write_audiofile(str(final_path))