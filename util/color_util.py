import re
import json
import os
import numpy as np

colors_json_file = "colors.json"

base_path = os.path.dirname(__file__)


def hex_to_rgb(value):
    """
    Converts a 6 character hex rgb value to a tuple of decimal rgb values
    This is intended to be a private method of the program, and no validation is done on the input
    Value *must* be a string of the form "FFFFFF"
    """
    return tuple(int(value[i:i+2], 16) for i in range(0, 6, 2))


def rgb_to_hex(r, g, b):
    """
    Converts the three values into a single hex string
    This is intended to be a private method of the program, and no validation is done on the input
    Each of r, g, b *must* be an int within range [0, 256)
    """
    return "{:02X}{:02X}{:02X}".format(r, g, b)


def get_color(r, g, b):
    point = np.array([r, g, b])
    distances = ((rgb_np_array-point)**2).sum(axis=1)
    min_idx = distances.argmin()
    return color_list[min_idx]


def convert_raw():
    """
    Creates a python list of dictionaries
    Each dictionary of the form {"group": color_group, "name": color_name, "rgb": current_rgb}
    Internal function to this file used by create_color_references()
    """
    pattern = re.compile(r"(?<=\w)([A-Z])")  # used to add space before capital letters: LightBlue -> Light Blue
    prelim_colors = dict()
    with open(os.path.join(base_path, "../aux", "raw_x11.txt"), "r") as f:
        for line in f:
            line = line.split()
            rgb = line[2].strip("#")
            color_name = line[1]
            prelim_colors[color_name] = rgb

    prelim_groups = dict()
    current_group = None
    with open(os.path.join(base_path, "../aux", "raw_groups.txt"), "r") as f:
        for line in f:
            if line[0] == "*":
                current_group = line.split()[0].strip("*")
                prelim_groups[current_group] = []
            else:
                prelim_groups[current_group] += [line.split()[0]]

    colors = []
    for (current_group, group_colors) in prelim_groups.iteritems():
        for current_color in group_colors:
            current_rgb = prelim_colors[current_color]
            color_name = pattern.sub(r" \1", current_color)
            color_group = pattern.sub(r" \1", current_group)
            colors.append({"group": color_group, "name": color_name, "hex": current_rgb})

    return colors


def save_as_json(file_path, python_object):
    """
    Saves a python object as json to file_path
    """
    json_colors = json.dumps(python_object, indent=2)
    with open(file_path, "w") as f:
        f.write(json_colors)


def create_color_references():
    if not os.path.exists(os.path.join(base_path, colors_json_file)):
        save_as_json(os.path.join(base_path, colors_json_file), convert_raw())

    with open(os.path.join(base_path, colors_json_file), "r") as f:
        color_list = json.loads(f.read())
        rgb_np_array = np.empty([len(color_list), 3], dtype=int)
        for q, color in enumerate(color_list):
            (r, g, b) = hex_to_rgb(color['hex'])
            rgb_np_array[q, 0] = r
            rgb_np_array[q, 1] = g
            rgb_np_array[q, 2] = b
    return color_list, rgb_np_array


color_list, rgb_np_array = create_color_references()