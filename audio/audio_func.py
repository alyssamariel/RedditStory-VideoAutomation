from moviepy.editor import *
from moviepy.audio.fx.volumex import volumex
import numpy as np

def make_silence(duration=0.5, fps=44100, n_channels=2):
    def make_frame(t):
        if np.isscalar(t):
            return np.zeros((n_channels,))
        else:
            return np.zeros((len(t), n_channels))
    silence = AudioClip(make_frame=make_frame, duration=duration, fps=fps)
    return silence


def combine_audio_clips(final_path, audio_paths):
    audio_clips = []
    total_duration = 0

    for i, path in enumerate(audio_paths):
        clip = AudioFileClip(str(path))
        silence = make_silence(0.5, clip.fps, clip.reader.nchannels)

        silence_duration = 0.5 if i < len(audio_paths) - 1 else 0

        if total_duration + clip.duration + silence_duration > 60:
            clip.close()
            break

        audio_clips.append(clip)
        total_duration += clip.duration

        if silence_duration > 0:
            silence = silence = make_silence(0.5, clip.fps, clip.reader.nchannels)
            audio_clips.append(silence)
            total_duration += silence_duration

    combined_audio = concatenate_audioclips(audio_clips)
    combined_audio.write_audiofile(str(final_path))

def get_duration(path):
    return AudioFileClip(str(path)).duration