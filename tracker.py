import threading
import time
from datetime import datetime
import os
import shutil
from dotenv import load_dotenv
from screenshot import take_screenshot
# from difference_hash import difference_hash
from crop_image import crop_image
from PIL import Image
import pytesseract
import imagehash

load_dotenv()

DEBUG = True

previous_hash = None

def binarize_image(image):
    img_copy = image.copy()
    # Convert to grayscale
    img_copy = img_copy.convert("L")
    # Perform the binarization through a simple lambda
    img_copy = img_copy.point(lambda x: 255 if x > int(os.getenv('BINARIZATION_THRESHOLD')) else 0, mode="1")
    return image

def process_screenshot():
    global previous_hash
    if DEBUG:
        start_time = time.time()

    datetime_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_file = f"./screenshots/{datetime_string}.png"
    take_screenshot(screenshot_file)

    capture = Image.open(f"./screenshots/{datetime_string}.png")

    # Check if the current screenshot is perceptually different from the previous one
    hash = imagehash.phash(capture)
    if previous_hash is not None:
        if hash == previous_hash:
            print(f"Skipping identical frame: {screenshot_file}")
            os.remove(screenshot_file)

            # if DEBUG:
            #     end_time = time.time()
            #     elapsed_time = end_time - start_time
            #     print(f"Executed in {elapsed_time} seconds")
            # return

    crop_data = crop_image(capture)
    if (len(crop_data) == 2):
        with open(f"./ocr/{datetime_string}_titlebar.txt", "w") as file:
            titlebar = binarize_image(crop_data[1])
            if bool(os.getenv('ENABLE_BINARIZATION')):
                titlebar = binarize_image(crop_data[1])
            file.write(pytesseract.image_to_string(titlebar))
    elif DEBUG:
        print(f"Screenshot does not have titlebar: {screenshot_file}")

    with open(f"./ocr/{datetime_string}_content.txt", "w") as file:
        content = binarize_image(crop_data[0])
        if bool(os.getenv('ENABLE_BINARIZATION')):
            content = binarize_image(crop_data[0])
        file.write(pytesseract.image_to_string(content))

    print(f"Screenshot taken: {screenshot_file}")
    previous_hash = hash

    if DEBUG:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function executed in {elapsed_time} seconds")

def screenshot_timer(func):
    threading.Timer(int(os.getenv('SCREENSHOT_INTERVAL')), screenshot_timer, [func]).start()
    func()

# Clear contents of image folders in debug mode
if DEBUG:
    print('Debug enabled, deleting images...')
    for folder in ['screenshots', 'ocr']:
        for filename in os.listdir(folder):
            if filename == '.gitkeep':  # Skip .gitkeep files
                continue
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


screenshot_timer(process_screenshot)
