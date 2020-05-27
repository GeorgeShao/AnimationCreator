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


def list_scenes():
    path = sys.argv[0][:-20] + "/res/scenes"
    files = []
    for r, d, f in os.walk(path):
        for f1 in f:
            f1 = str(f1).replace(".png","")
            files.append(f1)
    return files


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
    global toolbar, frames, current_frame, linked_scenes

    # Render entire toolbar, all user-drawn shapes
    arcade.start_render()
    
    if (current_frame-1) in linked_scenes.keys():
        background_texture = arcade.load_texture("res/scenes/" + linked_scenes[current_frame-1] + ".png")
        arcade.draw_texture_rectangle(center_x=500, center_y=400, width=800, height=800, texture=background_texture)
    try:
        frames[current_frame-1].draw()
    except Exception as e:
        print("ERROR:", e)
    try:
        toolbar.draw()
    except Exception as e:
        print("ERROR:", e)
    
    arcade.draw_text("Total # Frames:", 905, 731, color=arcade.color.BLACK, font_size=12)
    arcade.draw_text(str(len(frames)), 910, 705, color=arcade.color.BLACK, font_size=20)
    arcade.draw_text("Current Frame:", 905, 681, color=arcade.color.BLACK, font_size=12)
    arcade.draw_text(str(current_frame), 910, 655, color=arcade.color.BLACK, font_size=20)

    arcade.draw_text("PREV FRM", 902, 631, color=arcade.color.BLACK, font_size=9)
    arcade.draw_text("NEXT FRM", 952, 631, color=arcade.color.BLACK, font_size=9)

    arcade.draw_text("UNDO", 910, 581, color=arcade.color.BLACK, font_size=9)
    arcade.draw_text("CLR FRM", 955, 581, color=arcade.color.BLACK, font_size=9)

    arcade.draw_text("DEL FRM", 904, 531, color=arcade.color.BLACK, font_size=9)
    arcade.draw_text("NEW FRM", 952, 531, color=arcade.color.BLACK, font_size=9)

    arcade.draw_text("LOAD SCN", 902, 481, color=arcade.color.BLACK, font_size=9)
    arcade.draw_text("NEW SCN", 954, 481, color=arcade.color.BLACK, font_size=9)

    if captured[current_frame-1]:
        arcade.draw_xywh_rectangle_filled(900, 750, 100, 50, color=arcade.color.GREEN)
        arcade.draw_text("CAPTURED", 907, 765, color=arcade.color.BLACK, font_size=16)
    else:
        arcade.draw_text("CAPTURE", 912, 765, color=arcade.color.BLACK, font_size=16)
    if all(captured):
        arcade.draw_xywh_rectangle_filled(0, 750, 100, 50, color=arcade.color.GREEN)
    arcade.draw_text("RENDER", 13, 765, color=arcade.color.BLACK, font_size=18)

    arcade.draw_text("ABOUT", 918, 17, color=arcade.color.BLACK, font_size=18)


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


def on_key_press(key, modifiers):
    pass


def on_key_release(key, modifiers):
    pass


def on_mouse_drag(x, y, dx, dy, button, modifiers):
    if 100 < x < 900:
        if chosen_shape_column == 2:
            start_x = x
            start_y = y
            end_x = x + dx
            end_y = y + dy
            drawing_width = 2**(15-(chosen_shape_row))
            frames[current_frame-1].append(arcade.create_line(start_x, start_y, end_x, end_y, get_chosen_color(), drawing_width))
            captured[current_frame-1] = False


