import imageio
import numpy as np
from moviepy.editor import ImageSequenceClip

# Path to the input GIF file
gif_path = r"D:\wre\The Merge\game\images\bg\Starting_Room\bgstart.gif"

# Read the GIF frames
gif = imageio.mimread(gif_path)

# Get the dimensions of the first frame
height, width, _ = gif[0].shape

# Resize all frames to the dimensions of the first frame
gif_resized = [np.array(imageio.core.util.Array(frame).resize((width, height))) for frame in gif]

# Create a video clip from the resized frames
clip = ImageSequenceClip(gif_resized, fps=10)

# Path to the output OGG file
ogg_path = r"D:\wre\The Merge\game\images\bg\Starting_Room\bgstart.ogg"

# Write the video clip to the OGG file
clip.write_videofile(ogg_path, codec='libtheora')
