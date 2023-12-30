from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()

def does_pixel_match(image_path, x, y, target_hex):
    """
    Check if the pixel at coordinates (x, y) in the image matches the target hex color.
    """
    # Open the image
    with Image.open(image_path) as img:
        # Get the color of the pixel at (x, y)
        pixel_color = img.getpixel((x, y))

        # Convert the pixel color to hex format
        pixel_hex = "#{:02x}{:02x}{:02x}".format(*pixel_color[:3])
        print('pixel_hex', pixel_hex)

        # Compare with the target hex color
        return pixel_hex.lower() == target_hex.lower()

# Example usage
image_path = 'screenshots/editor_cropped.png'  # Replace with your image path

result = does_pixel_match(image_path, int(os.getenv('TITLEBAR_COLOR_X')), int(os.getenv('TITLEBAR_COLOR_Y')), os.getenv('TITLEBAR_COLOR'))
print("Does the pixel match the target color?", result)
