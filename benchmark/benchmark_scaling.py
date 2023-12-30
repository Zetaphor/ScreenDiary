from PIL import Image
import pytesseract
from dotenv import load_dotenv
import os
import time


load_dotenv()

threshold = 50
resize_scale = 0.75
image_path = 'browser.png'

resampling_methods = {
    'NEAREST': Image.Resampling.NEAREST,
    'BILINEAR': Image.Resampling.BILINEAR,
    'BICUBIC': Image.Resampling.BICUBIC,
    'LANCZOS': Image.Resampling.LANCZOS,
    'BOX': Image.Resampling.BOX,
    'HAMMING': Image.Resampling.HAMMING,
}

def test_method(resize_method):
  print(f"Testing {resize_method}")
  start_time = time.time()
  with Image.open(image_path) as img:
    img_copy = img.copy()
    # convert to grayscale
    img_copy = img_copy.convert("L")
    # perform the binarization through a simple lambda
    img_copy = img_copy.point(lambda x: 255 if x > threshold else 0, mode="1")

    # Resize while keeping aspect ratio
    # max_width = int(os.getenv('RESIZE_MAX_WIDTH'))
    # width_percent = (max_width) / float(img_copy.size[0])
    # new_height = int((float(img_copy.size[1]) * float(width_percent)))
    # resized_img = img_copy.resize((max_width, new_height), resampling_methods[resize_method])

    text = pytesseract.image_to_string(img_copy)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Function executed in {elapsed_time} seconds")
    with open(f"resized_{resize_method}.txt", "w") as file:
      file.write(text)
    img_copy.save(f"resized_{resize_method}.png")
    return True

# https://pillow.readthedocs.io/en/stable/handbook/concepts.html#filters-comparison-table
test_method('NEAREST') # This is pretty much unusable
test_method('BILINEAR')
test_method('BICUBIC')
test_method('LANCZOS')
test_method('BOX')
test_method('HAMMING')



