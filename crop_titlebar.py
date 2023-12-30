from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()

def hex_to_rgb(hex_color):
    """Convert a hex color to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def find_color_y_position(image_path):
    """
    Find the Y-coordinate of the first occurrence of a specified color in an image,
    starting from a given X-coordinate.
    """
    target_color = hex_to_rgb(os.getenv('TITLEBAR_COLOR'))
    with Image.open(image_path) as img:
        width, height = img.size

        if int(os.getenv('TITLEBAR_COLOR_X')) >= width:
            return None

        for y in range(int(os.getenv('TITLEBAR_COLOR_Y_LIMIT'))):
            pixel = img.getpixel((int(os.getenv('TITLEBAR_COLOR_X')), y))
            pixel_hex = "#{:02x}{:02x}{:02x}".format(*pixel[:3])
            if pixel_hex == os.getenv('TITLEBAR_COLOR').lower():
                return y

        return None

def crop_image_at_coordinate(image_path, y_coordinate, output_path=None):
    """
    Crop the image starting from a specified y-coordinate, using the full width
    and extending down by a specified height.
    """
    with Image.open(image_path) as img:
        width, _ = img.size
        # Define the cropping box (left, upper, right, lower)
        crop_box = (int(os.getenv('TITLEBAR_COLOR_X')) + int(os.getenv('TITLEBAR_LEFT_BOUNDARY')), y_coordinate, width - int(os.getenv('TITLEBAR_RIGHT_BOUNDARY')), y_coordinate + int(os.getenv('TITLEBAR_HEIGHT')))
        cropped_img = img.crop(crop_box)
        cropped_img.save(output_path)

def crop_titlebar(image_path, output_path):
  y_position = find_color_y_position(image_path)
  if y_position is not None:
      # print(f"Color found at Y-coordinate: {y_position}")
      crop_image_at_coordinate(image_path, y_position, output_path)
      return True
  else:
      print("Titlebar color not found.")
      return False


crop_titlebar('./benchmark/editor.png', './benchmark/editor_titlebar.png')