import os
import shutil
from logger_config import get_logger

logger = get_logger()

def parse_application_name(title):
    # Finding the index of the last occurrence of a dash (hyphen, en dash, em dash)
    last_hyphen = title.rfind(' - ')
    last_en_dash = title.rfind(' – ')
    last_em_dash = title.rfind(' — ')

    # Get the position of the last dash, whichever it is
    last_dash = max(last_hyphen, last_en_dash, last_em_dash)

    # If a dash is found, slice the string from that point
    if last_dash != -1:
        return title[last_dash + 3:]  # +3 to skip the dash and the spaces
    else:
        return "Unknown"

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