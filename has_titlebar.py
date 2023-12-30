from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()

def has_titlebar(image_path):
    """
    Check if the pixel at coordinates (x, y) in the image matches the target hex color.
    """
    # Open the image
    with Image.open(image_path) as img:
        # Get the color of the pixel at (x, y)
        pixel_color = img.getpixel((int(os.getenv('TITLEBAR_COLOR_X')), int(os.getenv('TITLEBAR_COLOR_Y'))))

        # Convert the pixel color to hex format
        pixel_hex = "#{:02x}{:02x}{:02x}".format(*pixel_color[:3])
        # print('pixel_hex', pixel_hex)

        # Compare with the target hex color
        return pixel_hex.lower() == os.getenv('TITLEBAR_COLOR')

# image_path = './screenshots/crop/2023-12-30_00-26-54.png'
# print(has_titlebar(image_path))
