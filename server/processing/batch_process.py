import os
from dotenv import load_dotenv
from server.logger_config import get_logger
from server.database import get_next_batch_ocr_record, get_next_batch_url_record, update_record
from server.processing.browser import capture_url
from server.processing.ocr import ocr_content
from PIL import Image
import time

load_dotenv()
logger = get_logger()

DEBUG_OCR = bool(int(os.getenv('DEBUG_OCR')))

OCR_UNKNOWN_APPLICATIONS = bool(int(os.getenv('OCR_UNKNOWN_APPLICATIONS')))

CAPTURE_BROWSER_URL = bool(int(os.getenv('CAPTURE_BROWSER_URL')))
BROWSER_HISTORY_MATCH_TIME_RANGE = int(os.getenv('BROWSER_HISTORY_MATCH_TIME_RANGE'))

def process_next_batch():
  record = get_next_batch_ocr_record()
  if len(record) == 1:
    id, file_path, ocr_time = record[0]

    ocr_start_time = time.time()
    capture = Image.open(file_path)
    content = ocr_content(capture)
    ocr_time += time.time() - ocr_start_time

    update_record({'record_id': id, 'ocr_content': content, 'ocr_completed': True, 'ocr_time': ocr_time})
    logger.debug(f"Batch OCR complete: {file_path}")

  if CAPTURE_BROWSER_URL:
    record = get_next_batch_url_record()
    if len(record) == 1:
      id, datetime, ocr_title, application_name = record[0]
      url, url_time, url_partial = capture_url(application_name, ocr_title, datetime)
      update_record({'id': id, 'url': url, 'url_time': url_time, 'url_partial': url_partial, 'url_captured': True})
      logger.debug(f"Batch URL capture complete: {url}")