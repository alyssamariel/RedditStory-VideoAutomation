from moviepy.editor import *
import os

#settings
final_size = (1080, 1920)
scale_duration = 0.5
corner_radius = 50

#imageclip title
clip = CompositeVideoClip([ImageClip("output.png").set_duration(scale_duration)])
clip.write_videofile("temp_image.mp4", fps=24)

scaled_clip = VideoFileClip("temp_image.mp4").without_audio()

#scale animation
def resize(t):
    start_scale = 0.9
    end_scale = 1.1
    scale_factor = start_scale + t/scale_duration * (end_scale - start_scale)
    return scale_factor

scaled_clip = scaled_clip.resize(lambda t: resize(t))
scaled_clip = scaled_clip.set_position("center")

#background video
background = ColorClip(final_size, color=(255, 255, 255)).set_duration(scale_duration)

#final video
video = CompositeVideoClip([background, scaled_clip])
video.write_videofile("final.mp4", fps=24)

scaled_clip.close()
if os.path.exists("temp_image.mp4"):
    os.remove("temp_image.mp4")
