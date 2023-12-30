from crop_image import crop_titlebar
from difference_hash import perceptual_hash
from tesseract import extract_text_from_image
import timeit
from dotenv import load_dotenv
import os
import time


load_dotenv()

file = "editor"

# print('Perceptual hashing')
# execution_time = timeit.timeit(lambda: perceptual_hash(f"./benchmark/{file}.png"), number=1000)
# print(f"Average execution time: {execution_time / 1000} seconds")

start_time = time.time()
print("Finding color")
find_color_y_position(f"./benchmark/{file}.png", 105, os.getenv('TITLEBAR_COLOR'))
# execution_time = timeit.timeit(lambda: find_color_y_position(f"./benchmark/{file}.png", 105, os.getenv('TITLEBAR_COLOR')), number=1000)
# print(f"Average execution time: {execution_time / 1000} seconds")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Function executed in {elapsed_time} seconds")

start_time = time.time()
print("Cropping titlebar")
crop_titlebar(f"./benchmark/{file}_crop.png", f"./benchmark/{file}_crop_titlebar.png")
# execution_time = timeit.timeit(lambda: crop_titlebar(f"./benchmark/{file}_crop.png", f"./benchmark/{file}_crop_titlebar.png"), number=1000)
# print(f"Average execution time: {execution_time / 1000} seconds")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Function executed in {elapsed_time} seconds")

def extract_title():
  global file
  with open(f"./benchmark/{file}_content.txt", "w") as file:
    title = extract_text_from_image(f"./benchmark/{file}_crop.png")
    file.write(title)

def extract_content():
  global file
  with open(f"./benchmark/{file}_content.txt", "w") as file:
    content = extract_text_from_image(f"./benchmark/{file}_crop.png")
    file.write(content)

# start_time = time.time()
# print("Extract title")
# extract_title()
# execution_time = timeit.timeit(lambda: extract_title, number=1000)
# print(f"Average execution time: {execution_time / 1000} seconds")
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Function executed in {elapsed_time} seconds")

# start_time = time.time()
# print("Extract content")
# extract_content()
# execution_time = timeit.timeit(lambda: extract_content, number=1000)
# print(f"Average execution time: {execution_time / 1000} seconds")
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Function executed in {elapsed_time} seconds")