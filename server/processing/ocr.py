from server.processing.image_manipulation import binarize_image, crop_image
from server.util import parse_application_name
import pytesseract
import os

def ocr_titlebar(image):
    titlebar_str = ""
    title_text = ""
    application_name = "Unknown"
    crop_data = crop_image(image)
    if (len(crop_data) == 2):
        titlebar = binarize_image(crop_data[1])
        if bool(os.getenv('ENABLE_BINARIZATION')):
            titlebar = binarize_image(crop_data[1])
        titlebar_str = pytesseract.image_to_string(titlebar).strip()
        if titlebar_str is None:
            titlebar_str = ""
        title_text, application_name = parse_application_name(titlebar_str)
    return titlebar_str, title_text, application_name

def ocr_content(image):
    crop_data = crop_image(image)[0]
    content_str = ""
    content = binarize_image(crop_data)
    if bool(int(os.getenv('ENABLE_BINARIZATION'))):
        content = binarize_image(crop_data)
    content_str = pytesseract.image_to_string(content).strip()
    if content_str is None:
        content_str = ""
    return content_str