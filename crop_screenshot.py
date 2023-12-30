from PIL import Image
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

def hex_to_rgb(hex_color):
    """Convert a hex color to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def is_close_color(colors, background_color, threshold=10):
    """
    Determine if colors are close to background_color within a given threshold.
    This is used to ensure the background color is still removed even if a floating window has a drop shadow.
    """
    return np.all(np.abs(colors - background_color) <= threshold, axis=-1)

def get_bounding_box(pixels, background_color, threshold=10):
    """Get the bounding box of the non-background area in an image."""
    mask = ~is_close_color(pixels, background_color, threshold)
    coords = np.argwhere(mask)
    if coords.size == 0:
        return None
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)
    return x_min, y_min, x_max + 1, y_max + 1

def replace_transparency(input_path, output_path):
    """
    Replace the transparency in a PNG image with a solid background color.

    Since Spectacle includes a transparent background we need to remove this and replace it with a solid color.
    Once we have the solid color we can crop the window so simplify OCR on the titlebar and contents.
    The use of a threshold ensures that the background color is removed even if a floating window has a drop shadow.
    """
    background_color = hex_to_rgb(os.getenv('TRANSPARENCY_REPLACEMENT_COLOR'))

    with Image.open(input_path) as img:
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            alpha = img.convert('RGBA').split()[-1]
            bg_image = Image.new("RGB", img.size, background_color)
            bg_image.paste(img, mask=alpha)
        else:
            bg_image = img.convert("RGB")

        pixels = np.array(bg_image)
        if is_close_color(pixels[0, 0], background_color, int(os.getenv('TRANSPARENCY_COLOR_THRESHOLD'))):
            bbox = get_bounding_box(pixels, background_color, int(os.getenv('TRANSPARENCY_COLOR_THRESHOLD')))
            if bbox:
                cropped_img = bg_image.crop(bbox)
                cropped_img.save(output_path, "PNG")
                return True
            else:
                print("No non-background area found.")
                return False
        else:
            return False

# Example usage
replace_transparency("./screenshots/qtbus.png", "./screenshots/qtbus_cropped.png")
replace_transparency("./screenshots/editor.png", "./screenshots/editor_cropped.png")
replace_transparency("./screenshots/terminal.png", "./screenshots/terminal_cropped.png")
