import subprocess
import os
import time
from datetime import datetime
from PIL import Image
import pytesseract
import imagehash
from dotenv import load_dotenv
from crop_image import crop_image
from logger_config import get_logger
from util import empty_folder, get_ocr_ignore_list, parse_application_name


load_dotenv()

logger = get_logger()

DEBUG = bool(int(os.getenv('DEBUG')))
DEBUG_RESET = bool(int(os.getenv('DEBUG_RESET')))
DEBUG_OCR = bool(int(os.getenv('DEBUG_OCR')))

LIVE_OCR_CONTENT = bool(int(os.getenv('LIVE_OCR_CONTENT')))
OCR_UNKNOWN_APPLICATIONS = bool(int(os.getenv('OCR_UNKNOWN_APPLICATIONS')))

ocr_ignore_list = get_ocr_ignore_list('./ocr_ignore.conf')

phash = None
dhash = None
previous_dhash = None
previous_phash = None

if DEBUG_RESET:
    if os.path.exists('screenshots'):
        logger.warning('Debug reset enabled, deleting images...')
        empty_folder('screenshots')

if not DEBUG_OCR:
    if os.path.exists('ocr'):
        logger.warning('OCR disabled, deleting files...')
        empty_folder('ocr')

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

def ocr_content(image):
    """Manually load an image and OCR its content"""
    image = Image.open(image)
    crop_data = crop_image(image)
    return ocr_content_live(crop_data[0])

def ocr_content_live(cropped_image):
    """OCR the content of an image after titlebar extraction"""
    content_str = ""
    content = binarize_image(cropped_image)
    if bool(int(os.getenv('ENABLE_BINARIZATION'))):
        content = binarize_image(cropped_image)
    content_str = pytesseract.image_to_string(content).strip()
    if content_str is None:
        content_str = ""
    return content_str

def process_display():
    global phash, dhash, previous_dhash, previous_phash
    if DEBUG:
        start_time = time.time()

    os.makedirs(f"./screenshots", exist_ok=True)

    datetime_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_file = f"./screenshots/{datetime_string}.png"
    take_screenshot(screenshot_file)
    logger.debug(f"Screenshot taken: {screenshot_file}")

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

    application_name = parse_application_name(titlebar_str)

    # Extract the content and OCR it
    content_str = ""
    should_ocr_content = True
    if LIVE_OCR_CONTENT:
        if application_name == "Unknown":
            if OCR_UNKNOWN_APPLICATIONS:
                content_str = ocr_content_live(crop_data[0])
            else:
                should_ocr_content = False
                logger.debug('Skipping OCR for unknown application')
        elif application_name in ocr_ignore_list:
            should_ocr_content = False
            logger.debug('Skipping OCR for ignored application ' + application_name)
        else:
            content_str = ocr_content_live(crop_data[0])

    capture_result = {
        'datetime': datetime_string,
        'file_path': screenshot_file,
        'ocr_title': titlebar_str,
        'ocr_content': content_str,
        'application_name': application_name,
        'should_ocr_content': should_ocr_content,
        'url': ''
    }

    previous_dhash = dhash
    previous_phash = phash

    if DEBUG_OCR:
        os.makedirs(f"./ocr", exist_ok=True)

        # Write OCR title to a file
        if len(titlebar_str) > 0:
            with open(f"./ocr/{datetime_string}_title.txt", "w") as file:
                file.write(titlebar_str)

        # Write OCR content to a file
        if len(content_str) > 0:
            with open(f"./ocr/{datetime_string}_content.txt", "w") as file:
                file.write(content_str)

    if DEBUG:
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.debug(f"Executed in {elapsed_time} seconds")

    return capture_result