from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()

def crop_titlebar(image_path, output_path):
    """
    Crop the top part of an image.

    :param image_path: Path to the input image.
    :param output_path: Path to save the cropped image.
    :param height: Height of the top part to keep in pixels. Default is 28.
    """
    # Open the image
    with Image.open(image_path) as img:
        # Calculate the crop rectangle
        crop_rectangle = (int(os.getenv('TITLEBAR_LEFT_BOUNDARY')), 0, img.width - int(os.getenv('TITLEBAR_RIGHT_BOUNDARY')), int(os.getenv('TITLEBAR_HEIGHT')))

        # Perform the crop
        cropped_img = img.crop(crop_rectangle)

        # Save the cropped image
        cropped_img.save(output_path)

# crop_titlebar('./screenshots/editor_cropped.png', './screenshots/editor_titlebar.png')
# crop_titlebar('./screenshots/qtbus_cropped.png', './screenshots/qtbus_titlebar.png')
