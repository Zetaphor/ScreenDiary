import easyocr

import easyocr

def gpu_accelerated_easyocr(image_path):
    # Create a reader instance with GPU enabled
    reader = easyocr.Reader(['en'], gpu=True)

    # Read the image and perform OCR
    results = reader.readtext(image_path)

    # Concatenate all text into a single string with newlines
    all_text = '\n'.join([text for _, text, _ in results])

    return all_text

# Example usage
image_path = './benchmark/editor.png'
extracted_text = gpu_accelerated_easyocr(image_path)
print(extracted_text)
