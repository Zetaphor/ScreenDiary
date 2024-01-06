import os
import shutil
from logger_config import get_logger

logger = get_logger()

import os
import shutil
from logger_config import get_logger

logger = get_logger()

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