import os
import shutil
from logger_config import get_logger

logger = get_logger()

import os
import shutil
from logger_config import get_logger

logger = get_logger()

def application_is_browser(title):
    title = title.lower()
    is_browser = False
    # Checking against list of browsers supported by browser-history package
    if 'chrome' in title or 'firefox' in title or 'edge' in title or 'opera' in title or 'brave' in title or 'vivaldi' in title or 'chromium' in title or 'safari' in title or 'librewolf' in title:
        is_browser = True
    return is_browser

def parse_application_name(title):
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

def empty_folder(folder_path):
    for folder in [folder_path]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logger.error(f'Failed to delete {file_path}. Reason: {e}')

def get_ocr_ignore_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if not line.startswith('#')]


def empty_folder(folder_path):
    for folder in [folder_path]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                logger.error('Failed to delete %s. Reason: %s' % (file_path, e))