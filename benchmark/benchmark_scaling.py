from PIL import Image
import pytesseract
import time
import timeit

threshold = 50
resize_scale = 0.6
image_path = './benchmark/editor.png'

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
    # Calculate the new size, X% of the original size
    new_size = tuple(int(dim * resize_scale) for dim in img.size)
    # Resize the image
    resized_img = img.resize(new_size, resampling_methods[resize_method])
    text = pytesseract.image_to_string(resized_img)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Function executed in {elapsed_time} seconds")
    with open(f"./benchmark/test/resized_{resize_method}.txt", "w") as file:
      file.write(text)
    resized_img.save(f"./benchmark/test/resized_{resize_method}.png")
    return True

# https://pillow.readthedocs.io/en/stable/handbook/concepts.html#filters-comparison-table
test_method('NEAREST') # This is pretty much unusable
test_method('BILINEAR')
test_method('BICUBIC')
test_method('LANCZOS')
test_method('BOX')
test_method('HAMMING')



