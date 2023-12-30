import threading
import time
from datetime import datetime
import os
import shutil
from dotenv import load_dotenv
from screenshot import take_screenshot
from image_hashing import perceptual_hash
from tesseract import extract_text_from_image
from crop_titlebar import crop_titlebar

load_dotenv()

DEBUG = True

previous_hash = None

def process_screenshot():
    global previous_hash
    if DEBUG:
      start_time = time.time()

    datetime_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_file = f"./screenshots/capture/{datetime_string}.png"
    take_screenshot(screenshot_file)
    hash = perceptual_hash(screenshot_file)

    # Check if the current screenshot is perceptually different from the previous one
    if previous_hash is not None:
        if hash == previous_hash:
          print(f"Skipping identical frame: {screenshot_file}")
          os.remove(screenshot_file)

          if DEBUG:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Executed in {elapsed_time} seconds")
          return

    titlebar_cropped = crop_titlebar(f"./screenshots/capture/{datetime_string}.png", f"./screenshots/titlebar/{datetime_string}_titlebar.png")
    # if titlebar_cropped:
    #     with open(f"./ocr/titlebar/{datetime_string}_titlebar.txt", "w") as file:
    #       file.write(extract_text_from_image(f"./screenshots/titlebar/{datetime_string}_titlebar.png"))
    # else:
    #     print(f"Screenshot does not have titlebar: {screenshot_file}")

    # with open(f"./ocr/content/{datetime_string}_content.txt", "w") as file:
    #   file.write(extract_text_from_image(f"./screenshots/capture/{datetime_string}.png"))

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
    for folder in ['screenshots/crop', 'screenshots/capture', 'screenshots/titlebar', 'ocr/titlebar', 'ocr/content']:
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
