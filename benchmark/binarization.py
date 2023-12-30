import pytesseract
from PIL import Image
import time
import pytesseract
import cv2
import numpy as np

image = Image.open('./benchmark/browser.png')

binarized_img = image.convert("1")

print('Without binarization')
start_time = time.time()
text = pytesseract.image_to_string(image)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Function executed in {elapsed_time} seconds")
with open(f"./benchmark/no_binarization.txt", "w") as file:
  file.write(text)

print('With Pillow binarization')
start_time = time.time()
text = pytesseract.image_to_string(binarized_img)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Function executed in {elapsed_time} seconds")
with open(f"./benchmark/pillow_binarization.txt", "w") as file:
  file.write(text)
binarized_img.save('./benchmark/browser_binarized.png')

print('With Lambda binarization')
start_time = time.time()
threshold = 50
img_copy = image.copy()
# convert to grayscale
img_copy = img_copy.convert("L")
# perform the binarization through a simple lambda
img_copy = img_copy.point(lambda x: 255 if x > threshold else 0, mode="1")
text = pytesseract.image_to_string(img_copy)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Function executed in {elapsed_time} seconds")
with open(f"./benchmark/lambda_binarization.txt", "w") as file:
  file.write(text)
img_copy.save('./benchmark/browser_lambda_binarized.png')

print('With OpenCV binarization erosion')
start_time = time.time()
img = cv2.imread('./benchmark/browser.png',0)
kernel = np.ones((3,3),np.uint8)
erosion = cv2.erode(img,kernel,iterations = 1)
# Save the eroded image
cv2.imwrite('./benchmark/browser_erosion.png', erosion)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Function executed in {elapsed_time} seconds")

print('With OpenCV binarization dilation')
start_time = time.time()
img = cv2.imread('./benchmark/browser.png',0)
kernel = np.ones((3,3),np.uint8)
dilation = cv2.dilate(img,kernel,iterations = 1)
# Save the dilated image
cv2.imwrite('./benchmark/browser_dilation.png', dilation)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Function executed in {elapsed_time} seconds")