from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()

def hex_to_rgb(hex_color):
    """Convert a hex color to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def find_color_y_position(input_image):
    """
    Find the Y-coordinate of the first occurrence of a specified color in an image,
    starting from a given X-coordinate.
    """
    width, height = input_image.size

    if int(os.getenv('TITLEBAR_COLOR_X')) >= width:
        return None

    for y in range(int(os.getenv('TITLEBAR_COLOR_Y_LIMIT'))):
        pixel = input_image.getpixel((int(os.getenv('TITLEBAR_COLOR_X')), y))
        pixel_hex = "#{:02x}{:02x}{:02x}".format(*pixel[:3])
        if pixel_hex == os.getenv('TITLEBAR_COLOR').lower():
            return y

    return None

def extract_titlebar(input_image, y_coordinate):
    """
    Crop the image starting from a specified y-coordinate, using the full width
    and extending down by a specified height.
    """

    width, _ = input_image.size
    # Define the cropping box (left, upper, right, lower)
    crop_box = (int(os.getenv('TITLEBAR_COLOR_X')) + int(os.getenv('TITLEBAR_LEFT_BOUNDARY')), y_coordinate, width - int(os.getenv('TITLEBAR_RIGHT_BOUNDARY')), y_coordinate + int(os.getenv('TITLEBAR_HEIGHT')))
    cropped_titlebar = input_image.crop(crop_box)
    return cropped_titlebar

def extract_content(input_image, y_coordinate):
    """
    Crop the image starting from a specified y-coordinate, using the full width
    and extending down by a specified height.
    """

    width, height = input_image.size
    crop_box = (0, y_coordinate, width, height)
    cropped_content = input_image.crop(crop_box)
    return cropped_content

def crop_image(input_image):
    y_position = find_color_y_position(input_image)
    if y_position is not None:
        # print(f"Color found at Y-coordinate: {y_position}")
        titlebar = extract_titlebar(input_image, y_position)
        content = extract_content(input_image, y_position)
        return content, titlebar
    else:
        print("Titlebar color not found.")
        content = extract_content(input_image, 0)
        return content,