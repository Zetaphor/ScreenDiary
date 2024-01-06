import os
import shutil
from logger_config import get_logger
import json
import re

logger = get_logger()
dbus_ignore_entries = []
ocr_ignore_entries = []
application_name_remaps = []

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

def remove_jsonc_comments(jsonc_str):
    # Pattern for C-style single-line and multi-line comments
    pattern = r'//.*?$|/\*.*?\*/'
    try:
        # Substitute comments with an empty string
        return re.sub(pattern, '', jsonc_str, flags=re.MULTILINE | re.DOTALL)
    except re.error as e:
        logger.error(f"Regex error: {e}")
        logger.error("Failed to remove JSONC comments")
        exit(1)

def load_jsonc(file_path):
    try:
        with open(file_path, 'r') as file:
            jsonc_str = file.read()
        json_str = remove_jsonc_comments(jsonc_str)
        if json_str is not None:
            return json.loads(json_str)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in file {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while loading JSONC file {file_path}: {e}")
        return None
    return None

def in_dbus_ignore(windowData):
    global dbus_ignore_entries
    try:
        for entry in dbus_ignore_entries:
            match = True
            for key in entry:
                if key.endswith('_exact'):
                    continue
                exact_key = f"{key}_exact"
                is_exact = entry.get(exact_key, False)
                entry_value = entry[key].lower()
                window_value = windowData.get(key, '').lower()

                if is_exact:
                    if entry_value != window_value:
                        match = False
                        break
                else:
                    if entry_value not in window_value:
                        match = False
                        break
            if match:
                return True
        return False
    except Exception as e:
        logger.error(f"Error checking DBus ignore list: {e}")
        exit(1)


def in_ocr_ignore(title_string):
    global ocr_ignore_entries
    try:
        title_string = title_string.lower()
        for condition in ocr_ignore_entries:
            if 'endswith' in condition and title_string.endswith(condition['endswith'].lower()):
                return True
            if 'startswith' in condition and title_string.startswith(condition['startswith'].lower()):
                return True
            if 'contains' in condition and condition['contains'].lower() in title_string:
                return True
            if 'equals' in condition and title_string == condition['equals'].lower():
                return True
        return False
    except Exception as e:
        logger.error(f"Error in checking OCR ignore list: {e}")
        return False

def load_ignore_lists():
    global dbus_ignore_entries, ocr_ignore_entries
    dbus_ignore_entries = load_jsonc('ignore_dbus.jsonc')
    if dbus_ignore_entries is not None:
        logger.info(f"Loaded {len(dbus_ignore_entries)} DBus ignore entries")
    else:
        logger.error("Failed to load DBus ignore entries")
        exit(1)

    ocr_ignore_entries = load_jsonc('ignore_ocr.jsonc')
    if ocr_ignore_entries is not None:
        logger.info(f"Loaded {len(ocr_ignore_entries)} OCR ignore entries")
    else:
        logger.error("Failed to load OCR ignore entries")
        exit(1)

def load_application_name_remaps():
    global application_name_remaps
    application_name_remaps = load_jsonc('application_name_remaps.jsonc')
    if application_name_remaps is not None:
        logger.info(f"Loaded {len(application_name_remaps)} application name remaps")
    else:
        logger.error("Failed to load application name remaps")
        exit(1)

def get_application_remap(windowData, using_ocr):
    try:
        for entry in application_name_remaps:
            if using_ocr and 'caption' not in entry:
                continue

            match = True
            for key in entry:
                if key.endswith('_exact') or key == 'new_name':
                    continue

                if using_ocr and key != 'caption':
                    continue

                exact_key = f"{key}_exact"
                is_exact = entry.get(exact_key, False)
                entry_value = entry[key].lower()
                window_value = windowData.get(key, '').lower()

                if is_exact:
                    if entry_value != window_value:
                        match = False
                        break
                else:
                    if entry_value not in window_value:
                        match = False
                        break

            if match:
                return entry.get('new_name')

        return None
    except Exception as e:
        logger.error(f"Error in get_application_remap: {e}")
        exit(1)

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