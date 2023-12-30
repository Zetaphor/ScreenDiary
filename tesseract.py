from PIL import Image
import pytesseract

def extract_text_from_image(image_path):
    """
    Extracts text from an image file using OCR (Optical Character Recognition).

    Args:
    image_path (str): The file path of the image from which to extract text.

    Returns:
    str: The extracted text.
    """
    # Open an image using PIL
    image = Image.open(image_path)

    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(image)

    return text

text = extract_text_from_image('./screenshots/qtbus_titlebar.png')
print(text)
text = extract_text_from_image('./screenshots/editor_titlebar.png')
print(text)