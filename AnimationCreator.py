import os
import sys
import math
import arcade
import PySimpleGUI as gui

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

def get_chosen_color():
    global chosen_color_column, chosen_color_row, colors_col1, colors_col2

    # Return user-chosen color
    if chosen_color_column == 1:
        return colors_col1[-int(chosen_color_row)]
    elif chosen_color_column == 2:
        return colors_col2[-int(chosen_color_row)]
    else:
        return arcade.color.BLACK

def on_update(delta_time):
    pass


def on_draw():
    pass


def on_mouse_press():
    pass


def on_mouse_release():
    pass


def on_key_press():
    pass


def on_key_release():
    pass


def on_mouse_drag():
    pass


def render_toolbar_dividers():
    global toolbar

    # Render left toolbar
    toolbar.append(arcade.create_rectangle_filled(50, 400, 100, 800, arcade.color.COOL_GREY))

    # Render right toolbar
    toolbar.append(arcade.create_rectangle_filled(950, 400, 100, 800, arcade.color.COOL_GREY))

    # Render left toolbar middle divider
    toolbar.append(arcade.create_line(50, 0, 50, 750, arcade.color.BLACK))

    # Render right toolbar middle divider
    toolbar.append(arcade.create_line(950, 200, 950, 650, arcade.color.BLACK))

    # Render left and right toolbar mini dividers
    for i in range(0, 800, 50):
        toolbar.append(arcade.create_line(0, i, 100, i, arcade.color.BLACK))
        toolbar.append(arcade.create_line(900, i, 1000, i, arcade.color.BLACK))


def render_toolbar_shapes():
    global toolbar

    # Render toolbar rectangles
    toolbar.append(arcade.create_rectangle_filled(25, 725, 35, 15, arcade.color.BLUE))
    toolbar.append(arcade.create_rectangle_outline(25, 575, 35, 15, arcade.color.BLUE))

    # Render toolbar circles
    toolbar.append(arcade.create_ellipse_filled(25, 675, 13, 13, arcade.color.BLUE))
    toolbar.append(arcade.create_ellipse_outline(25, 525, 13, 13, arcade.color.BLUE))

    # Render toolbar ellipses
    toolbar.append(arcade.create_ellipse_filled(25, 625, 18, 8, arcade.color.BLUE))
    toolbar.append(arcade.create_ellipse_outline(25, 475, 18, 8, arcade.color.BLUE))

    # Render toolbar lines
    for i in range(6):
        toolbar.append(arcade.create_line(60, 710-(50*i), 90, 740-(50*i), arcade.color.BLUE, line_width=(2**i)))


def render_toolbar_colors():
    global toolbar, colors_col1, colors_col2

    # Render toolbar colors
    for i in range(9):
        toolbar.append(arcade.create_rectangle_filled(25, 425-(50*i), 50, 50, colors_col1[i]))
        toolbar.append(arcade.create_rectangle_filled(75, 425-(50*i), 50, 50, colors_col2[i]))


def setup():
    global toolbar, frames

    arcade.open_window(WIDTH, HEIGHT, "AnimationCreator")
    arcade.set_background_color(arcade.color.WHITE)
    arcade.schedule(on_update, 1/60)

    # Create Vertex Buffer Object (VBO) shape lists
    frames.append(arcade.ShapeElementList())
    toolbar = arcade.ShapeElementList()

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release
    window.on_mouse_press = on_mouse_press
    window.on_mouse_release = on_mouse_release
    window.on_mouse_drag = on_mouse_drag

    # Render toolbar
    render_toolbar_dividers()
    render_toolbar_shapes()

    arcade.run()


if __name__ == '__main__':
    setup()
