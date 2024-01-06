import os
import shutil
from logger_config import get_logger
import json
import re

logger = get_logger()
dbus_ignore_entries = []
ocr_ignore_entries = []

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
        return None

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
    except Exception as e:
        logger.error(f"Unexpected error while loading JSONC file {file_path}: {e}")
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
        logger.error(f"Error in in_dbus_ignore: {e}")
        return False


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
    ocr_ignore_entries = load_jsonc('ignore_ocr.jsonc')
    if ocr_ignore_entries is not None:
        logger.info(f"Loaded {len(ocr_ignore_entries)} OCR ignore entries")
    else:
        logger.error("Failed to load OCR ignore entries")

# Need to test new syntax for in_dbus_ignore
test_data = {
    "name": "test",
    "res": "FFPWA",
    "caption": "Discord",
}

print(in_dbus_ignore(test_data))