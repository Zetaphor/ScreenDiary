import subprocess
import os
import time
from datetime import datetime
import shutil
from PIL import Image
import pytesseract
import imagehash
from dotenv import load_dotenv
from crop_image import crop_image
from logger_config import get_logger

load_dotenv()

logger = get_logger()

DEBUG = bool(int(os.getenv('DEBUG')))
DEBUG_OCR = bool(int(os.getenv('DEBUG_OCR')))

phash = None
dhash = None
previous_dhash = None
previous_phash = None

def take_screenshot(filename):
    """Takes a screenshot using KDE's spectacle tool"""
    # Using spectacle with flags -b (no GUI), -n (no notifications) and -o (output file)
    subprocess.run(["spectacle", "-a", "-b", "-n", "-o", filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def binarize_image(image):
    """Convert an image to grayscale and binarize it"""
    img_copy = image.copy()
    img_copy = img_copy.convert("L")
    img_copy = img_copy.point(lambda x: 255 if x > int(os.getenv('BINARIZATION_THRESHOLD')) else 0, mode="1")
    return image

def process_display():
    global phash, dhash, previous_dhash, previous_phash
    if DEBUG:
        start_time = time.time()

    os.makedirs(f"./screenshots", exist_ok=True)

    datetime_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_file = f"./screenshots/{datetime_string}.png"
    take_screenshot(screenshot_file)

    capture = Image.open(f"./screenshots/{datetime_string}.png")

    # Check if the screenshot is identical to the previous one
    if bool(int(os.getenv('ENABLE_PERCEPTUAL_HASHING'))):
        phash = imagehash.phash(capture)
        if previous_phash is not None:
            if phash == previous_phash:
                logger.debug(f"Skipping identical frame: {datetime_string}")
                os.remove(screenshot_file)
                return

    # Check if the screenshot is similar to the previous one
    if bool(int(os.getenv('ENABLE_DIFFERENCE_THRESHOLD'))):
        dhash = imagehash.dhash(capture)
        if previous_dhash is not None:
            difference = dhash - previous_dhash
            logger.debug(f"Difference: {difference}")
            if difference < int(os.getenv('DIFFERENCE_THRESHOLD')):
                logger.debug(f"Skipping similar frame: {datetime_string}")
                os.remove(screenshot_file)
                return

    # Extract tht titlebar and OCR it
    crop_data = crop_image(capture)
    titlebar_str = ""
    if (len(crop_data) == 2):
        titlebar = binarize_image(crop_data[1])
        if bool(os.getenv('ENABLE_BINARIZATION')):
            titlebar = binarize_image(crop_data[1])
        titlebar_str = pytesseract.image_to_string(titlebar).strip()
        if titlebar_str is None:
            titlebar_str = ""

    # Extract the content and OCR it
    content_str = ""
    content = binarize_image(crop_data[0])
    if bool(int(os.getenv('ENABLE_BINARIZATION'))):
        content = binarize_image(crop_data[0])
    content_str = pytesseract.image_to_string(content).strip()
    if content_str is None:
        content_str = ""

    capture_result = {
        'datetime': datetime_string,
        'file_path': screenshot_file,
        'ocr_title': titlebar_str,
        'ocr_content': content_str
    }

    logger.info(f"Screenshot taken: {screenshot_file}")
    previous_dhash = dhash
    previous_phash = phash

    if DEBUG_OCR:
        os.makedirs(f"./ocr", exist_ok=True)

        # Write OCR title to a file
        with open(f"./ocr/{datetime_string}_title.txt", "w") as file:
            file.write(titlebar_str)

        # Write OCR content to a file
        with open(f"./ocr/{datetime_string}_content.txt", "w") as file:
            file.write(content_str)

    if DEBUG:
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.debug(f"Executed in {elapsed_time} seconds")

    return capture_result

# Clear contents of image folders in debug mode
if DEBUG:
    logger.debug('Debug enabled, deleting images and OCR...')
    for folder in ['screenshots', 'ocr']:
        for filename in os.listdir(folder):
            if filename == '.gitkeep': continue
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logger.error('Failed to delete %s. Reason: %s' % (file_path, e))