def on_mouse_press(x, y, button, modifiers):
    global frames, current_frame, linked_scenes, captured
    global chosen_color_column, chosen_shape_column, chosen_color_row, chosen_shape_row
    global start_x, start_y, end_x, end_y

    # Determine what to do based on the location of the user's click
    if 100 < x < 900:
        start_x = x
        start_y = y
        captured[current_frame-1] = False
    elif x <= 50:
        if 450 <= y <= 750:
            chosen_shape_row = y//50 + 1
            chosen_shape_column = 1
        elif y <= 450:
            chosen_color_row = y/50 + 1
            chosen_color_column = 1
    elif x <= 100:
        if 450 <= y <= 750:
            chosen_shape_row = y//50 + 1
            chosen_shape_column = 2
        elif y <= 450:
            chosen_color_row = y//50 + 1
            chosen_color_column = 2
    elif x >= 950:
        if 450 < y < 500:
            gui.theme('Dark Blue 3')
            layout = [  [gui.Text("Scenes:")],
                        [gui.Listbox(values=list(list_scenes()), size=(30,6))],
                        [gui.Text("New Scene Name:"), gui.InputText()],
                        [gui.Button('Create New Scene'), gui.Button('Cancel')]  ]
            window = gui.Window('AnimationCreator', layout)
            while True:
                event, values = window.read()
                if event in (None, 'Cancel'):
                    break
                if str(values[1]).strip() != "":
                    image = arcade.get_image(100, 0, 800, 800)
                    image.save(f"res/scenes/{str(values[1]).strip()}.png", "PNG")
                    linked_scenes[current_frame-1] = str(values[1]).strip()
                    frames[current_frame-1] = arcade.ShapeElementList()
                    print('New Scene Created From Current Frame:', str(values[1]).strip())
                    break
            window.close()
        elif 500 < y < 550:
            frames.append(arcade.ShapeElementList())
            current_frame = len(frames)
            print("New Frame Created")
            captured.append(False)
        elif 550 < y < 600:
            frames[current_frame-1] = arcade.ShapeElementList()
            if (current_frame-1) in linked_scenes:
                del linked_scenes[current_frame-1]
            print("Current Frame Cleared")
            captured[current_frame-1] = False
        elif 600 < y < 650:
            if current_frame < len(frames):
                current_frame += 1
                print("Forward Frame")
            else:
                print("Cannot Forward Frame - Reached End of Timeline")
    elif x >= 900:
        if 450 < y < 500:
            gui.theme('Dark Blue 3')
            layout = [  [gui.Text("Scenes:")],
                        [gui.Listbox(values=list(list_scenes()), size=(30,6))],
                        [gui.Button('Load Scene'), gui.Button('Cancel')]  ]
            window = gui.Window('AnimationCreator', layout)
            while True:
                event, values = window.read()
                if event in (None, 'Cancel'):
                    break
                if str(values[0])[2:-2] != "":
                    linked_scenes[current_frame-1] = str(values[0])[2:-2]
                    frames[current_frame-1] = arcade.ShapeElementList()
                    print('Loaded Scene:', str(values[0])[2:-2])
                    break
            window.close()
            captured[current_frame-1] = False
        elif 500 < y < 550:
            if len(frames) > 1:
                del frames[current_frame-1]
                if str(current_frame-1) in linked_scenes.keys():
                    del linked_scenes[current_frame-1]
                print("Deleted Current Frame")
                captured[current_frame-1] = False
                for i in range(current_frame-1, len(captured)):
                    captured[i] = False
                current_frame -= 1
            else:
                print("Cannot Delete Frame - At Least One Frame Must Exist")
        elif 550 < y < 600:
            frames[current_frame-1].remove(frames[current_frame-1][-1])
            print("Last Drawing on Current Frame Undone")
            captured[current_frame-1] = False
        elif 600 < y < 650:
            if current_frame > 1:
                current_frame -= 1
                print("Backward Frame")
            else:
                print("Cannot Backward Frame - Reached Beginning of Timeline")
    
    # Capture functionality
    if x > 900 and y > 750:
        image = arcade.get_image(100, 0, 800, 800)
        current_frame_name = (10-len(str(current_frame)))*"0" + str(current_frame)
        image.save(f"res/frames/{current_frame_name}.png", "PNG")
        print("Captured Frame")
        captured[current_frame-1] = True

    # Render functionality
    if x < 100 and y > 750:
        if all(captured):
            gui.theme('Dark Blue 3')
            layout = [  [gui.Text("Frames per Image (positive integer): "), gui.InputText("20")],
                        [gui.Button('Start Render'), gui.Button('Cancel')]  ]
            window = gui.Window('AnimationCreator', layout)
            while True:
                event, values = window.read()
                if event in (None, 'Cancel'):
                    break
                if event in (None, 'Start Render'):
                    if str(values[0]) != "" and str(values[0]).isdigit():
                        print(f"Rendering at {int(values[0])} frames per image...")
                        render_video.run(int(values[0]))
                    else:
                        print(f"Rendering at 20 frames per image...")
                        render_video.run(20)
                    print("Render Complete")
                    break
            window.close()
        else:
            gui.theme('Dark Blue 3')
            layout = [  [gui.Text("Please Capture All Frames Before Rendering")],
                        [gui.Button('Ok')]  ]
            window = gui.Window('AnimationCreator', layout)
            while True:
                event, values = window.read()
                if event in (None, 'Ok'):
                    break
            window.close()

    # About button functionality
    if x > 900 and y < 50:
        gui.theme('Dark Blue 3')
        layout = [  [gui.Text("AnimationCreator was created by George Shao")],
                    [gui.Text("Find out more at: https://github.com/GeorgeShao/AnimationCreator")],
                    [gui.Button('Ok')]  ]
        window = gui.Window('AnimationCreator', layout)
        while True:
            event, values = window.read()
            if event in (None, 'Ok'):
                break
        window.close()
        

def on_mouse_release(x, y, button, modifiers):
    global toolbar, frames, current_frame
    global start_x, start_y, end_x, end_y

    if 100 < x < 900:
        end_x = x
        end_y = y
        if chosen_shape_column == 1:
            if chosen_shape_row == 15:
                frames[current_frame-1].append(arcade.create_rectangle_filled((start_x+end_x)//2, (start_y+end_y)//2, abs(end_x-start_x), abs(end_y-start_y), get_chosen_color()))
            if chosen_shape_row == 14:
                radius = round(math.sqrt(abs(end_x-start_x)** 2 + abs(end_y-start_y)**2))
                frames[current_frame-1].append(arcade.create_ellipse_filled(start_x, start_y, radius, radius, get_chosen_color()))
            if chosen_shape_row == 13:
                frames[current_frame-1].append(arcade.create_ellipse_filled(start_x, start_y, abs(end_x-start_x), abs(end_y-start_y), get_chosen_color()))
            if chosen_shape_row == 12:
                frames[current_frame-1].append(arcade.create_rectangle_outline((start_x+end_x)//2, (start_y+end_y)//2, abs(end_x-start_x), abs(end_y-start_y), get_chosen_color()))
            if chosen_shape_row == 11:
                radius = round(math.sqrt(abs(end_x-start_x)** 2 + abs(end_y-start_y)**2))
                frames[current_frame-1].append(arcade.create_ellipse_outline(start_x, start_y, radius, radius, get_chosen_color()))
            if chosen_shape_row == 10:
                frames[current_frame-1].append(arcade.create_ellipse_outline(start_x, start_y, abs(end_x-start_x), abs(end_y-start_y), get_chosen_color()))


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
    render_toolbar_colors()

    arcade.run()


if __name__ == '__main__':
    setup()
