import os
import sys
import math
import arcade
import PySimpleGUI as gui
import render_video

# Main window width & height
WIDTH = 1000
HEIGHT = 800

# Chosen color & shape row & column variables
chosen_color_row = 0
chosen_color_column = 0
chosen_shape_row = 0
chosen_shape_column = 0

# In-the-moment rendering variables
start_x = 0
start_y = 0
end_x = 0
end_y = 0

# Toolbar color lists
colors_col1 = [arcade.color.RED, arcade.color.ORANGE, arcade.color.YELLOW, arcade.color.GREEN,arcade.color.BLUE, arcade.color.PURPLE, arcade.color.VIOLET, arcade.color.WHITE, arcade.color.BLACK]
colors_col2 = [arcade.color.RED_ORANGE, arcade.color.FLUORESCENT_ORANGE, arcade.color.FLUORESCENT_YELLOW, arcade.color.YELLOW_GREEN, arcade.color.AIR_SUPERIORITY_BLUE, arcade.color.FUCHSIA_PURPLE, arcade.color.BLUE_VIOLET, arcade.color.WHITE_SMOKE, arcade.color.ASH_GREY]

# Vertex Buffer Object (VBO), background scene, and captured frame rendering variables
toolbar = None
current_frame = 1
frames = []
linked_scenes = dict()
captured = [False]

# Create resource directories
try:
    os.makedirs("res/frames")
    print("Directory \"res/frames\" Created")
except:
    print("Directory \"res/frames\" Already Exists")
try:
    os.makedirs("res/scenes")
    print("Directory \"res/scenes\" Created")
except:
    print("Directory \"res/scenes\" Already Exists")