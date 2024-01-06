from processing.image_manipulation import binarize_image, crop_image
import pytesseract
import os

def parse_ocr_application_name(title):
    # Finding the index of the last occurrence of various dash types
    last_hyphen = title.rfind(' - ')
    last_en_dash = title.rfind(' – ')
    last_em_dash = title.rfind(' — ')

    # Get the position of the last dash, whichever it is
    last_dash = max(last_hyphen, last_en_dash, last_em_dash)

    # If a dash is found, split the string from that point
    if last_dash != -1:
        return (title[:last_dash].strip(), title[last_dash + 3:].strip())  # Extract preceding text and app name
    else:
        return (title, "Unknown")  # No dash found, return original title and "Unknown"

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
        title_text, application_name = parse_ocr_application_name(titlebar_str)
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